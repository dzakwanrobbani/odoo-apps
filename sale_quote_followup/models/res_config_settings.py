from odoo import _, fields, models
from odoo.exceptions import UserError


class ResConfigSettings(models.TransientModel):
    _inherit = "res.config.settings"

    quotation_followup_auto_enable = fields.Boolean(
        string="Auto-schedule follow-ups",
        config_parameter="sale_quote_followup.auto_enable",
        default=True,
    )
    quotation_followup_days_1 = fields.Integer(
        string="1st follow-up (days)",
        config_parameter="sale_quote_followup.days_1",
        default=2,
    )
    quotation_followup_days_2 = fields.Integer(
        string="2nd follow-up (days)",
        config_parameter="sale_quote_followup.days_2",
        default=5,
    )
    quotation_followup_days_3 = fields.Integer(
        string="3rd follow-up (days)",
        config_parameter="sale_quote_followup.days_3",
        default=10,
    )
    quotation_followup_activity_type_id = fields.Many2one(
        "mail.activity.type",
        string="Follow-up activity type",
        config_parameter="sale_quote_followup.activity_type_id",
    )

    def set_values(self):
        for record in self:
            d1 = record.quotation_followup_days_1
            d2 = record.quotation_followup_days_2
            d3 = record.quotation_followup_days_3
            if not (0 < d1 < d2 < d3):
                raise UserError(_(
                    "Follow-up intervals must be positive and strictly "
                    "increasing (for example 2 < 5 < 10)."
                ))
        return super().set_values()
