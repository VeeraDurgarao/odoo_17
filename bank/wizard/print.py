
from odoo import fields, models


class Print(models.TransientModel):
    _name = "print.wizard"

    order_id = fields.Many2one('sale.order')
    order_line = fields.Many2many('sale.order.line')

    def submit(self):
        print(" order _idf >>>>>>>>>>>", self.order_id)
        print(" selected order line <<<<<<<<<<<<<", self.order_line)
        order_line_ids = self.order_line.mapped('id')
        for line in self.order_line:
            print(" line >>>>>>>>>>>>>>>>>>>>", line)
        return self.env.ref('sale.action_report_saleorder').with_context(my_report=True, order_lines=order_line_ids).report_action(
            self.order_id)
        # return self.env.ref().with_context()
        # pass

