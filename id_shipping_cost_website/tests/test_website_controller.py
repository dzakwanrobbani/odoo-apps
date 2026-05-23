import json

from odoo.tests import HttpCase, tagged


@tagged("post_install", "-at_install")
class TestWebsiteController(HttpCase):

    def _jsonrpc(self, route, params):
        return self.url_open(
            route,
            data=json.dumps({"jsonrpc": "2.0", "params": params}),
            headers={"Content-Type": "application/json"},
        )

    def test_calculate_happy_path(self):
        res = self._jsonrpc(
            "/id_shipping/calculate",
            {"origin_code": "DKI", "dest_code": "JABAR", "weight_kg": 1.0},
        )
        body = res.json()["result"]
        self.assertTrue(body["success"])
        self.assertEqual(body["origin_code"], "DKI")
        self.assertEqual(body["dest_code"], "JABAR")
        self.assertGreater(len(body["results"]), 0)
        first = body["results"][0]
        self.assertIn("provider_code", first)
        self.assertIn("price", first)
        self.assertGreater(first["price"], 0)

    def test_calculate_unknown_region(self):
        res = self._jsonrpc(
            "/id_shipping/calculate",
            {"origin_code": "DKI", "dest_code": "ATLANTIS", "weight_kg": 1.0},
        )
        body = res.json()["result"]
        self.assertFalse(body["success"])
        self.assertIn("Unknown region", body["error"])

    def test_calculate_includes_calibration_flag(self):
        self.env["ir.config_parameter"].sudo().set_param(
            "id_shipping_cost.rates_calibrated", "False"
        )
        res = self._jsonrpc(
            "/id_shipping/calculate",
            {"origin_code": "DKI", "dest_code": "JABAR", "weight_kg": 1.0},
        )
        body = res.json()["result"]
        self.assertIn("rates_calibrated", body)
        self.assertFalse(body["rates_calibrated"])
