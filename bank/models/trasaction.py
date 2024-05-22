import xlsxwriter
import base64
import io
from odoo import api, fields, models, _
from odoo.exceptions import ValidationError


class BankTransaction(models.Model):
    _name = 'bank.transaction'
    _description = 'Bank Transaction'

    account_number = fields.Char(string="Account Number", required=True)
    date = fields.Date(string='Date', required=True)
    amount = fields.Float(string='Amount', required=True)
    transaction_type = fields.Selection([
        ('deposit', 'Deposit'),
        ('withdraw', 'Withdraw'),
        ('transfer', 'Transfer')
    ], string='Transaction Type', required=True)
    account_id = fields.Many2one('bank.account', string='Account')
    partner_id = fields.Many2one('res.partner', string='Partner')
    email = fields.Char(string="mail")
    name = fields.Char(string="name")
    mobile = fields.Char(string="mobile")

    listed_property_count = fields.Integer(string='Listed Property Count', compute='_compute_listed_property_count')

    # status = fields.Selection([('active', "Active"), ('resign', "Resign")], string="status", readonly=True,
    #                           default='active')
    def _get_customer_information(self):
        # Implement the logic to retrieve customer information here
        return {'name': self.name, 'email': self.email, 'mobile': self.mobile}

    def generate_excel_report(self):
        output = io.BytesIO()
        workbook = xlsxwriter.Workbook(output)
        sheet = workbook.add_worksheet('Transactions')

        bold_format = workbook.add_format(
            {'bold': True, 'align': 'center', 'font_size': 10, 'valign': 'vcenter', 'bg_color': '#f2eee4',
             'border': True})
        normal_format = workbook.add_format({'text_wrap': True, 'align': 'center', 'valign': 'top'})
        date_format = workbook.add_format({'num_format': 'dd/mm/yy', 'align': 'center'})
        sheet.set_column('A:G', 15)  # Adjust the width as needed
        # Set row height
        sheet.set_default_row(30)  # Adjust the height as needed
        row = 1
        col = 0

        # Write headers with bold format
        sheet.write('A1', 'Account Number', bold_format)
        sheet.write('B1', 'Date', bold_format)
        sheet.write('C1', 'Amount', bold_format)
        sheet.write('D1', 'Transaction Type', bold_format)
        sheet.write('E1', 'Email', bold_format)
        sheet.write('F1', 'Name', bold_format)
        sheet.write('G1', 'Mobile', bold_format)

        sheet.write(row, col, self.account_number, normal_format)
        sheet.write(row, col + 1, self.date, date_format)
        sheet.write(row, col + 2, self.amount, normal_format)
        sheet.write(row, col + 3, self.transaction_type, normal_format)
        sheet.write(row, col + 4, self.email, normal_format)
        sheet.write(row, col + 5, self.name, normal_format)
        sheet.write(row, col + 6, self.mobile, normal_format)

        workbook.close()
        output.seek(0)

        # Encode the file to base64
        excel_file = base64.b64encode(output.read())
        output.close()

        # Create an attachment
        attachment = self.env['ir.attachment'].create({
            'name': f'{self.name}_report.xlsx',
            'type': 'binary',
            'datas': excel_file,
            'res_model': 'bank.transaction',
            'res_id': self.id,
            'mimetype': 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
        })

        return {
            'type': 'ir.actions.act_url',
            'url': f'/web/content/{attachment.id}?download=true',
            'target': 'self',
        }

    def resignation(self):
        for rec in self:
            rec.transaction_type = 'deposit'

    def revert_to_active(self):
        for rec in self:
            rec.transaction_type = 'withdraw'

    def action_property_list(self):
        return {
            'type': 'ir.actions.act_window',
            'name': 'Transaction LIST',
            'res_model': 'bank.transaction',
            'view_mode': 'tree,form',
            'target': 'new',
            'domain': [('account_number', '=', self.account_number)]
        }

    @api.depends('account_number')
    def _compute_listed_property_count(self):
        for record in self:
            listed_property_count = self.env['bank.transaction'].search_count(
                [('account_number', '=', record.account_number)])
            record.listed_property_count = listed_property_count

    @api.model
    def _name_search(self, name='', args=None, operator='ilike', limit=100, name_get_uid=None):
        args = args or []
        if name:
            domain = ['|', '|', ('date', operator, name), ('amount', operator, name),
                      ('transaction_type', operator, name), ('account_id', operator, name)]
            records = self.search(domain + args, limit=limit)
            return records.name_get()
        else:
            return super(BankTransaction, self)._name_search(name=name, args=args, operator=operator, limit=limit,
                                                             name_get_uid=name_get_uid)

    @api.model
    def create(self, vals):
        transaction = super(BankTransaction, self).create(vals)
        print("Transaction>>>>>>>", transaction)
        if vals.get('transaction_type') == 'deposit' and transaction.account_id:
            transaction.account_id.write({'balance': transaction.account_id.balance + vals.get('amount', 0.0)})
        elif vals.get('transaction_type') == 'withdraw' and transaction.account_id:
            transaction.account_id.write({'balance': transaction.account_id.balance - vals.get('amount', 0.0)})
        return transaction

    def write(self, vals):
        for transaction in self:
            if vals.get('transaction_type') == 'deposit' and vals.get('amount'):
                transaction.account_id.write({'balance': transaction.account_id.balance + vals['amount']})
            elif vals.get('transaction_type') == 'withdraw' and vals.get('amount'):
                transaction.account_id.write({'balance': transaction.account_id.balance - vals['amount']})
        return super(BankTransaction, self).write(vals)


class ResPartner(models.Model):
    _inherit = "res.partner"

    dob = fields.Date(string="DOB")

    def customerPrint(self):
        return self.env.ref("bank.action_report_res_partner").report_action(self)

    def action_send_email(self):
        self.ensure_one()
        lang = self.env.context.get('lang')

        # Correct reference to the mail template
        mail_template = self.env.ref('bank.customer_mail_template_blog')

        if mail_template and mail_template.lang:
            lang = mail_template._render_lang(self.ids)[self.id]

        ctx = {
            'default_model': 'res.partner',  # Use the correct model
            'default_res_ids': [self.id],  # Correct parameter name and as a list
            'default_template_id': mail_template.id if mail_template else None,
            'default_composition_mode': 'comment',
            'mark_so_as_sent': True,
            'default_email_layout_xmlid': 'mail.mail_notification_light',
            'proforma': self.env.context.get('proforma', False),
            'force_email': True,
        }

        return {
            'type': 'ir.actions.act_window',
            'view_mode': 'form',
            'res_model': 'mail.compose.message',
            'views': [(False, 'form')],
            'view_id': False,
            'target': 'new',
            'context': ctx,
        }

    def run_bdy_notification(self):
        today = fields.Date.today()
        today_month_day = today.strftime('%m-%d')
        all_records = self.search([])
        for rec in all_records:
            if rec.dob and rec.dob.strftime('%m-%d') == today_month_day:
                email_values = {
                    'email_to': rec.email,
                    'subject': f"Happy Birthday {rec.name}"
                }
                print(f"Happy Birthday {rec.display_name}")
                mail_template = self.env.ref('bank.birthday_email_template')
                mail_template.send_mail(rec.id, email_values=email_values, force_send=True)
                print(f"Happy Birthday {rec.display_name} Again")


