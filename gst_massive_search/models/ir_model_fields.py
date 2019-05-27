# -*- coding: utf-8 -*-
from odoo import fields, api, models
from odoo.exceptions import UserError


class IrModelFields(models.Model):
    _inherit = "ir.model.fields"

    is_massive_searchable = fields.Boolean(
        string="Searchable",
        default=False
    )

    @api.multi
    def make_searchable(self):
        if len(self) == 0:
            raise UserError("You must select some field to convert it to "
                            "massive search.")
        else:
            for field in self:
                self._cr.execute("UPDATE ir_model_fields "
                                 "SET is_massive_searchable = true "
                                 "WHERE id={}".format(field.id))

    @api.multi
    def disable_searchable(self):
        if len(self) == 0:
            raise UserError("You must select some field to deactivate it "
                            "as a massive search.")
        else:
            for field in self:
                self._cr.execute("UPDATE ir_model_fields "
                                 "SET is_massive_searchable = false "
                                 "WHERE id={}".format(field.id))

    @api.model_cr
    def init(self):
        self._cr.execute("UPDATE ir_model_fields "
                         "SET is_massive_searchable=false "
                         "WHERE is_massive_searchable IS NULL")

        self._cr.execute("ALTER TABLE ir_model_fields "
                         "ALTER COLUMN is_massive_searchable SET DEFAULT false")
