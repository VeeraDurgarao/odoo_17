from odoo import fields,models,api
class SalesReports(models.Model):
    _name="reports.customer"

    # amount_untaxed = fields.Monetary(string="Untaxed Amount", store=True, compute='_compute_amounts', tracking=5)
    # amount_tax = fields.Monetary(string="Taxes", store=True, compute='_compute_amounts')
    # amount_total = fields.Monetary(string="Total", store=True, compute='_compute_amounts', tracking=4)
    # amount_to_invoice = fields.Monetary(string="Amount to invoice", store=True, compute='_compute_amount_to_invoice')
    signed_by = fields.Char(
        string="Signed By", copy=False)
    signed_on = fields.Datetime(
        string="Signed On", copy=False)
    origin = fields.Char(
        string="Source Document",
        help="Reference of the document that generated this sales order request")
    reference = fields.Char(
        string="Payment Ref.",
        help="The payment communication of this sale order.",
        copy=False)


    def _select(self):
        return "signed_by,signed_on,origin,reference"

    def _from(self):
        return "sale_order"

    def _query(self):
        return f"""
            SELECT {self._select()}
            FROM {self._from()}
        """

    @property
    def _table_query(self):
        return self._query()