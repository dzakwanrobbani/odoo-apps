import math

from odoo import http
from odoo.http import request


class IdShippingWebsite(http.Controller):

    @http.route(
        "/id_shipping/calculate",
        type="jsonrpc",
        auth="public",
        website=True,
        csrf=False,
    )
    def calculate(self, origin_code=None, dest_code=None, weight_kg=None):
        """Return a sorted list of available rates for the given OD pair.

        Public endpoint — used by storefront JS to preview rates before
        the customer commits to a delivery method. The actual order
        carrier selection still goes through the standard `website_sale`
        flow, which lists `delivery.carrier` records configured by the
        operator.
        """
        if not origin_code or not dest_code:
            order = request.website.sale_get_order() if request.website else None
            if order and order.partner_shipping_id.id_shipping_region_id:
                dest_code = dest_code or order.partner_shipping_id.id_shipping_region_id.code
            icp = request.env["ir.config_parameter"].sudo()
            default_origin_id = icp.get_param("id_shipping_cost.default_origin_id")
            if default_origin_id and not origin_code:
                origin = request.env["id.shipping.region"].sudo().browse(
                    int(default_origin_id)
                ).exists()
                if origin:
                    origin_code = origin.code
        if not origin_code or not dest_code:
            return {"success": False, "error": "origin_code and dest_code required"}

        try:
            weight = float(weight_kg or 1.0)
        except (TypeError, ValueError):
            weight = 1.0

        origin = request.env["id.shipping.region"].sudo().search(
            [("code", "=", origin_code)], limit=1
        )
        dest = request.env["id.shipping.region"].sudo().search(
            [("code", "=", dest_code)], limit=1
        )
        if not origin or not dest:
            return {
                "success": False,
                "error": f"Unknown region code(s): {origin_code} / {dest_code}",
            }

        rates = request.env["id.shipping.rate"].sudo().search(
            [("origin_id", "=", origin.id), ("dest_id", "=", dest.id)],
            order="price_per_kg asc",
        )
        results = []
        for rate in rates:
            chargeable_kg = max(rate.min_kg, math.ceil(weight))
            cost = chargeable_kg * rate.price_per_kg + rate.base_fee
            results.append(
                {
                    "provider_code": rate.provider_id.code,
                    "provider_name": rate.provider_id.name,
                    "service_code": rate.service_id.code,
                    "service_name": rate.service_id.name,
                    "price": cost,
                    "etd_min_days": rate.etd_min_days,
                    "etd_max_days": rate.etd_max_days,
                }
            )
        icp = request.env["ir.config_parameter"].sudo()
        calibrated = (
            (icp.get_param("id_shipping_cost.rates_calibrated") or "False")
            .lower()
            in ("true", "1")
        )
        return {
            "success": True,
            "origin_code": origin_code,
            "dest_code": dest_code,
            "weight_kg": weight,
            "rates_calibrated": calibrated,
            "results": results,
        }
