from odoo import models, fields, api

class CommissionLine(models.Model):
    _name = "commissionorder.line"

    name = fields.Char(string="Name")
    partner_id = fields.Many2one('res.partner', string="Order Reference")
    user_id = fields.Many2one('res.partner', string="Customer Name")
    amount_total = fields.Float(string="Total")
    commission = fields.Float(string="Commission")
    order_no = fields.Char(string="Order No")
    create_date = fields.Date(string="Create Date")

class Partner(models.Model):
    _inherit = "res.partner"

    commission = fields.Float(string="Commission")
    percentage = fields.Float(string="Percentage")