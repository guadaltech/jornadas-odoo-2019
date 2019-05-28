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

from odoo import fields, models, api, _
from odoo.exceptions import ValidationError

from logging import getLogger

_logger = getLogger(__name__)


class IrActionsReportJasperReportParameter(models.Model):
    _name = 'ir.actions.report.jasper.report.parameter'

    name = fields.Char(string="Nombre del parámetro")
    expression = fields.Text(
        string="Valor evaluado", help="Valor evaluado del parámetro.",
        default="""
# Python code.
# You can use the following variables :
#  - self: ORM model of the record which is checked
#  - object: same as order or line, browse_record of the sale order or
#  - pool: ORM model pool (i.e. self.pool)
#  - cr: database cursor
#  - context: current context
#  - invoice: test for invoice tests
# Note: returned value have to be set in the variable 'result'
"""
    )
    ir_action_report_jasper_server_id = fields.Many2one(
        comodel_name="ir.actions.report"
    )

    @api.multi
    def evaluate_expression(self, res):
        """
        Returns the value defined in the 'expression'.
        It will also check if the expression is valid and
        throw the applicable exception.
        """
        _logger.debug(
            "Checking the expression of {} with ID {}".format(res._name, res.id)
        )

        return_value = None
        try:
            # FIXME Unsecure use of 'eval', but it is needed to allow correct
            # transformation of elements to the report.
            return_value = eval(self.expression, __builtins__, res)
        except ValueError:
            raise ValidationError(
                _("The code provided contains bytecode that can be considered"
                  " dangerous. Expression of parameter {}.").format(self.name)
            )
        except TypeError:
            raise TypeError(
                _("The code contains a code object, thus it can't be compiled."
                  " Expression of parameter {}.").format(self.name)
            )
        except NameError:
            raise NameError(
                _("The code contains code that uses forbidden names."
                  "Expression of parameter {}").format(self.name)
            )
        except SyntaxError as excp:
            raise SyntaxError(
                _("The code contains an error related to the syntax of the "
                  "expression. The exception message is: {}".format(
                    excp.msg + excp.message
                    )
                  )
            )
        except Exception as excp:
            raise Exception(
                _("An unexpected exception was launched when evaluating the"
                  "code. Exception message is {}".format(
                    excp.msg + excp.message
                    )
                  )
            )

        return return_value
