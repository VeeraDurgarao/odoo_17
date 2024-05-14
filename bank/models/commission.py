from odoo import models,fields,api

class Commission(models.Model):
    _name = 'commission.model'


    start_date = fields.Date(string="Start Date")
    end_date = fields.Date(string="End Date")
    order_Number=fields.Char(string="Order Number")
    customer=fields.Many2one('res.users',string="Customer Name")

    list = fields.Many2many('sale.order',string="List",compute="_compute_order_list")

    @api.depends('start_date','end_date')
    def _compute_order_list(self):
        for record in self:
            if record.start_date and record.end_date and record.customer.name:
                print(record.customer.name)
                domain = [('date_order', '>=', record.start_date), ('date_order', '<=', record.end_date), ('user_id', '=', record.customer.name)]
                orders = self.env['sale.order'].search(domain)
                record.list = [(6, 0, orders.ids)]
            else:
                record.list = False

    def action_show_matching_orders(self):
        pass


    # def action_show_matching_orders(self):
    #     self.ensure_one()
    #     domain = [('date_order', '>=', self.start_date), ('date_order', '<=', self.end_date)]
    #     matching_orders = self.env['sale.order'].search(domain)
    #     self.list = [(6, 0, matching_orders.ids)]  # Update the list field with matching order ids
    #
    #     return {
    #         'name': 'Matching Orders',
    #         'type': 'ir.actions.act_window',
    #         'res_model': 'sale.order',
    #         'view_mode': 'tree,form',
    #         'domain': domain,
    #     }


