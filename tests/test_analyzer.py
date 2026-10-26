
import sys
import unittest
from pathlib import Path

# Permite importar el analizador desde la carpeta src.
ROOT_DIR = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT_DIR / "src"))

from analyzer import (
    validate_data,
    detect_unauthorized_communications,
    detect_unrestricted_ot_assets,
    detect_undefined_update_policies,
    detect_conditional_communications_without_controls,
)


class TestDetectionRules(unittest.TestCase):

    def test_r01_detects_unauthorized_communication(self):
        communications = [
            {
                "id_comunicacion": "COM-TEST",
                "origen": "IT-01",
                "destino": "OT-03",
                "estado": "no_autorizada",
            }
        ]

        findings = detect_unauthorized_communications(communications)

        self.assertEqual(len(findings), 1)
        self.assertEqual(findings[0]["regla"], "R-01")

    def test_r02_detects_unrestricted_ot_asset(self):
        assets = [
            {
                "id": "OT-TEST",
                "zona": "OT",
                "acceso_restringido": "no",
            }
        ]

        findings = detect_unrestricted_ot_assets(assets)

        self.assertEqual(len(findings), 1)
        self.assertEqual(findings[0]["regla"], "R-02")

    def test_r03_detects_undefined_update_policy(self):
        assets = [
            {
                "id": "OT-TEST",
                "actualizaciones_definidas": "no",
            }
        ]

        findings = detect_undefined_update_policies(assets)

        self.assertEqual(len(findings), 1)
        self.assertEqual(findings[0]["regla"], "R-03")

    def test_r04_detects_conditional_communication_without_control(self):
        communications = [
            {
                "id_comunicacion": "COM-TEST",
                "origen": "OT-05",
                "destino": "OT-03",
                "estado": "condicional",
                "control_previsto": "",
            }
        ]

        findings = detect_conditional_communications_without_controls(
            communications
        )

        self.assertEqual(len(findings), 1)
        self.assertEqual(findings[0]["regla"], "R-04")

    def test_r04_ignores_conditional_communication_with_control(self):
        communications = [
            {
                "id_comunicacion": "COM-TEST",
                "origen": "OT-05",
                "destino": "OT-03",
                "estado": "condicional",
                "control_previsto": "Acceso autorizado solo durante mantenimiento",
            }
        ]

        findings = detect_conditional_communications_without_controls(
            communications
        )

        self.assertEqual(len(findings), 0)


    def test_validation_rejects_unknown_asset_reference(self):
        assets = [
            {
                "id": "IT-01",
                "zona": "IT",
                "acceso_restringido": "si",
                "actualizaciones_definidas": "si",
            }
        ]
        communications = [
            {
                "id_comunicacion": "COM-TEST",
                "origen": "IT-99",
                "destino": "IT-01",
                "estado": "permitida",
                "control_previsto": "Control de prueba",
            }
        ]

        errors = validate_data(assets, communications)

        self.assertTrue(errors)
        self.assertTrue(
            any("IT-99" in error for error in errors),
            f"Se esperaba un error que mencionara IT-99. Errores: {errors}",
        )

    def test_example_scenario_produces_five_findings(self):
        import csv

        data_dir = ROOT_DIR / "data"

        with open(data_dir / "inventario.csv", newline="", encoding="utf-8-sig") as file:
            assets = list(csv.DictReader(file))

        with open(data_dir / "comunicaciones.csv", newline="", encoding="utf-8-sig") as file:
            communications = list(csv.DictReader(file))

        errors = validate_data(assets, communications)
        self.assertEqual(errors, [], f"Errores de validación: {errors}")

        findings = []
        findings.extend(detect_unauthorized_communications(communications))
        findings.extend(detect_unrestricted_ot_assets(assets))
        findings.extend(detect_undefined_update_policies(assets))
        findings.extend(detect_conditional_communications_without_controls(communications))

        self.assertEqual(len(findings), 5)
        self.assertEqual(
            [finding["regla"] for finding in findings].count("R-01"), 1
        )
        self.assertEqual(
            [finding["regla"] for finding in findings].count("R-02"), 1
        )
        self.assertEqual(
            [finding["regla"] for finding in findings].count("R-03"), 3
        )
        self.assertEqual(
            [finding["regla"] for finding in findings].count("R-04"), 0
        )

if __name__ == "__main__":
    unittest.main()
