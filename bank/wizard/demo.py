from odoo import fields, models


class Demo(models.TransientModel):
    _name = "demo.demo"

    help = fields.Char(string="Help", help="what you want")
    Report_issue = fields.Text(string="Report", help="what is your problem")

    def submit(self):
        pass
