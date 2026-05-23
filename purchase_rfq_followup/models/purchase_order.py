import logging
from datetime import timedelta

from odoo import _, fields, models
from odoo.exceptions import UserError

_logger = logging.getLogger(__name__)

PRF_MARKER = "[PRF]"


class PurchaseOrder(models.Model):
    _inherit = "purchase.order"

    def action_rfq_send(self):
        result = super().action_rfq_send()
        for order in self:
            if order._prf_auto_enabled() and order.state in ("draft", "sent"):
                try:
                    order.action_schedule_followups()
                except Exception as exc:
                    _logger.warning(
                        "purchase_rfq_followup: failed to schedule "
                        "follow-ups for %s: %s", order.name, exc,
                    )
        return result

    def button_confirm(self):
        result = super().button_confirm()
        self._close_rfq_followups(_("Order confirmed"))
        return result

    def button_cancel(self):
        result = super().button_cancel()
        self._close_rfq_followups(_("Order cancelled"))
        return result

    def action_schedule_followups(self):
        self.ensure_one()
        if self.state not in ("draft", "sent", "to approve"):
            raise UserError(_(
                "Follow-ups can only be scheduled on draft, sent or "
                "to-approve RFQs."
            ))
        intervals = self._prf_intervals()
        if not intervals:
            return False
        activity_type = self._prf_activity_type()
        if not activity_type:
            _logger.info(
                "purchase_rfq_followup: no mail.activity.type available, "
                "skipping scheduling for %s", self.name,
            )
            return False

        self._prf_clear_pending()

        Activity = self.env["mail.activity"].sudo()
        model_id = self.env["ir.model"]._get_id("purchase.order")
        responsible = self.user_id or self.env.user
        today = fields.Date.context_today(self)

        for days in intervals:
            Activity.create({
                "res_model_id": model_id,
                "res_model": "purchase.order",
                "res_id": self.id,
                "activity_type_id": activity_type.id,
                "date_deadline": today + timedelta(days=days),
                "summary": "%s Follow-up %s (day +%d)" % (
                    PRF_MARKER, self.name, days,
                ),
                "note": _(
                    "Auto-scheduled by Purchase RFQ Follow-Up module."
                ),
                "user_id": responsible.id,
            })
        return True

    def _close_rfq_followups(self, feedback):
        if not self:
            return False
        Activity = self.env["mail.activity"].sudo()
        model_id = self.env["ir.model"]._get_id("purchase.order")
        activities = Activity.search([
            ("res_model_id", "=", model_id),
            ("res_id", "in", self.ids),
            ("summary", "=like", "%s%%" % PRF_MARKER),
        ])
        for act in activities:
            try:
                act.action_feedback(feedback=feedback)
            except Exception as exc:
                _logger.warning(
                    "purchase_rfq_followup: failed to close activity %s: %s",
                    act.id, exc,
                )
                act.unlink()
        return True

    def _prf_clear_pending(self):
        self.ensure_one()
        Activity = self.env["mail.activity"].sudo()
        model_id = self.env["ir.model"]._get_id("purchase.order")
        Activity.search([
            ("res_model_id", "=", model_id),
            ("res_id", "=", self.id),
            ("summary", "=like", "%s%%" % PRF_MARKER),
        ]).unlink()

    def _prf_auto_enabled(self):
        param = self.env["ir.config_parameter"].sudo().get_param(
            "purchase_rfq_followup.auto_enable", "True",
        )
        return str(param).lower() in ("true", "1", "yes")

    def _prf_intervals(self):
        ICP = self.env["ir.config_parameter"].sudo()
        try:
            d1 = int(ICP.get_param("purchase_rfq_followup.days_1", "2"))
            d2 = int(ICP.get_param("purchase_rfq_followup.days_2", "5"))
            d3 = int(ICP.get_param("purchase_rfq_followup.days_3", "10"))
        except (TypeError, ValueError):
            d1, d2, d3 = 2, 5, 10
        return [d for d in (d1, d2, d3) if d > 0]

    def _prf_activity_type(self):
        ICP = self.env["ir.config_parameter"].sudo()
        type_id = ICP.get_param("purchase_rfq_followup.activity_type_id")
        if type_id:
            try:
                act = self.env["mail.activity.type"].browse(
                    int(type_id)
                ).exists()
                if act:
                    return act
            except (TypeError, ValueError):
                pass
        fallback = self.env.ref(
            "mail.mail_activity_data_call", raise_if_not_found=False,
        )
        if fallback:
            return fallback
        return self.env["mail.activity.type"].search([], limit=1)
