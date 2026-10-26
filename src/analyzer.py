
import csv
from pathlib import Path


# Localizar la raíz del proyecto.
PROJECT_ROOT = Path(__file__).resolve().parent.parent

# Rutas de los archivos de datos.
INVENTORY_FILE = PROJECT_ROOT / "data" / "inventario.csv"
COMMUNICATIONS_FILE = PROJECT_ROOT / "data" / "comunicaciones.csv"


def load_csv(file_path):
    """Leer un CSV y devolver sus filas como diccionarios."""
    with file_path.open("r", encoding="utf-8-sig", newline="") as csv_file:
        reader = csv.DictReader(csv_file)
        return list(reader)


def validate_communications(assets, communications):
    """Comprobar que los origenes y destinos existen en el inventario."""
    asset_ids = {asset["id"].strip() for asset in assets}
    errors = []

    for communication in communications:
        communication_id = communication["id_comunicacion"].strip()
        origin = communication["origen"].strip()
        destination = communication["destino"].strip()

        if not origin:
            errors.append(
                f"{communication_id}: falta el identificador de origen."
            )
        elif origin not in asset_ids:
            errors.append(
                f"{communication_id}: el origen '{origin}' no existe."
            )

        if not destination:
            errors.append(
                f"{communication_id}: falta el identificador de destino."
            )
        elif destination not in asset_ids:
            errors.append(
                f"{communication_id}: el destino '{destination}' no existe."
            )

    return errors


def detect_unrestricted_ot_assets(assets):
    """Detectar activos OT sin acceso restringido."""
    findings = []

    for asset in assets:
        zone = asset["zona"].strip().upper()
        restricted = asset["acceso_restringido"].strip().lower()

        if zone == "OT" and restricted == "no":
            findings.append({
                "regla": "R-02",
                "activo_afectado": asset["id"].strip(),
                "prioridad": "Alta",
                "titulo": "Activo OT sin acceso restringido",
                "evidencia": (
                    f"zona={zone}; "
                    f"acceso_restringido={restricted}"
                ),
                "recomendacion": (
                    "Revisar los controles de acceso del activo y "
                    "documentar las restricciones necesarias."
                ),
            })

    return findings


def detect_unauthorized_communications(communications):
    """Detectar comunicaciones marcadas como no autorizadas."""
    findings = []

    for communication in communications:
        status = communication["estado"].strip().lower()

        if status == "no_autorizada":
            findings.append({
                "regla": "R-01",
                "activo_afectado": communication["id_comunicacion"],
                "prioridad": "Alta",
                "titulo": "Comunicacion no autorizada",
                "evidencia": (
                    f"origen={communication['origen']}; "
                    f"destino={communication['destino']}; "
                    f"estado={status}"
                ),
                "recomendacion": (
                    "Revisar la necesidad de la comunicacion y aplicar "
                    "los controles de bloqueo previstos en el diseno."
                ),
            })

    return findings

def detect_undefined_update_policies(assets):
    """Detectar activos sin politica de actualizaciones definida."""
    findings = []

    for asset in assets:
        update_policy = (
            asset["actualizaciones_definidas"].strip().lower()
        )

        if update_policy == "no":
            findings.append({
                "regla": "R-03",
                "activo_afectado": asset["id"].strip(),
                "prioridad": "Media",
                "titulo": "Politica de actualizaciones no definida",
                "evidencia": (
                    f"actualizaciones_definidas={update_policy}"
                ),
                "recomendacion": (
                    "Definir y documentar una politica de gestion de "
                    "actualizaciones adecuada para el activo, teniendo "
                    "en cuenta las necesidades operativas de OT."
                ),
            })

    return findings

def main():
    """Punto de entrada del analizador."""
    assets = load_csv(INVENTORY_FILE)
    communications = load_csv(COMMUNICATIONS_FILE)

    print(f"Activos cargados: {len(assets)}")
    print(f"Comunicaciones cargadas: {len(communications)}")

    for asset in assets:
        print(f"{asset['id']} - {asset['nombre']}")

    errors = validate_communications(assets, communications)

    print("\nValidacion de comunicaciones:")

    if errors:
        for error in errors:
            print(f"ERROR: {error}")
        raise SystemExit(1)

    print("Correcto: todos los origenes y destinos existen en el inventario.")

    findings = detect_unauthorized_communications(communications)

    print(f"\nHallazgos detectados: {len(findings)}")

    for finding in findings:
        print(
            f"[{finding['prioridad']}] "
            f"{finding['regla']} - {finding['titulo']}"
        )
        print(f"  Elemento: {finding['activo_afectado']}")
        print(f"  Evidencia: {finding['evidencia']}")
        print(f"  Recomendacion: {finding['recomendacion']}")
    
    ot_findings = detect_unrestricted_ot_assets(assets)

    print(f"\nHallazgos R-02: {len(ot_findings)}")

    for finding in ot_findings:
        print(
            f"[{finding['prioridad']}] "
            f"{finding['regla']} - {finding['titulo']}"
        )
        print(f"  Activo: {finding['activo_afectado']}")
        print(f"  Evidencia: {finding['evidencia']}")
        print(f"  Recomendacion: {finding['recomendacion']}")

        update_findings = detect_undefined_update_policies(assets)

    print(f"\nHallazgos R-03: {len(update_findings)}")

    for finding in update_findings:
        print(
            f"[{finding['prioridad']}] "
            f"{finding['regla']} - {finding['titulo']}"
        )
        print(f"  Activo: {finding['activo_afectado']}")
        print(f"  Evidencia: {finding['evidencia']}")
        print(f"  Recomendacion: {finding['recomendacion']}")

if __name__ == "__main__":
    main()
