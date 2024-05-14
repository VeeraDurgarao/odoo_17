from odoo import api, fields, models,_
from odoo.exceptions import ValidationError


class BankTransaction(models.Model):
    _name = 'bank.transaction'
    _description = 'Bank Transaction'

    account_number = fields.Char(string="Account Number", required=True)
    date = fields.Date(string='Date', required=True)
    amount = fields.Float(string='Amount', required=True)
    transaction_type = fields.Selection([
        ('deposit', 'Deposit'),
        ('withdraw', 'Withdraw'),
        ('transfer', 'Transfer')
    ], string='Transaction Type', required=True)
    account_id = fields.Many2one('bank.account', string='Account')
    partner_id = fields.Many2one('res.partner', string='Partner')

    listed_property_count = fields.Integer(string='Listed Property Count', compute='_compute_listed_property_count')
    status = fields.Selection([('active', "Active"), ('resign', "Resign")], string="status", readonly=True,
                              default='active')

    def resignation(self):
        for rec in self:
            rec.status = 'resign'

    def revert_to_active(self):
        for rec in self:
            rec.status = 'active'
    def action_property_list(self):
        return {
            'type': 'ir.actions.act_window',
            'name': 'Transaction LIST',
            'res_model': 'bank.transaction',
            'view_mode': 'tree,form',
            'target': 'new',
            'domain': [('account_number', '=', self.account_number)]
        }

    @api.depends('account_number')
    def _compute_listed_property_count(self):
        for record in self:
            listed_property_count = self.env['bank.transaction'].search_count(
                [('account_number', '=', record.account_number)])
            record.listed_property_count = listed_property_count

    @api.model
    def _name_search(self, name='', args=None, operator='ilike', limit=100, name_get_uid=None):
        args = args or []
        if name:
            domain = ['|', '|', ('date', operator, name), ('amount', operator, name),
                      ('transaction_type', operator, name), ('account_id', operator, name)]
            records = self.search(domain + args, limit=limit)
            return records.name_get()
        else:
            return super(BankTransaction, self)._name_search(name=name, args=args, operator=operator, limit=limit,
                                                             name_get_uid=name_get_uid)

    @api.model
    def create(self, vals):
        transaction = super(BankTransaction, self).create(vals)
        print("Transaction>>>>>>>", transaction)
        if vals.get('transaction_type') == 'deposit' and transaction.account_id:
            transaction.account_id.write({'balance': transaction.account_id.balance + vals.get('amount', 0.0)})
        elif vals.get('transaction_type') == 'withdraw' and transaction.account_id:
            transaction.account_id.write({'balance': transaction.account_id.balance - vals.get('amount', 0.0)})
        return transaction

    def write(self, vals):
        for transaction in self:
            if vals.get('transaction_type') == 'deposit' and vals.get('amount'):
                transaction.account_id.write({'balance': transaction.account_id.balance + vals['amount']})
            elif vals.get('transaction_type') == 'withdraw' and vals.get('amount'):
                transaction.account_id.write({'balance': transaction.account_id.balance - vals['amount']})
        return super(BankTransaction, self).write(vals)
