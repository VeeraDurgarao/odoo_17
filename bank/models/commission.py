import io
import xlsxwriter
import xlrd
import base64
from odoo import models,fields,api

class Commission(models.Model):
    _name = 'commission.model'


    start_date = fields.Date(string="Start Date")
    end_date = fields.Date(string="End Date")
    order_Number=fields.Char(string="Order Number")
    customer=fields.Many2one('res.users',string="Customer Name")

    list = fields.Many2many('sale.order',string="List",compute="_compute_order_list")

    @api.model
    def get_custom_data(self,params):
        query = """
               SELECT customer
               FROM commission_model 
           """
        params = (10,)
        print(">>>>>>>>>>>>>>>>>>>>>>>>>",self.env.cr.execute(query, params))
        self.env.cr.execute(query, params)
        print("++++++++++++++++++++",self.env.cr.fetchall())
        return self.env.cr.fetchall()

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

    def get_data(self):
        domain = [('write_date', '>=', self.start_date), ('write_date', '<=', self.end_date),  ('user_id', '=', self.customer.name)]
        return self.env['sale.order'].search(domain)

    def generates_excel_report(self):
        output = io.BytesIO()
        workbook = xlsxwriter.Workbook(output)
        sheet = workbook.add_worksheet('Transactions')

        bold_format = workbook.add_format(
            {'bold': True, 'align': 'center', 'font_size': 12, 'bg_color': '#FFA500',
             'border': True})
        normal_format = workbook.add_format({'text_wrap': True, 'align': 'center','font_size': 10})
        number_format = workbook.add_format({'text_wrap': True, 'align': 'right','font_size': 10})
        text_formate = workbook.add_format({'text_wrap': True, 'align': 'left','font_size': 10})
        date_format = workbook.add_format({'num_format': 'dd/mm/yy', 'align': 'center','font_size': 10})
        sheet.set_column('A:I', 12)  # Adjust the width as needed
        # Set row height
        sheet.set_default_row(25)  # Adjust the height as needed
        row = 1
        col = 0
        data = self.get_data()
        # record = self.env['sale.order'].browse(data)

        # Write headers with bold format
        sheet.write('A1', 'Number', bold_format)
        sheet.write('B1', 'Date', bold_format)
        sheet.write('C1', 'Status', bold_format)
        sheet.write('D1', 'Total', bold_format)
        sheet.write('E1', 'Name', bold_format)
        sheet.write('F1', 'Partner', bold_format)
        sheet.write('G1', 'Company', bold_format)
        sheet.write('H1', 'Tags', bold_format)
        sheet.write('I1', 'Sale Team', bold_format)

        # row += 1
        for rec in data:
            sheet.write(row, col, rec.name or '', normal_format)  # Changed rec.name to rec.name or '' to avoid NoneType error
            sheet.write(row, col + 1, rec.date_order.strftime('%Y-%m-%d') if rec.date_order else '', date_format)
            sheet.write(row, col + 2, rec.state or '', normal_format)
            sheet.write(row, col + 3, rec.amount_total or 0.0, number_format)
            sheet.write(row, col+4, rec.user_id.name or 'NA', text_formate)
            sheet.write(row, col + 5, rec.partner_id.name or 'NA', text_formate)
            sheet.write(row, col + 6, rec.company_id.name or 'NA', text_formate)
            sheet.write(row, col + 7, rec.tag_ids.name or 'NA', normal_format)
            sheet.write(row, col + 8, rec.team_id.name or 'NA', text_formate)

            row += 1

        workbook.close()
        output.seek(0)

        # Encode the file to base64
        excel_file = base64.b64encode(output.read())
        output.close()

        # Create an attachment
        attachment = self.env['ir.attachment'].create({
            'name': f'{self.customer.name}_report.xlsx',  # Changed from f'{self.name}_report.xlsx'
            'type': 'binary',
            'datas': excel_file,
            'res_model': 'commission.model',
            'res_id': self.id,
            'mimetype': 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
        })

        return {
            'type': 'ir.actions.act_url',
            'url': f'/web/content/{attachment.id}?download=true',
            'target': 'self',
        }


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


