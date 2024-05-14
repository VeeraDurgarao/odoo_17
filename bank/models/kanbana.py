from odoo import fields, models, api


class ButtonKanbanView(models.Model):
    _name = "button.model.kanban"
    _description = "Button Model Kanban View"
    _inherit = "button.model"
    _order = "status"

    kanban_state = fields.Selection([('active', 'Active'), ('inactive', 'Inactive'),
                                     ], string='Status', default='active')

    _inherit = 'button.model'
    _inherit_views = {
        'kanban': 'button_kanban.button_model_kanban_view',
    }
