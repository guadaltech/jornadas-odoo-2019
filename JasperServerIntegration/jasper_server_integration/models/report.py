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
from odoo import fields, api, models


class Report(models.Model):
    _inherit = "report"

    @api.model
    def get_pdf(self, docids, report_name, html=None, data=None):
        report_action = self._get_report_from_name(report_name)
        if report_action.is_jasper_report:
            # Si es Jasper Report, iniciamos la impresión del informe
            # El resultado de la operación de 'jasper_render_report'
            # contiene el PDF resultado.
            pdf_content = report_action.jasper_render_report(docids)[0]
            return pdf_content
        else:
            # Se trata de otro tipo de informe. Imprimimos con el sistema normal
            return super(Report, self).get_pdf(docids, report_name,
                                               html, data)
