# -*- coding: utf-8 -*-
# Copyright 2016-2017 Guadaltech.
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import fields
from odoo import models
from odoo import api


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    import_date = fields.Datetime(
        string="Import Date"
    )
    import_description = fields.Char(
        string="Import Description"
    )

    @api.multi
    def update_sale_order_partner_datas(self):
        for record in self.filtered(lambda r: r.partner_id):
            if not record.payment_term_id or not record.payment_mode_id:
                record.onchange_partner_id()
