from odoo import fields, models, api, _
from odoo.exceptions import ValidationError


class BankCustomer(models.Model):
    _name = "customer.bank"
    _description = "Bank customer"
    # _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char(string="Name", required=True, translate=True)
    account_number = fields.Char(string="Account Number", required=True)
    location = fields.Char(string="location")
    assets = fields.Integer(string='assets')
    # assigned_emp = fields.Many2one('employee.bank', string="Assigned employee")
    Loans_List = fields.Many2many(comodel_name='bank.loan', string='Loans List', domain=[('duration', '>', '12')])
    image = fields.Binary(string='Image')
    status = fields.Selection([("done", 'Done'), ("draft", "Draft")], string="Status", default="draft")

    @api.constrains('account_number')
    def check_number(self):
        existing_account = self.env['bank.account'].search([('account_number', '=', self.account_number)])
        if not existing_account:
            raise ValidationError("Please create new account.")
    @api.model
    # ORM CREATE METHOD
    def create(self, vals):
        field_info = self.env['bank.loan'].fields_get(['name', 'description'])
        print(">>>>>>>>>>>>>>>>>>>>", field_info)
        res = super(BankCustomer, self).create(vals)
        print("Create the values>>>>>>>>>>>", vals)
        return res

    #
    #     # ORM write method
    #
    #     def write(self,vals):
    #         res = super(BankCustomer,self).write(vals)
    #         res1 = self.search([('name', '=', self.name)])
    #         res2 = self.search_count([('name', '=', self.name)])
    #         names_in_uppercase = res1.mapped(lambda rec: rec.name.upper())
    #         print("Changes in the customer list>>>>>>>>>>>>>>>",vals)
    #         print("Search values is>>>>>>>>", res1,res1.name)
    #         print("Search count is>>>>>>>>>>", res2)
    #         print("Mapped function>>>>>>>>>>>",names_in_uppercase)
    #         return res,res1,res2,names_in_uppercase
    #
    #
    # # ORM UNLINK/DELETE METHOD
    #     def unlink(self):
    #         for record in self:
    #             print("Deleted item is:", record.name)
    #         return super(BankCustomer, self).unlink()
    #
    #
    # # ORM Read method
    # #     @api.model
    # #     def read(self, fields=None, load='_classic_read'):
    # #         for i in self:
    # #             print("Read records '{}'".format(i.name))
    # #         return super(BankCustomer, self).read(fields=fields, load=load)
    #
    #
    #     # ORM UNLINK/DELETE METHOD

    def unlink(self):
        # if self.status == 'done':
        #     raise ValidationError("You cannot delete odoo domain")
        self.ensure_one()
        res = super(BankCustomer, self).unlink()
        return res

    #     # ORM COPY METHOD

    def copy(self, default=None):
        self.ensure_one()
        if self.status == 'done':
            raise ValidationError("You cannot duplicate the record")
        res = super().copy(default)
        return res
