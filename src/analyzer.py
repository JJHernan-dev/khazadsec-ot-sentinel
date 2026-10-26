
import csv
import sys
from pathlib import Path



# Rutas del proyecto.
PROJECT_ROOT = Path(__file__).resolve().parent.parent
INVENTORY_FILE = PROJECT_ROOT / "data" / "inventario.csv"
COMMUNICATIONS_FILE = PROJECT_ROOT / "data" / "comunicaciones.csv"
REPORTS_DIR = PROJECT_ROOT / "reports"
REPORT_FILE = REPORTS_DIR / "hallazgos.csv"

# Prioridades y campos del informe.
FINDING_FIELDS = [
    "id_hallazgo",
    "regla",
    "activo_afectado",
    "prioridad",
    "titulo",
    "evidencia",
    "recomendacion",
]

INVENTORY_FIELDS = {
    "id",
    "nombre",
    "zona",
    "acceso_restringido",
    "actualizaciones_definidas",
}

COMMUNICATION_FIELDS = {
    "id_comunicacion",
    "origen",
    "destino",
    "estado",
    "control_previsto",
}


def load_csv(file_path, required_fields):
    """Leer un CSV y comprobar que contiene las columnas requeridas."""
    if not file_path.is_file():
        raise ValueError(f"No se encuentra el archivo: {file_path}")

    with file_path.open(
        "r", encoding="utf-8-sig", newline=""
    ) as csv_file:
        reader = csv.DictReader(csv_file)

        if reader.fieldnames is None:
            raise ValueError(f"El CSV está vacío: {file_path.name}")

        headers = {
            header.strip() for header in reader.fieldnames if header
        }
        missing = required_fields - headers

        if missing:
            raise ValueError(
                f"{file_path.name}: faltan columnas: "
                f"{', '.join(sorted(missing))}"
            )

        return list(reader)



def validate_data(assets, communications):
    """Validar campos, identificadores y referencias entre los CSV."""
    errors = []

    def get_value(row, field):
        """Obtener un valor como texto, incluso si la celda está vacía."""
        return (row.get(field) or "").strip()

    # Validar activos.
    asset_ids = []

    for row_number, asset in enumerate(assets, start=2):
        asset_id = get_value(asset, "id")
        asset_ids.append(asset_id)

        if not asset_id:
            errors.append(
                f"Inventario, fila {row_number}: falta el identificador."
            )

        if not get_value(asset, "zona"):
            errors.append(
                f"Inventario, fila {row_number}: falta la zona."
            )

        restricted = get_value(
            asset, "acceso_restringido"
        ).lower()

        if restricted not in {"si", "no"}:
            errors.append(
                f"Inventario, fila {row_number}: "
                "acceso_restringido debe ser 'si' o 'no'."
            )

        update_policy = get_value(
            asset, "actualizaciones_definidas"
        ).lower()

        if update_policy not in {"si", "no"}:
            errors.append(
                f"Inventario, fila {row_number}: "
                "actualizaciones_definidas debe ser 'si' o 'no'."
            )

    non_empty_asset_ids = [
        asset_id for asset_id in asset_ids if asset_id
    ]

    if len(non_empty_asset_ids) != len(set(non_empty_asset_ids)):
        errors.append(
            "El inventario contiene identificadores duplicados."
        )

    known_assets = set(non_empty_asset_ids)

    # Validar comunicaciones.
    communication_ids = []

    valid_statuses = {
        "permitida",
        "condicional",
        "no_autorizada",
    }

    for row_number, communication in enumerate(
        communications, start=2
    ):
        communication_id = get_value(
            communication, "id_comunicacion"
        )
        communication_ids.append(communication_id)

        if not communication_id:
            errors.append(
                f"Comunicaciones, fila {row_number}: "
                "falta el identificador."
            )

        status = get_value(communication, "estado").lower()

        if status not in valid_statuses:
            errors.append(
                f"Comunicaciones, fila {row_number}: "
                f"estado no válido '{status or 'vacío'}'."
            )

        for field in ("origen", "destino"):
            asset_id = get_value(communication, field)
            label = communication_id or f"fila {row_number}"

            if not asset_id:
                errors.append(
                    f"{label}: falta el campo {field}."
                )
            elif asset_id not in known_assets:
                errors.append(
                    f"{label}: el {field} '{asset_id}' "
                    "no existe en el inventario."
                )

    non_empty_communication_ids = [
        communication_id
        for communication_id in communication_ids
        if communication_id
    ]

    if len(non_empty_communication_ids) != len(
        set(non_empty_communication_ids)
    ):
        errors.append(
            "Hay identificadores de comunicación duplicados."
        )

    return errors



def make_finding(rule, asset, priority, title, evidence, recommendation):
    """Crear un hallazgo con el formato común del informe."""
    return {
        "regla": rule,
        "activo_afectado": asset,
        "prioridad": priority,
        "titulo": title,
        "evidencia": evidence,
        "recomendacion": recommendation,
    }


def detect_unauthorized_communications(communications):
    """R-01: detectar comunicaciones marcadas como no autorizadas."""
    findings = []

    for communication in communications:
        status = communication["estado"].strip().lower()

        if status == "no_autorizada":
            findings.append(make_finding(
                "R-01",
                communication["id_comunicacion"].strip(),
                "Alta",
                "Comunicacion no autorizada",
                (
                    f"origen={communication['origen'].strip()}; "
                    f"destino={communication['destino'].strip()}; "
                    f"estado={status}"
                ),
                (
                    "Revisar la necesidad de la comunicacion y aplicar "
                    "los controles de bloqueo previstos en el diseno."
                ),
            ))

    return findings


def detect_unrestricted_ot_assets(assets):
    """R-02: detectar activos OT sin acceso restringido."""
    findings = []

    for asset in assets:
        zone = asset["zona"].strip().upper()
        restricted = asset["acceso_restringido"].strip().lower()

        if zone == "OT" and restricted == "no":
            findings.append(make_finding(
                "R-02",
                asset["id"].strip(),
                "Alta",
                "Activo OT sin acceso restringido",
                f"zona={zone}; acceso_restringido={restricted}",
                (
                    "Revisar los controles de acceso del activo y "
                    "documentar las restricciones necesarias."
                ),
            ))

    return findings


def detect_undefined_update_policies(assets):
    """R-03: detectar activos sin politica de actualizaciones definida."""
    findings = []

    for asset in assets:
        policy = asset["actualizaciones_definidas"].strip().lower()

        if policy == "no":
            findings.append(make_finding(
                "R-03",
                asset["id"].strip(),
                "Media",
                "Politica de actualizaciones no definida",
                f"actualizaciones_definidas={policy}",
                (
                    "Definir y documentar una politica de gestion de "
                    "actualizaciones adecuada para el activo, teniendo "
                    "en cuenta las necesidades operativas de OT."
                ),
            ))

    return findings


def detect_conditional_communications_without_controls(communications):
    """R-04: detectar comunicaciones condicionales sin control documentado."""
    findings = []

    for communication in communications:
        status = communication["estado"].strip().lower()
        control = communication["control_previsto"].strip()

        if status == "condicional" and not control:
            findings.append(make_finding(
                "R-04",
                communication["id_comunicacion"].strip(),
                "Media",
                "Comunicacion condicional sin control documentado",
                f"estado={status}; control_previsto=vacío",
                (
                    "Documentar el control que debe hacer cumplir "
                    "la condicion de acceso y definir como verificarlo."
                ),
            ))

    return findings


def assign_finding_ids(findings):
    """Asignar identificadores secuenciales a los hallazgos."""
    for number, finding in enumerate(findings, start=1):
        finding["id_hallazgo"] = f"H-{number:03d}"

    return findings


def write_report(findings):
    """Guardar los hallazgos en un CSV."""
    REPORTS_DIR.mkdir(parents=True, exist_ok=True)

    with REPORT_FILE.open(
        "w", encoding="utf-8-sig", newline=""
    ) as csv_file:
        writer = csv.DictWriter(
            csv_file,
            fieldnames=FINDING_FIELDS,
            extrasaction="ignore",
        )
        writer.writeheader()
        writer.writerows(findings)


def main():
    """Cargar datos, validar, detectar y generar el informe."""
    try:
        assets = load_csv(INVENTORY_FILE, INVENTORY_FIELDS)
        communications = load_csv(
            COMMUNICATIONS_FILE, COMMUNICATION_FIELDS
        )

        print(f"Activos cargados: {len(assets)}")
        print(f"Comunicaciones cargadas: {len(communications)}")

        errors = validate_data(assets, communications)

        if errors:
            print("\nErrores de validacion:")
            for error in errors:
                print(f"ERROR: {error}")

            if REPORT_FILE.exists():
                print(
                    "\nAVISO: no se ha actualizado el informe. "
                    "El archivo existente puede corresponder a una ejecucion anterior:"
                )
                print(REPORT_FILE.relative_to(PROJECT_ROOT))
            else:
                print("\nNo se ha generado ningun informe.")

            return 1

        print("Validacion de datos: correcta.")

        findings = []
        findings.extend(
            detect_unauthorized_communications(communications)
        )
        findings.extend(detect_unrestricted_ot_assets(assets))
        findings.extend(detect_undefined_update_policies(assets))
        findings.extend(
            detect_conditional_communications_without_controls(
                communications
            )
        )

        assign_finding_ids(findings)
        write_report(findings)

        print(f"\nTotal de hallazgos: {len(findings)}")

        for finding in findings:
            print(
                f"[{finding['prioridad']}] "
                f"{finding['id_hallazgo']} "
                f"{finding['regla']} - {finding['titulo']}"
            )
            print(f"  Elemento: {finding['activo_afectado']}")
            print(f"  Evidencia: {finding['evidencia']}")

        print(f"\nInforme generado: {REPORT_FILE.relative_to(PROJECT_ROOT)}")
        return 0

    except (OSError, ValueError, KeyError) as error:
        print(f"ERROR: {error}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
