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

from odoo import models, fields, api, _
from odoo.exceptions import ValidationError

import re

FIELD_KEY_DICT = {
    'jasper_server_address': "jasper_server_integration.address",
    'jasper_server_username': "jasper_server_integration.username",
    'jasper_server_password': "jasper_server_integration.password",
    'jasper_server_timeout': "jasper_server_integration.timeout"
}


class JasperServerIntegrationSettings(models.TransientModel):
    _name = "jasper.server.integration.configuration"

    jasper_server_address = fields.Char(
        string="Address",
        help="The address of the Jasper Server. The complete address must"
             " follow this pattern: http://<host>:<port>/jasperserver[-pro]/",
        default=lambda self: self._default_address()
    )
    jasper_server_username = fields.Char(
        string="Username",
        help="The username of the user that will print the reports.",
        default=lambda self: self._default_username()
    )
    jasper_server_password = fields.Char(
        string="Password",
        help="The password of the user that will print the reports.",
        default=lambda self: self._default_password()
    )
    jasper_server_timeout = fields.Integer(
        string="Timeout",
        help="Timeout for the response of the request. If the response from the"
             " server surpasses this value, it will throw an error message.",
        default=lambda self: self._default_timeout()
    )

    def _default_address(self):
        saved_address = self.env['ir.config_parameter'].get_param(
            "jasper_server_integration.address"
        )
        return saved_address if saved_address else ""

    def _default_username(self):
        saved_username = self.env['ir.config_parameter'].get_param(
            "jasper_server_integration.username"
        )
        return saved_username if saved_username else "jasperadmin"

    def _default_password(self):
        saved_password = self.env['ir.config_parameter'].get_param(
            "jasper_server_integration.password"
        )
        return saved_password if saved_password else "jasperadmin"

    def _default_timeout(self):
        saved_timeout = self.env['ir.config_parameter'].get_param(
            "jasper_server_integration.timeout"
        )
        return saved_timeout if saved_timeout else 60

    @api.multi
    def write(self, vals):
        super(JasperServerIntegrationSettings, self).write(vals)
        self.set_params()

    @api.multi
    @api.constrains('jasper_server_address')
    def validate_server_address(self):
        valid_address_regex = re.compile("http:\/\/.*:[0-9]+\/jasperserver(-pro)*\/")
        if not valid_address_regex.match(self.jasper_server_address):
            raise ValidationError(
                _("The address used does not follow this pattern:"
                  " http://<host>:<port>/jasperserver[-pro]/")
            )

    @api.multi
    def set_params(self):
        for field, key in FIELD_KEY_DICT.items():
            value = getattr(self, field, '')
            self.env['ir.config_parameter'].set_param(key, value)
