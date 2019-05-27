# -*- coding: utf-8 -*-
# Copyright 2016-2017 Guadaltech.
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import fields
from odoo import models
from odoo import api
from odoo import _
import pytz
import xlrd
import base64
from xlrd import open_workbook
from odoo.exceptions import UserError
from datetime import datetime
import logging
from datetime import datetime
from pytz import timezone
from odoo.tools import DEFAULT_SERVER_DATETIME_FORMAT

_logger = logging.getLogger(__name__)


def number2string(cell):
    res = cell.value
    if cell.ctype == 2:
        res = str(int(cell.value))
    return res


class ImportSaleOrder(models.TransientModel):
    _name = 'import.sale.order'
    _description = 'Import Sale Order'

    name = fields.Char(
        string='name',
        default='Import Sale Order'
    )
    sale_import_conf_id = fields.Many2one(
        comodel_name='sale.import.conf',
        string='Import Template',
        required=True
    )
    file = fields.Binary(
        string='File',
        required=True
    )
    description = fields.Char(
        string="Technical Description"
    )

    log = fields.Text(
        string='Log'
    )

    @api.one
    def read_file(self):
        return open_workbook(file_contents=base64.decodebytes(self.file))

    @api.multi
    def read_and_import_sale_order(self):
        pc = self.env['product.category']
        rp = self.env['res.partner']
        cell_2_string_arr = [['descripcion', 'name'],
                             ]
        self.log = ''
        conf_columns = [x.name for x in self.sale_import_conf_id.columns_ids]
        if 'name' not in conf_columns:
            raise UserError('Please, add the PN column.')
        sale_obj = self.env['sale.order']
        sale_line_obj = self.env['sale.order.line']
        wb_list = self.read_file()
        created_sale_count = 0
        currency_ids = self.env['res.currency'].search([])
        reference = ''
        for wb in wb_list:
            sheet = 0
            for s in wb.sheets():
                sheet += 1
                for row in range(s.nrows):
                    row_ = row + 1
                    try:
                        if row != 0:
                            partner= []
                            sale_new = False
                            nif_partner = number2string(s.cell(row, conf_columns.index('partner')))
                            if len(partner) <= 0 and 'partner' in conf_columns:
                                dom_search = [('vat', '=', nif_partner),('customer', '=', True), ('parent_id', '=', False)]
                                partner = rp.search(dom_search)
                                if len(partner) > 1:
                                    self.log += "In the sheet: " + str(sheet) + " the Row: " + \
                                                str(row_) + " with NIF: " + nif_partner + " are duplicated. \n"
                                    break
                            if len(partner) <= 0 and 'partner' in conf_columns:
                                nif_partner = 'ES' + number2string(s.cell(row, conf_columns.index('partner')))
                                dom_search = [('vat', '=', nif_partner),('customer', '=', True), ('parent_id', '=', False)]
                                partner = self.env['res.partner'].search(dom_search)
                                if len(partner) > 1:
                                    self.log += "In the sheet: " + str(sheet) + " the Row: " + \
                                                str(row_) + " with NIF: " + nif_partner + " are duplicated. \n"
                                    break
                            if len(partner) <= 0:
                                self.log += "In the sheet: " + str(sheet) + " the Row: " + \
                                            str(row_) + " with NIF: " + nif_partner + " not found. \n"
                                break
                            vals = {'partner_id': partner[0].id,
                                    }
                            if not sale_new:
                                sale_doc = False
                                if 'referencia' in conf_columns:
                                    sale_doc = number2string(s.cell(row, conf_columns.index('referencia')))
                                vals.update({
                                             'client_order_ref': sale_doc})
                            if 'fecha_pedido' in conf_columns:
                                idateorder = conf_columns.index('fecha_pedido')
                                date_order = datetime.now()
                                if s.cell(row, idateorder).value != '':
                                    date_order = self.cell2datetime(s.cell(row, idateorder), wb)
                                vals.update({'date_order': date_order})
                            iproduct = conf_columns.index('name')
                            name_product = number2string(s.cell(row, iproduct))
                            dom = [('name', '=', name_product)]
                            product_ids = self.env['product.product'].search(dom)
                            product = None
                            if product_ids:
                                product = product_ids[0]
                            if not product:
                                self.log += "In the sheet: " + str(sheet) + " row: " + str(row_) + \
                                            "#" + name_product + " Producto no encontrado. \n"
                                break
                            vals_line = {'product_id': product.id,
                                         'product_uom': product.uom_id.id}
                            if 'precio' in conf_columns:
                                iprice = conf_columns.index('precio')
                                price = float(s.cell(row, iprice).value) or 0.0
                                vals_line.update({'price_unit': price})
                            if 'cantidad' in conf_columns:
                                iqty = conf_columns.index('cantidad')
                                qty = int(s.cell(row, iqty).value)
                                vals_line.update({'product_uom_qty': qty or 1})
                            for cell_2_string in cell_2_string_arr:
                                conf_column = cell_2_string[0]
                                model_column = cell_2_string[1]
                                new_value = {}
                                if conf_column in conf_columns:
                                    new_value[model_column] = \
                                        number2string(s.cell(row, conf_columns.index(conf_column)))
                                    vals_line.update(new_value)
                            vals.update({'import_date': fields.Datetime.now(),
                                         'import_description': self.description})
                            if reference != sale_doc:
                                sale_new = sale_obj.create(vals)
                                reference = sale_doc
                            sale_new.onchange_partner_id()
                            vals_line.update({'order_id': sale_new.id})
                            sale_line_obj.create(vals_line)
                            created_sale_count += 1
                    except Exception as e:
                        self.log += "In the sheet: " + str(sheet) + " row: " + str(row_) + \
                                    "#" + "Error in created order process. In the log all info. \n"
                        _logger.error("Error in created order process %s" % e.name if hasattr(e, 'name') else e)
        self.log += "\n\n %s Orders created:\n" % created_sale_count

    def cell2datetime(self, cell, wb):
        str_ = cell.value
        if cell.ctype == 3:  # 3 es 'xldate' , 1 es 'text'
            year, month, day, hour, minute, second = xlrd.xldate_as_tuple(str_, wb.datemode)
            initial_date = datetime(year, month, day, hour, minute, second)
        else:
            if "." in str_:
                initial_date = datetime.strptime(str_, '%d.%m.%Y')
            elif "-" in str_:
                initial_date = datetime.strptime(str_, '%d-%m-%Y')
            else:
                initial_date = datetime.strptime(str_, '%d/%m/%Y')
        native = datetime.strptime('%s-%s-%s 00:00:00' % (initial_date.year,
                                                          initial_date.month,
                                                          initial_date.day),
                                   "%Y-%m-%d %H:%M:%S")
        return self._sync_datetime_zone(initial_date)

    @api.model
    def _sync_datetime_zone(self, date):
        new_timezone = timezone("UTC")

        old_timezone = timezone("Europe/Madrid")
        if date:
            dt_planned = old_timezone.localize(datetime.strptime(str(date), DEFAULT_SERVER_DATETIME_FORMAT))
        date = datetime.strftime(dt_planned.astimezone(new_timezone), DEFAULT_SERVER_DATETIME_FORMAT)
        return date
