# Indonesia Shipping Cost — Website Checkout

Companion add-on for the [`id_shipping_cost`](https://apps.odoo.com/apps/modules/19.0/id_shipping_cost) paid module. Adds eCommerce-specific touches to `website_sale` checkout. Installs automatically when both `id_shipping_cost` and `website_sale` are present.

## What this adds

- **Calibration warning banner** on `/shop/checkout` when the merchant has not yet ticked **"Rates Calibrated for Production"** in Inventory settings. Reminds customers and staff that bundled seed rates are estimates until updated.
- **JSON rate endpoint** `POST /id_shipping/calculate` returning the full Indonesia rate matrix for the current cart. Useful for storefront customisations (e.g. show ETD chart pre-checkout) without needing to traverse every Odoo carrier.

The actual courier picker reuses Odoo's built-in delivery dropdown — every `delivery.carrier` with `delivery_type='id_offline'` (configured by the merchant) shows up automatically. No fork of `website_sale` checkout flow.

## Installation

This module **auto-installs** the moment both `id_shipping_cost` and `website_sale` are installed in the same database. Manual install is also fine.

## License

LGPL-3 — see [LICENSE](LICENSE). The paid pricing of the parent module (`id_shipping_cost`) is unaffected: this add-on is intentionally free so customers without eCommerce can install the core module without consuming a paid licence slot for unused features.
