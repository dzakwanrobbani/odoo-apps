# Sales Quote Follow-Up

Auto-schedules three follow-up activities the moment an Odoo quotation is sent. Pending follow-ups auto-close when the order is confirmed or cancelled. Zero setup, works out of the box.

## Features

- Auto-creates 3 follow-up activities on quotation send (default day +2, +5, +10)
- Auto-closes pending follow-ups when the order is confirmed or cancelled
- Per-database configuration in **Settings > Sales > Quotations**
- Manual **Schedule Follow-Ups** button on the quotation form
- LGPL-3, no external dependencies
- Compatible with Odoo 19 Community and Enterprise

## Installation

1. Place the `sale_quote_followup` folder in your Odoo addons path.
2. Restart Odoo and update the apps list.
3. Search for "Sales Quotation Follow-Up Activities" and install.
4. (Optional) Adjust intervals in **Settings > Sales > Quotations > Auto Follow-Up on Sent Quotations**.

## How it works

- When a user clicks **Send by Email** on a quotation, three `mail.activity` records are scheduled on the order: at day +N1, +N2 and +N3 (default 2 / 5 / 10).
- Activities are tagged with the `[SQF]` marker in their summary so they can be identified and cleaned up later.
- When the order is confirmed or cancelled, every `[SQF]`-marked activity on that order is closed with a corresponding feedback message.
- The **Schedule Follow-Ups** button on the form replaces any existing auto follow-ups, making it idempotent.

## Configuration

Open **Settings > Sales > Quotations** and locate the *Auto Follow-Up on Sent Quotations* section.

| Field | Default | Meaning |
| --- | --- | --- |
| Auto-schedule follow-ups | True | Master switch |
| 1st follow-up (days) | 2 | Days after send for the first reminder |
| 2nd follow-up (days) | 5 | Days after send for the second reminder |
| 3rd follow-up (days) | 10 | Days after send for the third reminder |
| Follow-up activity type | Call | `mail.activity.type` used for created activities |

Intervals must be positive and strictly increasing. The settings page validates this on save.

## Testing checklist (manual)

1. Install on a fresh Odoo 19 DB with `sale_management` installed.
2. Create a quotation and click **Send by Email**. Three activities should appear in the chatter with deadlines H+2, H+5, H+10.
3. Change the intervals in Settings (for example 1 / 3 / 7) and create another quotation. New deadlines should match.
4. Confirm the order. The three activities should close with feedback "Order confirmed".
5. Cancel another quotation that has active follow-ups. Activities should close with feedback "Order cancelled".
6. Click **Schedule Follow-Ups** twice on the same quotation. The total stays at three activities (no duplicates).
7. Try saving Settings with `days_2 <= days_1`. A UserError should appear.
8. Test in a multi-company database. Each company should respect its own settings (note: config parameters are per-database by default; multi-company customisation is a v1.1 item).
9. Uninstall the module. Existing activities remain (they are now plain follow-ups, no longer auto-managed).

## Compatibility

- Tested on Odoo 19.0 Community
- Odoo 20.0: retest required when released
- Requires at least one `mail.activity.type` to exist (Odoo bootstraps several by default, including "Call")

## Assets status (pre-upload)

| Asset | Status | Action required |
| --- | --- | --- |
| `static/description/icon.png` | Generated (envelope + clock motif) | Optional: replace with custom branding before upload. |
| `static/description/screenshot_01..06.png` | **PLACEHOLDER** | **Mandatory: replace with real screenshots from a running Odoo 18 instance before uploading to apps.odoo.com.** Each placeholder is labelled with the scene it should depict. |

apps.odoo.com reviewers will reject a listing whose screenshots are clearly placeholder images. Treat the six PNGs in `static/description/` as slots to be filled, not final deliverables.

## License

LGPL-3 — see `LICENSE`.
