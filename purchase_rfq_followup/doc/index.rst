======================
Purchase RFQ Follow-Up
======================

Auto-schedules three internal follow-up activities the moment a Purchase RFQ
is sent to a vendor in Odoo 19. Pending follow-ups auto-close when the order
is confirmed or cancelled. Includes a per-vendor insight dashboard with
rule-based suggestions.

Features
========

- Auto-creates 3 follow-up activities on RFQ send (default day +2, +5, +10).
- Auto-closes pending follow-ups when the PO is confirmed or cancelled.
- Per-database configuration under **Settings > Purchase**.
- Manual **Schedule Follow-Ups** button on the RFQ form.
- **RFQ Follow-Up Insights dashboard** under **Purchase > Reporting**.
- Rule-based smart suggestion per vendor based on their historical response time.
- LGPL-3, no external dependencies, no external AI service.

How it works
============

When a user clicks **Send by Email** on an RFQ, three ``mail.activity``
records are scheduled on the order at day +N1, +N2 and +N3 (default
2 / 5 / 10). Activities are tagged with the ``[PRF]`` marker in their summary
so they can be identified and cleaned up later. When the order is confirmed
or cancelled, every ``[PRF]``-marked activity on that order is closed with a
corresponding feedback message.

The dashboard reads existing ``purchase.order`` and ``mail.activity`` records
and computes per-vendor metrics plus a rule-based smart suggestion. No
external service is called.

Configuration
=============

Open **Settings > Purchase** and locate *Auto Follow-Up on Sent RFQ*.
Intervals must be positive and strictly increasing. The settings page
validates this on save.

Compatibility
=============

- Odoo 19.0 Community and Enterprise.
- Requires at least one ``mail.activity.type`` to exist.

License
=======

LGPL-3.
