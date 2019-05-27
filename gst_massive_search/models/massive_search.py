# -*- coding: utf-8 -*-
from odoo import models
from odoo import fields
from odoo import api


class MassiveSearch(models.TransientModel):
    _name = 'massive.search'

    model_id = fields.Many2one(
        comodel_name="ir.model",
        string="Model",
    )
    field_id = fields.Many2one(
        comodel_name="ir.model.fields",
        string="Fields"
    )
    exist_searchable = fields.Boolean()
    text_search = fields.Text(
        string='Datas',
        required=False,
        help='Search data separate by return')

    @api.onchange('model_id')
    def search_exist_searchable(self):
        self.exist_searchable = False
        if self.model_id.field_id.filtered(lambda a: a.is_massive_searchable):
            self.exist_searchable = True

    @api.multi
    def op_search(self):
        added_filters = self.env.context.get('added_filters', None)
        op_names = None
        if self.text_search:
            op_names = self.text_search.rstrip().split('\n')
        domain = []
        if self.field_id and self.text_search:
            field_model_name = self.field_id.relation
            if field_model_name:
                searched_ids = []
                for name in op_names:
                    name_search_results = \
                        self.env[field_model_name].name_search(name)
                    searched_ids += map(lambda x: x[0], name_search_results)
                domain = [(self.field_id.name, 'in', searched_ids)]
            elif op_names:
                domain = [(self.field_id.name, 'in', op_names)]
        if added_filters:
            if type(added_filters[0]) == list:
                for item in added_filters:
                    domain.append(item)
            else:
                domain.append(added_filters)
        new_row = self.env[self.model_id.model].sudo().search(domain)
        return {'type': 'ir.actions.act_window',
                'name': self.model_id.name,
                'res_model': self.model_id.model,
                'view_type': 'form',
                'view_mode': 'tree,form',
                'domain': [("id", "in", new_row.ids)]}
