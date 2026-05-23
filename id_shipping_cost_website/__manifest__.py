{
    "name": "Indonesia Shipping Cost — Website Checkout",
    "version": "19.0.1.0.0",
    "summary": "eCommerce checkout integration for Indonesia Shipping Cost (calibration banner + JSON rate endpoint).",
    "description": """
<h2>Indonesia Shipping Cost &mdash; Website Checkout</h2>
<p><strong>Free LGPL-3 companion add-on</strong> for the paid
<code>id_shipping_cost</code> module. Installs automatically when both
<code>id_shipping_cost</code> and <code>website_sale</code> are present.</p>
<ul>
  <li><strong>Calibration banner</strong> on <code>/shop/checkout</code>
  when the operator has not yet confirmed bundled rates are calibrated to
  their contracted prices.</li>
  <li><strong>JSON endpoint</strong> <code>POST /id_shipping/calculate</code>
  returning the full sorted rate matrix for the current cart (used by
  storefront customisations).</li>
</ul>
<p>The actual Indonesia courier picker reuses Odoo&apos;s built-in delivery
method dropdown &mdash; every <code>delivery.carrier</code> with
<code>delivery_type='id_offline'</code> shows up automatically. No fork of
<code>website_sale</code> flow.</p>
    """,
    "author": "Muhammad Dzakwan Robbani",
    "website": "https://github.com/dzakwanrobbani/odoo-apps",
    "license": "LGPL-3",
    "category": "Website/Website",
    "price": 0.0,
    "currency": "USD",
    "depends": ["id_shipping_cost", "website_sale"],
    "data": [
        "views/website_templates.xml",
    ],
    "images": [
        "static/description/icon.png",
        "static/description/banner.png",
    ],
    "installable": True,
    "application": False,
    "auto_install": True,
}
