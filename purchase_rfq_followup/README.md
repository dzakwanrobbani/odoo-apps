# Purchase RFQ Follow-Up

Auto-schedules three internal follow-up activities the moment an Odoo Purchase RFQ is sent to a vendor. Pending follow-ups auto-close when the order is confirmed or cancelled. Includes a per-vendor insight dashboard with rule-based suggestions for tuning your follow-up cadence.

## Features

- Auto-creates 3 follow-up activities on RFQ send (default day +2, +5, +10).
- Auto-closes pending follow-ups when the PO is confirmed or cancelled.
- Per-database configuration in **Settings > Purchase > Auto Follow-Up on Sent RFQ**.
- Manual **Schedule Follow-Ups** button on the RFQ form.
- **RFQ Follow-Up Insights dashboard** under **Purchase > Reporting** — per-vendor stats (total RFQs, response rate, avg response days, pending, overdue) + rule-based smart suggestions.
- 100% rule-based heuristics — **no external AI service, no data sharing**.
- LGPL-3, no Python package dependencies, depends only on `purchase` and `mail` (Odoo core).
- Compatible with Odoo 19 Community and Enterprise.

## Installation

1. Place the `purchase_rfq_followup` folder in your Odoo addons path.
2. Restart Odoo and update the apps list.
3. Install "Purchase RFQ Follow-Up".
4. (Optional) Adjust intervals in **Settings > Purchase**.

## How it works

When a user clicks **Send by Email** on an RFQ, three `mail.activity` records are scheduled on the order at day +N1, +N2 and +N3 (default 2 / 5 / 10). Activities are tagged with the `[PRF]` marker in their summary so they can be identified and cleaned up later. When the order is confirmed or cancelled, every `[PRF]`-marked activity on that order is closed with a corresponding feedback message.

The **Schedule Follow-Ups** button replaces any existing auto follow-ups, making it idempotent.

The **RFQ Follow-Up Insights** dashboard reads your existing `purchase.order` and `mail.activity` records and computes:

- **Total / confirmed RFQs**, **response rate** (% of RFQs that became confirmed POs)
- **Avg response days** (from RFQ creation to PO confirmation)
- **Pending RFQs** (sent, not yet confirmed)
- **Overdue follow-ups** (auto-scheduled activities whose deadline has passed)
- **Smart suggestion** — a rule-based hint per vendor:
  - `avg < days_2_config` → "Responds fast, consider tighter intervals"
  - `avg > days_3_config` → "Responds slow, suggested intervals X / Y / Z"
  - otherwise → "Matches default schedule"
  - vendors with fewer than 3 historical RFQs get no suggestion (insufficient data)

## Configuration

Open **Settings > Purchase** and locate *Auto Follow-Up on Sent RFQ*.

| Field | Default | Meaning |
| --- | --- | --- |
| Auto-schedule RFQ follow-ups | True | Master switch |
| 1st follow-up (days) | 2 | Days after send for the first reminder |
| 2nd follow-up (days) | 5 | Days after send for the second reminder |
| 3rd follow-up (days) | 10 | Days after send for the third reminder |
| Follow-up activity type | Call | `mail.activity.type` used for created activities |

Intervals must be positive and strictly increasing. The settings page validates this on save.

## Testing checklist (manual)

1. Install on a fresh Odoo 19 DB with `purchase` installed.
2. Create an RFQ and click **Send by Email** → three activities appear in the chatter with deadlines H+2, H+5, H+10.
3. Change intervals in Settings → save → create a new RFQ → new deadlines match.
4. Confirm the order. The three activities close with feedback "Order confirmed".
5. Cancel another RFQ that has active follow-ups → activities close with feedback "Order cancelled".
6. Click **Schedule Follow-Ups** twice on the same RFQ → total stays at three activities.
7. Try saving Settings with `days_2 <= days_1` → UserError.
8. After 3+ confirmed RFQs with one vendor, open **Purchase > Reporting > RFQ Follow-Up Insights** → vendor card shows stats and a smart suggestion.
9. Uninstall the module → existing activities remain.

## Compatibility

- Tested on Odoo 19.0 Community
- Requires at least one `mail.activity.type` to exist (Odoo bootstraps several by default, including "Call")

## Privacy & AI disclaimer

This module markets a "Smart Suggestion" feature. To be clear:

- **No external AI service is called.** No data leaves your Odoo instance.
- The suggestion is a deterministic rule-based heuristic written in pure Python.
- All data used is already in your database (`purchase.order` and `mail.activity` records).

## Assets status (pre-upload)

The screenshots and icon in `static/description/` ship as labelled PLACEHOLDER images during initial publication. Replace them with real screenshots from a running Odoo 19 instance before releasing a polished version.

## License

LGPL-3 — see `LICENSE`.
