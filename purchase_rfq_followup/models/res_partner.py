from odoo import _, fields, models

PRF_MARKER = "[PRF]"

CONFIRMED_STATES = ("purchase", "done")
PENDING_STATES = ("sent", "to approve")


class ResPartner(models.Model):
    _inherit = "res.partner"

    prf_total_rfqs = fields.Integer(
        string="Total RFQs",
        compute="_compute_prf_stats",
    )
    prf_confirmed_rfqs = fields.Integer(
        string="Confirmed RFQs",
        compute="_compute_prf_stats",
    )
    prf_response_rate = fields.Float(
        string="Response Rate",
        compute="_compute_prf_stats",
        help="Share of RFQs sent to this vendor that became confirmed POs.",
    )
    prf_avg_response_days = fields.Float(
        string="Avg Response (days)",
        compute="_compute_prf_stats",
        help="Average number of days between RFQ creation and PO confirmation "
             "for orders with this vendor.",
    )
    prf_pending_rfqs = fields.Integer(
        string="Pending RFQs",
        compute="_compute_prf_stats",
        help="RFQs sent but not yet confirmed or cancelled.",
    )
    prf_overdue_count = fields.Integer(
        string="Overdue Follow-Ups",
        compute="_compute_prf_stats",
        help="Auto-scheduled follow-up activities whose deadline has passed.",
    )
    prf_smart_suggestion = fields.Char(
        string="Smart Suggestion",
        compute="_compute_prf_suggestion",
        help="Rule-based hint on how to tune follow-up intervals for this vendor "
             "based on their historical response speed. Heuristic only — no AI service.",
    )

    def _compute_prf_stats(self):
        PurchaseOrder = self.env["purchase.order"].sudo()
        Activity = self.env["mail.activity"].sudo()
        model_id = self.env["ir.model"]._get_id("purchase.order")
        today = fields.Date.context_today(self)
        for partner in self:
            if not partner.id or partner.supplier_rank <= 0:
                partner.prf_total_rfqs = 0
                partner.prf_confirmed_rfqs = 0
                partner.prf_response_rate = 0.0
                partner.prf_avg_response_days = 0.0
                partner.prf_pending_rfqs = 0
                partner.prf_overdue_count = 0
                continue
            orders = PurchaseOrder.search([
                ("partner_id", "=", partner.id),
                ("state", "in", PENDING_STATES + CONFIRMED_STATES),
            ])
            total = len(orders)
            confirmed = orders.filtered(lambda o: o.state in CONFIRMED_STATES)
            pending = orders.filtered(lambda o: o.state in PENDING_STATES)

            # avg response days = days from create_date to date_approve
            response_days = []
            for o in confirmed:
                if o.create_date and o.date_approve:
                    delta = (o.date_approve.date() - o.create_date.date()).days
                    if delta >= 0:
                        response_days.append(delta)
            avg = sum(response_days) / len(response_days) if response_days else 0.0

            overdue = Activity.search_count([
                ("res_model_id", "=", model_id),
                ("res_id", "in", pending.ids),
                ("summary", "=like", "%s%%" % PRF_MARKER),
                ("date_deadline", "<", today),
            ]) if pending else 0

            partner.prf_total_rfqs = total
            partner.prf_confirmed_rfqs = len(confirmed)
            partner.prf_response_rate = (
                (len(confirmed) / total) if total else 0.0
            )
            partner.prf_avg_response_days = avg
            partner.prf_pending_rfqs = len(pending)
            partner.prf_overdue_count = overdue

    def _compute_prf_suggestion(self):
        ICP = self.env["ir.config_parameter"].sudo()
        try:
            d2 = int(ICP.get_param("purchase_rfq_followup.days_2", "5"))
            d3 = int(ICP.get_param("purchase_rfq_followup.days_3", "10"))
        except (TypeError, ValueError):
            d2, d3 = 5, 10
        for partner in self:
            avg = partner.prf_avg_response_days
            total = partner.prf_total_rfqs
            if total < 3 or avg <= 0:
                partner.prf_smart_suggestion = ""
                continue
            avg_int = int(round(avg))
            if avg_int < d2:
                partner.prf_smart_suggestion = _(
                    "Responds fast (avg %d days). Consider tighter intervals "
                    "for this vendor."
                ) % avg_int
            elif avg_int > d3:
                partner.prf_smart_suggestion = _(
                    "Responds slow (avg %d days). Suggested intervals: "
                    "%d / %d / %d."
                ) % (avg_int, max(1, avg_int - 2), avg_int + 1, avg_int + 5)
            else:
                partner.prf_smart_suggestion = _(
                    "Matches default schedule (avg %d days)."
                ) % avg_int
