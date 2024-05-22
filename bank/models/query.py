from odoo import fields, models, api

class QueryBank(models.Model):
    _name = "query.bank"
    _description = "Bank customer"

    name = fields.Char(string="Name", required=True, translate=True)
    account_number = fields.Char(string="Account Number", required=True)
    location = fields.Char(string="Location")
    assets = fields.Integer(string='Assets')
    status = fields.Selection([("done", 'Done'), ("draft", "Draft")], string="Status", default="draft")

    def _select(self):
        return "name, account_number, location, assets, status"

    def _from(self):
        return "customer_bank"

    def _query(self):
        return f"""
            SELECT {self._select()}
            FROM {self._from()}
        """

    @property
    def _table_query(self):
        return self._query()






