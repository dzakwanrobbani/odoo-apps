=====================
Sales Quote Follow-Up
=====================

Auto-schedules three follow-up activities the moment an Odoo quotation is sent.
Pending follow-ups auto-close when the order is confirmed or cancelled.
Zero setup, works out of the box.

Features
========

- Auto-creates 3 follow-up activities on quotation send (default day +2, +5, +10).
- Auto-closes pending follow-ups when the order is confirmed or cancelled.
- Per-database configuration under **Settings > Sales > Quotations**.
- Manual **Schedule Follow-Ups** button on the quotation form.
- LGPL-3, no external dependencies.

How it works
============

When a user clicks **Send by Email** on a quotation, three ``mail.activity``
records are scheduled on the order at day +N1, +N2 and +N3 (default
2 / 5 / 10). Activities are tagged with the ``[SQF]`` marker in their summary
so they can be identified and cleaned up later. When the order is confirmed
or cancelled, every ``[SQF]``-marked activity on that order is closed with a
corresponding feedback message.

The **Schedule Follow-Ups** button on the form replaces any existing auto
follow-ups, making it idempotent.

Configuration
=============

Open **Settings > Sales > Quotations** and locate the *Auto Follow-Up on Sent
Quotations* section. Intervals must be positive and strictly increasing.
The settings page validates this on save.

Compatibility
=============

- Odoo 19.0 Community and Enterprise.
- Requires at least one ``mail.activity.type`` to exist.

License
=======

LGPL-3.
