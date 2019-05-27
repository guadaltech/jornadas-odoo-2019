# -*- encoding: utf-8 -*-
#
#    Guadaltech Soluciones tecnológicas S.L.  www.guadaltech.es
#    Author:  Guadaltech Soluciones tecnológicas S.L
#    Copyright (C) 2004-2010 Tiny SPRL (http://tiny.be). All Rights Reserved
#
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see http://www.gnu.org/licenses/.
#
from odoo import fields
from odoo import models
from odoo import api
from odoo import _


class SaleImportConf(models.TransientModel):
    _name = 'sale.import.conf'
    _rec_name = 'name'

    name = fields.Char(
        string='name',
        required='True'
    )
    columns_ids = fields.One2many(
        comodel_name='sale.import.conf.columns',
        inverse_name='sale_import_conf_id',
        string='Columns'
    )

    @api.multi
    def copy(self, default=None):
        self.ensure_one()
        default = default or {}
        columns_ids = [x.copy().id for x in self.columns_ids]
        default.update({'name': self.name,
                        'columns_ids': [(6, 0, columns_ids)]})
        return super(SaleImportConf, self).copy(default)


class PnImportConfColumns(models.TransientModel):
    _name = 'sale.import.conf.columns'
    _order = 'sequence,id'

    sequence = fields.Integer(
        string='Sequence',
        default=10
    )
    name = fields.Selection(
        [('partner', _('Customer')),
         ('name', 'PN'),
         ('descripcion', _('PN Description')),
         ('referencia', _('Reference')),
         ('fecha_pedido', _('Order Date')),
         ('cantidad', _('Qty')),
         ('precio', _('Price')),
         ('blank', _('Ignore Column'))],
        string='Column Name',
        required=True
    )
    sale_import_conf_id = fields.Many2one(
        comodel_name='sale.import.conf',
        string='Template'
    )
