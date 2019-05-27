# -*- coding: utf-8 -*-
from odoo import api
from odoo import models


class OpMassiveSearch(models.TransientModel):
    _inherit = "massive.search"

    @api.model
    def action_open_op_masive_search_orders(self):
        sale_order_model = self.env.ref('sale.model_sale_order')
        view1 = "gst_massive_search.massive_search_form"
        return {'name': "Mass Search - Orders",
                'type': "ir.actions.act_window",
                'res_model': "massive.search",
                'view_mode': 'form',
                'view_id': self.env.ref(view1).id,
                'context': {'default_customize': 1,
                            'default_model_id': sale_order_model.id},
                'target': "new"}

    @api.model
    def action_open_op_massive_search_deliveries(self):
        stock_move_model = self.env.ref('stock.model_stock_move')
        customer_location = self.env.ref("stock.stock_location_customers")
        view1 = "gst_massive_search.massive_search_form"
        return {'name': "Mass Search - Deliveries",
                'type': "ir.actions.act_window",
                'res_model': "massive.search",
                'view_mode': 'form',
                'view_id': self.env.ref(view1).id,
                'context': {'default_customize': 1,
                            'default_model_id': stock_move_model.id,
                            'added_filters': [('location_dest_id', '=',
                                               customer_location.id),
                                              ('group_id.sale_id',
                                               '!=', False)]},
                'target': "new"}

    @api.model
    def action_open_op_massive_search_dispatches(self):
        stock_move_model = self.env.ref('stock.model_stock_move')
        view1 = "gst_massive_search.massive_search_form"
        return {'name': "Mass Search - Dispatches",
                'type': "ir.actions.act_window",
                'res_model': "massive.search",
                'view_mode': 'form',
                'view_id': self.env.ref(view1).id,
                'context': {'default_customize': 1,
                            'default_model_id': stock_move_model.id,
                            'added_filters': ('raw_material_production_id',
                                              '!=', False)},
                'target': "new"}

    @api.model
    def action_open_op_massive_search_warehouse(self):
        stock_production_lot_model = \
            self.env.ref('stock.model_stock_production_lot')
        view1 = "gst_massive_search.massive_search_form"
        filters = [('product_qty', '>', 0),
                   ('product_id.sale_ok', '=', True)]
        return {'name': "Mass Search - Warehouse",
                'type': "ir.actions.act_window",
                'res_model': "massive.search",
                'view_mode': 'form',
                'view_id': self.env.ref(view1).id,
                'context': {'default_customize': 1,
                            'default_model_id': stock_production_lot_model.id,
                            'added_filters': filters},
                'target': "new"}
