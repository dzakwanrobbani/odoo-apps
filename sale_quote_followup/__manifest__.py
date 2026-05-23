{
    "name": "Sales Quote Follow-Up",
    "version": "19.0.1.0.0",
    "summary": "Auto-schedule follow-up activities when a quotation is sent. Never lose a quote again.",
    "description": """
Sales Quote Follow-Up
=====================
Auto-creates three follow-up activities on quotation send at configurable
intervals (default 2 / 5 / 10 days). Pending follow-ups auto-close when the
order is confirmed or cancelled. Zero setup, works out of the box.
    """,
    "author": "Muhammad Dzakwan Robbani",
    "website": "https://github.com/dzakwanrobbani/odoo-apps",
    "license": "LGPL-3",
    "category": "Sales/Sales",
    "depends": ["sale_management", "mail"],
    "data": [
        "data/ir_default_data.xml",
        "views/res_config_settings_views.xml",
        "views/sale_order_views.xml",
    ],
    "images": [
        "static/description/icon.png",
        "static/description/screenshot_01_chatter.png",
        "static/description/screenshot_02_settings.png",
        "static/description/screenshot_03_button.png",
        "static/description/screenshot_04_autocancel.png",
        "static/description/screenshot_05_activities.png",
        "static/description/screenshot_06_compare.png",
    ],
    "installable": True,
    "application": False,
    "auto_install": False,
}
