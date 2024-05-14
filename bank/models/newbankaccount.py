from odoo import api, fields, models
from odoo.exceptions import ValidationError


class BankAccount(models.Model):
    _name = "bank.account"
    _description = "New bankAccount"

    name = fields.Char(string="Name", help='Name of the account holder')
    account_number = fields.Char(string="Account Number",required=True)
    mobile = fields.Char(string="Mobile", help='Mobile Number of the accountHolder')
    age = fields.Integer(string='Age')
    gender = fields.Selection([('male', 'Male'), ('female', 'Female')], string='Gender')
    Aadhar = fields.Char(String="Aadhar", index=True, help="Aadhar number of the accountHolder")
    account_Type = fields.Selection([('savings', 'Savings'), ('checking', 'Checking')], string='Account Type',
                                    help="Type of bank account", require=True, default='savings')
    balance = fields.Float(string='Balance', default=0.0, readonly=True, help='Current balance of the account')
    Date_opened = fields.Date(string="Date Opened", help='Date when thw account opened')
    image = fields.Binary(string='Image',widget="image")
    completed = fields.Boolean(string='Completed', default=False)
    transaction_ids = fields.One2many('bank.transaction', 'account_id', string="Transactions")
    choose_branch = fields.Many2one('button.model', string="Choose Branch")
    branch = fields.Char(string="Code",related="choose_branch.Branch_Code")
    seq = fields.Integer(string="Sequence")


    #
    # @api.model
    # def create(self, vals):
    #     res = super(BankAccount, self).create(vals)
    #     if 'completed' in vals and vals['completed']:
    #         self.env['recycle.account'].create({
    #             'name': vals.get('name'),
    #             'account_number': vals.get('account_number'),
    #             'mobile': vals.get('mobile'),
    #             'age': vals.get('age'),
    #             'Aadhar': vals.get('Aadhar'),
    #             'gender': vals.get('gender'),
    #             'account_Type': vals.get('account_Type'),
    #             'balance': vals.get('balance', 0.0),  # Assuming balance is a float field
    #             'Date_opened': vals.get('Date_opened'),
    #             'transaction_ids': vals.get('transaction_ids'),
    #             'choose_branch': vals.get('choose_branch')
    #         })
    #     return res

    # _sql_constraints = [
    #     ('unique_name', 'UNIQUE (name)', 'Name must be unique.')
    # ]

    @api.onchange('age')
    def on_change(self):
        if self.age and self.age <= 18:
            raise ValidationError("age must be greater than 18")

    @api.model
    def write(self, vals):
        res = super(BankAccount, self).write(vals)
        return res

    # ONCHANGE METHOD
    @api.onchange('completed')
    def chk_completed(self):
        if self.completed == True:
            recycle_model = self.env['recycle.account'].create({
                'name': self.name,
                'account_number': self.account_number,
                'mobile': self.mobile,
                'age': self.age,
                'Aadhar': self.Aadhar,
                'gender': self.gender,
                'account_Type': self.account_Type

            })
        if self.completed == False:
            print("hi")
            acc_name = self.name
            model_recycle = self.env['recycle.account'].search([('name', '=', acc_name)])

            for rec in model_recycle:
                rec.unlink()
