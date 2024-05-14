from odoo import fields, models, api, _


class BankEmployee(models.Model):
    _name = "employee.bank"
    _description = "employee bank"
    _noupdate = True

    name = fields.Char(string="Name")
    emp_id = fields.Integer(string="Emp_id")
    # assigned_cus_ids = fields.One2many('customer.bank','assigned_emp', string="Assigned Customer")
    assigned_cus_ids = fields.Many2many('customer.bank', string="Assigned Customer")




    # ORM METHODS WRITE,SEARCH,BROWSE
    @api.model
    def write(self, vals):
        res = super(BankEmployee, self).write(vals)
        res1 = self.browse([self.emp_id])
        res2 = self.search([('name', '=', self.name)])
        res3 = self.search_count([('name', '=', self.name)])
        print("Browse values is>>>>>>>>>>>>>>>>>", res1)
        print("Search values is>>>>>>>>>>>>>>>>>", res2, res2.name)
        print("Changed values is>>>>>>>>>>>>>>>>", vals)
        print("Search count is>>>>>>.", res3)

        return res, res1, res2, res3
