from odoo import fields, models, api, _


class Button(models.Model):
    #Attributes
    _name = "button.model"
    _description = "Branch Model"

    #fields
    name = fields.Char(string="Name")
    location = fields.Text(string="Location")
    email = fields.Char(string="Email")
    Contact = fields.Char(string="Contact")
    Branch_Code = fields.Char(string="Branch Code")
    status = fields.Selection([
        ('active', 'Active'),
        ('inactive', 'Inactive'),
    ], string="Status")
    # signature = fields.Binary(string='Signature')
    ref_no = fields.Text(string="Ref No", required=True, readonly=True, default=lambda self: _('NEW'))


    # ORM CREATE METHOD
    @api.model
    def create(self, vals):
        if vals.get('ref_no', _('NEW')) == _('NEW'):
            vals['ref_no'] = self.env['ir.sequence'].next_by_code('button.model') or _('NEW')
        return super(Button, self).create(vals)

    # SEARCH NAME METHOD BY USING MANY TO ONE
    @api.model
    def _name_search(self, name='', args=None, operator='ilike', limit=100, name_get_uid=None, order=None):
        args = args or []
        if name:
            args += ['|', '|', ('name', operator, name), ('email', operator, name), ('location', operator, name)]
        return self._search(args, limit=limit, access_rights_uid=name_get_uid)

    def name_get(self):
        result = []
        for rec in self:
            # Customize the display name as needed
            name = f"{rec.name} ({rec.custom_field})"
            result.append((rec.id, name))
        return result

    def searchRead(self):
        records_search = self.search_read([('status', '=', 'active')], ['name'])
        print("Search read function with domain:", records_search)

    def filter(self):
        values = self.search([])
        values2 = self.search([('status', '=', 'active')])
        values3 = self.browse([values])
        print("VALUES IS>>>>>>>>>>>>>>", values)
        print("Searched values is>>>>>", values2)
        print("Browse values is>>>>>>>>>", values3)
        active_records = values.filtered(lambda r: r.status == 'active')
        active_names = [record.name for record in active_records]
        print("Names of active records filter>>>>>:", active_names)

    def mapping(self):
        result = self.search([])
        # value = [i.name for i in result]
        # print(value)
        mapped_values = result.mapped(lambda record: record.name.upper())
        print("Mapped values is>>>>>>>>>>>>>", mapped_values)

    def readGroup(self):
        data = self.read_group(
            [('status', '=', 'active')], ['name','Branch_Code'],
            ['status'])
        print(">>>>>>>>>>>",data)
        # for group in data:
        #     print("Read group>>>>>>>>>>>>", group)

    # def check_orm(self):
    #     recordss = self.search([])
    #     print("id",recordss)
    #
    #     print("Search values in the list:  ")
    #     value = [i.name for i in recordss]
    #     print(value)
    #
    #     # browse = self.browse([1, 2, 3, 4, 5, 6, 7])
    #     # for i in browse:
    #     #     print("Browse is >>>>>>>>>>>>", i.name)
    #
    #     value2 = sorted(value,key=None,reverse = False)
    #     # value3 = map(value,lambda rec:rec.name.upper())
    #     print("sorted values is: ",value2)
