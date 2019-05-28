# -*- encoding: utf-8 -*-
##############################################################################
#
#    Guadaltech Soluciones tecnológicas S.L.  www.guadaltech.es
#    Author: Ignacio José Alés López & Carlos Jimeno Cordero
#    Copyright (C) 2018 Guadaltech Soluciones Tecnológicas (https://www.guadaltech.es/). All Rights Reserved
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
###############################################################################
from odoo import fields, models

from logging import getLogger

_logger = getLogger(__name__)


class JasperServerReport(models.Model):
    _name = "jasper.server.report"

    report_name = fields.Char(
        string="Nombre del informe",
        help="El nombre del informe. Aparecerá en la lista de items a imprimir"
    )
    report_path = fields.Char(
        string="Ruta del informe",
        help="La localización del informe en Jasper Server."
    )


