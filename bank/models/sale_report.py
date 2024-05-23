import base64
import io
from datetime import date, datetime, timedelta

import xlsxwriter

from odoo import fields,models,api
class SalesReports(models.Model):
    _name="reports.customer"

    # amount_untaxed = fields.Monetary(string="Untaxed Amount", store=True, compute='_compute_amounts', tracking=5)
    # amount_tax = fields.Monetary(string="Taxes", store=True, compute='_compute_amounts')
    # amount_total = fields.Monetary(string="Total", store=True, compute='_compute_amounts', tracking=4)
    # amount_to_invoice = fields.Monetary(string="Amount to invoice", store=True, compute='_compute_amount_to_invoice')
    signed_by = fields.Char(
        string="Signed By", copy=False)
    signed_on = fields.Datetime(
        string="Signed On", copy=False)
    origin = fields.Char(
        string="Source Document",
        help="Reference of the document that generated this sales order request")
    reference = fields.Char(
        string="Payment Ref.",
        help="The payment communication of this sale order.",
        copy=False)


    def _select(self):
        return "signed_by,signed_on,origin,reference"

    def _from(self):
        return "sale_order"

    def _query(self):
        return f"""
            SELECT {self._select()}
            FROM {self._from()}
        """

    @property
    def _table_query(self):
        return self._query()

class reportMonthly(models.Model):
    _inherit = "sale.order"

    def generates_customer_report(self):
        output = io.BytesIO()
        workbook = xlsxwriter.Workbook(output)
        sheet = workbook.add_worksheet('Transactions')
        admin = self.env.user.name
        mail = self.env.user.email
        today_date = datetime.today()
        last_month_date = today_date-timedelta(days=today_date.day)

        bold_format = workbook.add_format(
            {'bold': True, 'align': 'center', 'font_size': 12, 'bg_color': '#FFA500',
             'border': True})
        normal_format = workbook.add_format({'text_wrap': True, 'align': 'center', 'font_size': 10})
        number_format = workbook.add_format({'text_wrap': True, 'align': 'right', 'font_size': 10})
        text_formate = workbook.add_format({'text_wrap': True, 'align': 'left', 'font_size': 10})
        date_format = workbook.add_format({'num_format': 'dd/mm/yy', 'align': 'center', 'font_size': 10})
        sheet.set_column('A:I', 12)  # Adjust the width as needed
        # Set row height
        sheet.set_default_row(25)  # Adjust the height as needed
        row = 1
        col = 0
        data = self.search([('user_id', '=', admin),('date_order', '>=',last_month_date),('date_order', '<=',today_date)])
        # record = self.env['sale.order'].browse(data)

        # Write headers with bold format
        sheet.write('A1', 'Number', bold_format)
        sheet.write('B1', 'Date', bold_format)
        sheet.write('C1', 'Status', bold_format)
        sheet.write('D1', 'Total', bold_format)
        sheet.write('E1', 'Name', bold_format)
        sheet.write('F1', 'Partner', bold_format)
        sheet.write('G1', 'Company', bold_format)
        # sheet.write('H1', 'Tags', bold_format)
        sheet.write('H1', 'Sale Team', bold_format)

        # row += 1
        for rec in data:
            sheet.write(row, col, rec.name or '',
                        normal_format)  # Changed rec.name to rec.name or '' to avoid NoneType error
            sheet.write(row, col + 1, rec.date_order.strftime('%Y-%m-%d') if rec.date_order else '', date_format)
            sheet.write(row, col + 2, rec.state or '', normal_format)
            sheet.write(row, col + 3, rec.amount_total or 0.0, number_format)
            sheet.write(row, col + 4, rec.user_id.name or 'NA', text_formate)
            sheet.write(row, col + 5, rec.partner_id.name or 'NA', text_formate)
            sheet.write(row, col + 6, rec.company_id.name or 'NA', text_formate)
            # sheet.write(row, col + 7, rec.tag_ids.name or 'NA', normal_format)
            sheet.write(row, col + 7, rec.team_id.name or 'NA', text_formate)

            row += 1

        workbook.close()
        output.seek(0)

        # Encode the file to base64
        excel_file = base64.b64encode(output.read())
        output.close()

        # Create an attachment
        attachment = self.env['ir.attachment'].create({
            'name': f'{self.name}_report.xlsx',  # Changed from f'{self.name}_report.xlsx'
            'type': 'binary',
            'datas': excel_file,
            'res_model': 'sale.order',
            'res_id': self.id,
            'mimetype': 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
        })

        email_values = {
            'email_from':'durgarao@mail.com',
            'email_to': f'{mail}',
            'subject': f"Report from",
            'attachment_ids': [(6, 0, [attachment.id])]
        }

        # Send a single email with the report attachment to all recipients
        mail_template = self.env.ref('bank.mail_monthly_report_template')
        mail_template.send_mail(self.env.user.id, email_values=email_values, force_send=True)

        return {
            'type': 'ir.actions.act_url',
            'url': f'/web/content/{attachment.id}?download=true',
            'target': 'self',
        }

