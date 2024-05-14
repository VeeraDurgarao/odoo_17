from odoo import api, fields, models


class Loan(models.Model):
    _name = 'bank.loan'
    _description = "loan Bank"

    name = fields.Char(string="Name")
    amount = fields.Float(string="Loan Amount", required=True)
    interest_rate = fields.Float(string='Interest Rate', required=True)
    duration = fields.Integer(string='Duration (months)', required=True)
    total_interest = fields.Float(string="Total Amount", compute="total_interest1", store=True)

    # account_id = fields.Many2one('bank.account', string="Bank Account")

    # bY USING COMPUTE METHOD IT IS AUTOMATICALLY CALCULATE THE TOTAL INTEREST WITH AMOUNT
    @api.depends('amount', 'interest_rate', 'duration')
    def total_interest1(self):
        for loan in self:
            loan.total_interest = (loan.amount * loan.duration * loan.interest_rate) / 100

    @api.model
    def write(self, vals):
        self.ensure_one()
        res = super(Loan, self).write(vals)
        print("Changed values is>>>>>>>>>>>>>>", vals)
        return res
