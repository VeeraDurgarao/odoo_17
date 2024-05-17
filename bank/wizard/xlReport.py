from odoo import fields, models,api
import io
import xlsxwriter
import xlrd
import base64

from odoo.exceptions import ValidationError


class Print(models.TransientModel):
    _name = "xlreport.wizard"

    start_date = fields.Date(string="Start Date")
    end_date = fields.Date(string="End Date")



    def submit(self):
        start = self.start_date
        end=self.end_date
        if start > end:
            raise ValidationError("The start date cannot be later than the end date.")

        output = io.BytesIO()
        workbook = xlsxwriter.Workbook(output)
        sheet = workbook.add_worksheet('Transactions')

        bold_format = workbook.add_format({
            'bold': 600,
            'align': 'center',
            'valign':'center',
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
        dollar_format = workbook.add_format({'num_format': '$#,##0.00',"font_size": 10})
        sheet.set_column('A:I', 15)  # Adjust the width as needed
        sheet.set_default_row(25)  # Adjust the height as needed


        sheet.write('A1', 'Number', bold_format)
        sheet.write('B1', 'Date', bold_format)
        sheet.write('C1',"Expire Date",bold_format)
        sheet.write('D1', 'Status', bold_format)
        sheet.write('E1',"Invoice Statue",bold_format)
        sheet.write('F1', 'Sale Team', bold_format)
        sheet.write('G1', 'Name', bold_format)
        sheet.write('H1', 'Company', bold_format)
        sheet.write('I1', 'Tags', bold_format)
        sheet.write('J1', 'UnTaxes', bold_format)
        sheet.write('K1', 'Taxes', bold_format)
        sheet.write('L1', 'Total', bold_format)

        col = 0
        row = 1
        data = self.env['sale.order'].search([('date_order', '>=', start),('date_order','<=',end)])

        for rec in data:
            sheet.write(row, col, rec.name or '', normal_format)
            sheet.write(row, col+1, rec.date_order.strftime('%Y-%m-%d') if rec.date_order else '', date_format)
            sheet.write(row, col + 2, rec.validity_date.strftime('%Y-%m-%d') if rec.date_order else '', date_format)
            sheet.write(row, col+3, rec.state or '', normal_format)
            sheet.write(row, col +4, rec.invoice_status or '', normal_format)

            sheet.write(row, col+5, rec.team_id.name or 0.0, text_format)
            sheet.write(row, col+6, rec.user_id.name or 'NA', text_format)
            sheet.write(row, col+7, rec.partner_id.name or 'NA', text_format)

            tag_names = ', '.join(rec.tag_ids.mapped('name'))
            sheet.write(row, col+8, tag_names or 'NA', normal_format)
            sheet.write(row, col+9, rec.amount_untaxed or 'NA', dollar_format)
            sheet.write(row, col+10, rec.amount_tax or 'NA', dollar_format)
            sheet.write(row, col+11, rec.amount_total or 'NA',dollar_format)
            row += 1

        workbook.close()
        output.seek(0)

        # Encode the file to base64
        excel_file = base64.b64encode(output.read())
        output.close()

        # Create an attachment
        attachment = self.env['ir.attachment'].create({
            'name': f'Sale_report.xlsx',
            'type': 'binary',
            'datas': excel_file,
            'res_model': 'sale.order',
            'res_id': self.id,
            'mimetype': 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
        })

        return {
            'type': 'ir.actions.act_url',
            'url': f'/web/content/{attachment.id}?download=true',
            'target': 'self',
        }
