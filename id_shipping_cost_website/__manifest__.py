{
    "name": "Indonesia Shipping Cost — Website Checkout",
    "version": "19.0.1.0.0",
    "summary": "eCommerce checkout integration for Indonesia Shipping Cost (calibration banner + JSON rate endpoint).",
    "description": """
Indonesia Shipping Cost — Website Checkout
==========================================
Companion add-on for `id_shipping_cost`. Installs automatically when
both `id_shipping_cost` and `website_sale` are present.

* Calibration banner on /shop/checkout when the operator has not yet
  confirmed bundled rates are calibrated to their contracted prices.
* JSON endpoint `/id_shipping/calculate` returning the full rate matrix
  for the current cart (used by storefront customisations).

The actual Indonesia courier picker reuses Odoo's built-in delivery
method dropdown — each `delivery.carrier` with `delivery_type='id_offline'`
shows up automatically.
    """,
    "author": "Muhammad Dzakwan Robbani",
    "website": "https://github.com/dzakwanrobbani/odoo-apps",
    "license": "LGPL-3",
    "category": "Website/Website",
    "depends": ["id_shipping_cost", "website_sale"],
    "data": [
        "views/website_templates.xml",
    ],
    "installable": True,
    "application": False,
    "auto_install": True,
}
