from odoo import fields, models, api
import io
import xlsxwriter
import base64
from odoo.exceptions import ValidationError

class Print(models.TransientModel):
    _name = "xlreport.wizard"

    start_date = fields.Date(string="Start Date")
    end_date = fields.Date(string="End Date")

    def submit(self):
        start = self.start_date
        end = self.end_date
        if start > end:
            raise ValidationError("The start date cannot be later than the end date.")

        output = io.BytesIO()
        workbook = xlsxwriter.Workbook(output)
        sheet = workbook.add_worksheet('Transactions')

        bold_format = workbook.add_format({
            'bold': True,
            'align': 'center',
            'valign': 'center',
            'font_size': 11,
            'bg_color': '#FFA500',
            'border': True
        })
        normal_format = workbook.add_format({
            'text_wrap': True,
            'valign': 'center',
            'align': 'center',
            'font_size': 10
        })
        number_format = workbook.add_format({
            'text_wrap': True,
            'align': 'right',
            'font_size': 9
        })
        text_format = workbook.add_format({
            'text_wrap': True,
            'align': 'left',
            'font_size': 10
        })
        date_format = workbook.add_format({
            'num_format': 'dd/mm/yy',
            'align': 'center',
            'font_size': 10
        })
        dollar_format = workbook.add_format({'num_format': '$#,##0.00', "font_size": 10})
        sheet.set_column('A:L', 15)  # Adjust the width as needed
        sheet.set_default_row(25)  # Adjust the height as needed

        sheet.write('A1', 'Number', bold_format)
        sheet.write('B1', 'Date', bold_format)
        sheet.write('C1', "Expire Date", bold_format)
        sheet.write('D1', 'Status', bold_format)
        sheet.write('E1', "Invoice Status", bold_format)
        sheet.write('F1', 'Sale Team', bold_format)
        sheet.write('G1', 'Name', bold_format)
        sheet.write('H1', 'Company', bold_format)
        sheet.write('I1', 'Tags', bold_format)
        sheet.write('J1', 'UnTaxes', bold_format)
        sheet.write('K1', 'Taxes', bold_format)
        sheet.write('L1', 'Total', bold_format)

        col = 0
        row = 1
        data = self.env['sale.order'].search([('date_order', '>=', start), ('date_order', '<=', end)])

        for rec in data:
            sheet.write(row, col, rec.name or '', normal_format)
            sheet.write(row, col + 1, rec.date_order.strftime('%Y-%m-%d') if rec.date_order else '', date_format)
            sheet.write(row, col + 2, rec.validity_date.strftime('%Y-%m-%d') if rec.validity_date else '', date_format)
            sheet.write(row, col + 3, rec.state or '', normal_format)
            sheet.write(row, col + 4, rec.invoice_status or '', normal_format)
            sheet.write(row, col + 5, rec.team_id.name or 'NA', text_format)
            sheet.write(row, col + 6, rec.user_id.name or 'NA', text_format)
            sheet.write(row, col + 7, rec.partner_id.name or 'NA', text_format)

            tag_names = ', '.join(rec.tag_ids.mapped('name'))
            sheet.write(row, col + 8, tag_names or 'NA', normal_format)
            sheet.write(row, col + 9, rec.amount_untaxed or 0.0, dollar_format)
            sheet.write(row, col + 10, rec.amount_tax or 0.0, dollar_format)
            sheet.write(row, col + 11, rec.amount_total or 0.0, dollar_format)
            row += 1

            # query_fet = (
            #     "SELECT "
            #     "so.partner_id, "
            #     "rp.name AS partner_name, "
            #     "COUNT(so.id) AS order_count, "
            #     "SUM(so.amount_untaxed) AS total_amount_untaxed, "
            #     "SUM(so.amount_tax) AS total_amount_tax, "
            #     "SUM(so.amount_total) AS total_amount_total, "
            #     "SUM(so.amount_to_invoice) AS total_amount_to_invoice "
            #     "FROM sale_order so "
            #     "JOIN res_partner rp ON so.partner_id = rp.id "
            #     "WHERE so.date_order BETWEEN %s AND %s "
            #     "GROUP BY so.partner_id, rp.name"
            # )
            #
            # params = (self.start_date.strftime('%Y-%m-%d'), self.end_date.strftime('%Y-%m-%d'))
            # self.env.cr.execute(query_fet, params)
            # result_data = self.env.cr.fetchall()

        workbook.close()
        output.seek(0)

        # Encode the file to base64
        excel_file = base64.b64encode(output.read())
        output.close()

        # Create an attachment
        attachment = self.env['ir.attachment'].create({
            'name': 'Sale_report.xlsx',
            'type': 'binary',
            'datas': excel_file,
            'res_model': 'xlreport.wizard',
            'res_id': self.id,
            'mimetype': 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
        })

        download_url = f'/web/content/{attachment.id}?download=true'
        return {
            'type': 'ir.actions.act_url',
            'url': download_url,
            'target': 'self',
        }
