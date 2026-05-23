{
    "name": "Purchase RFQ Follow-Up",
    "version": "19.0.1.0.0",
    "summary": "Auto-schedule internal follow-up activities when an RFQ is sent, plus a vendor-response insight dashboard.",
    "description": """
Purchase RFQ Follow-Up
======================
Auto-creates three internal follow-up activities on RFQ send at configurable
intervals (default 2 / 5 / 10 days). Pending follow-ups auto-close when the
order is confirmed or cancelled.

Includes an Intelligence Dashboard (Reporting > RFQ Follow-Up Insights) that
computes per-vendor metrics from your own RFQ history and a rule-based smart
suggestion that recommends a custom follow-up schedule per vendor.

No external AI service. No data sharing. All "intelligence" is rule-based
heuristics on data already in your database.
    """,
    "author": "Muhammad Dzakwan Robbani",
    "website": "https://github.com/dzakwanrobbani/odoo-apps",
    "license": "LGPL-3",
    "category": "Inventory/Purchase",
    "depends": ["purchase", "mail"],
    "data": [
        "data/ir_default_data.xml",
        "views/res_config_settings_views.xml",
        "views/purchase_order_views.xml",
        "views/dashboard_views.xml",
        "views/menus.xml",
    ],
    "images": [
        "static/description/icon.png",
        "static/description/screenshot_01_chatter.png",
        "static/description/screenshot_02_settings.png",
        "static/description/screenshot_03_button.png",
        "static/description/screenshot_04_dashboard.png",
        "static/description/screenshot_05_activities.png",
        "static/description/screenshot_06_compare.png",
    ],
    "installable": True,
    "application": False,
    "auto_install": False,
}
