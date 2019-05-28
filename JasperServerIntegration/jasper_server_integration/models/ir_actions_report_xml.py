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
from odoo.exceptions import UserError
from odoo.http import HttpRequest

from logging import getLogger
import requests

_logger = getLogger(__name__)


class IrActionsReportXml(models.Model):
    _inherit = 'ir.actions.report.xml'

    is_jasper_report = fields.Boolean(
        string="Is the report a Jasper Server report?"
    )
    report_name = fields.Char(required=False)

    report_full_path = fields.Text(
        string="Full path",
        help="The full path from the Jasper Server's repository of the report."
    )
    parameters_ids = fields.One2many(
        comodel_name="ir.actions.report.jasper.report.parameter",
        inverse_name="ir_action_report_jasper_server_id", string="Parameters",
        help="The parameters that communicate between Odoo and Jasper Server."
    )

    def log_in_or_restore_session(self):
        _logger.debug(
            "Checking if there's a valid session for the Jasper Server"
        )

        if hasattr(HttpRequest.session, 'jasperServerSessionId'):
            jasper_server_cookie = HttpRequest.session.jasperServerSessionId
            _logger.debug("Session cookie of Jasper Server found.")
        else:
            _logger.debug("Session cookie not found. Starting new session...")

            user_credentials = dict()
            user_credentials['j_username'] = self.env['ir.config_parameter'].\
                get_param('jasper_server_integration.username', '')
            user_credentials['j_password'] = self.env['ir.config_parameter'].\
                get_param('jasper_server_integration.password', '')

            jasper_server_address = self.env['ir.config_parameter'].\
                get_param('jasper_server_integration.address', '')

            if not (user_credentials['j_username'] and
                    user_credentials['j_password'] and
                    jasper_server_address
            ):
                _logger.error(
                    "No configuration found for Jasper Server integration!"
                    " You need to fill it at"
                    " \"Settings/General Settings Technical/"
                    "Reporting/Jasper Server Configuration\""
                )
                raise UserError(_(
                    "No configuration found for Japer Server integration."
                ))

            _logger.debug("Credentials: {} | {}".format(
                user_credentials['j_username'], user_credentials['j_password']
            ))

            _logger.debug("Attempting to obtain a new session ID")

            try:
                request = requests.post(
                    jasper_server_address, params=user_credentials,
                    allow_redirects=False
                )
            except Exception:
                raise UserError(
                    _("Couldn't make the request to the Jasper Server."
                      " The URL may be incorrect or the server has"
                      " stopped working")
                )

            if request.status_code == 200:
                _logger.debug(
                    "Request successful, retrieving session ID and creating a"
                    " cookie for the user"
                )
                session_id = request.cookies['JSESSIONID']
                HttpRequest.session.jasperServerSessionId = session_id
                jasper_server_cookie = session_id
            # In Spring 3, if there's an error with the login data, it will
            # redirect to a login page with a ?error=1 GET parameter.
            elif request.status_code == 302:
                _logger.info(
                    "Got a 302 status code response for the"
                    " login request, checking if the response warns us of"
                    " incorrect credentials."
                )
                # We'll check if the Location header attribute has a error=1,
                # else we'll asume that the session id is valid.
                if "error=1" in request.headers['location']:
                    raise UserError(
                        _("Login data is invalid. Make sure that the user"
                          " exists and it's password is correct.")
                    )
                else:
                    # Same as request.status_code == 200. We assign the
                    # session_id and proceed as valid
                    session_id = request.cookies['JSESSIONID']
                    HttpRequest.session.jasperServerSessionId = session_id
                    jasper_server_cookie = session_id
            elif request.status_code == 401:
                _logger.warn(
                    "The current user can't log in. The server returned 401!"
                )
                raise UserError(
                    _("Can't connect to Jasper Server with the user defined."
                      " Please, change the permissions of the user or"
                      " change the credentials to another user that"
                      " is able to log in.")
                )
            else:
                _logger.error(
                    "Unexpected error found! The status code is:"
                    " {}".format(request.status_code)
                )
                raise UserError(
                    _("Unexpected error was encountered when attempting to"
                      " print this report!")
                )

        return jasper_server_cookie

    @api.one
    def jasper_render_report(self, ids):
        # We'll start by retrieving the session ID of the user specified
        # in the configuration
        session_id = self.log_in_or_restore_session()
        # Next, we'll construct the URL to the Jasper Server's API endpoint
        url = "{}rest_v2/reports/{}.pdf".format(
            self.env['ir.config_parameter']
                .get_param('jasper_server_integration.address'),
            self.report_full_path
        )

        # Preparing all the parameters specified in the report
        parameters = dict()
        res_object = self.env[self.model].browse(ids)
        for parameter in self.parameters_ids:
            parameters[parameter.name] = parameter.evaluate_expression(
                res_object
            )
        # We make the request and check it's result.
        timeout = int(
            self.env['ir.config_parameter']
            .get_param('jasper_server_integration.timeout', 60)
        )

        try:
            request = requests.get(
                url, cookies={'JSESSIONID': session_id},
                params=parameters, allow_redirects=False,
                timeout=timeout
            )
        except requests.Timeout:
            raise UserError(
                _(
                    "The request took too long to respond. This report may be"
                    " too large.")
            )

        if request.status_code == 200:
            _logger.info(
                "Successfully retrieved report {}".format(self.name)
            )
            return request.content
        # This status code signifies a forbidden operation. It can be
        # caused by lack of priviledges or an expired session.
        elif request.status_code == 401:
            _logger.warn(
                "Session ID has timeout. Removing the session id"
                " and throwing a warning")
            _logger.warn(
                "This can also be caused by lack of priviledges. Make sure"
                " that the user specified in the configuration file can"
                " print the reports."
            )
            HttpRequest.session.jasperServerSessionId = \
                self.log_in_or_restore_session()
            raise UserError(
                _(
                    "Current Jasper Server session has expired. Try again to"
                    " redo the log in and print the report.")
            )
        # This status code specifies that the file wasn't found.
        elif request.status_code == 404:
            _logger.error(
                "File not found. The report isn't deployed in the"
                " specified path. Make sure that the repository in"
                " Jasper Server contains that file and the route is valid."
            )
            raise UserError(
                _("This report's template wasn't found in the"
                  " specified path. Make sure that the Jasper Server's"
                  " repository contains the file in that path.")
            )
        # In the case we find a strange status code,
        # we'll print it in the screen.
        else:
            _logger.error(
                "Unexpected status code found when making the"
                " request for report {}. The status code is {}"
                .format(self.name, request.status_code)
            )
            raise UserError(
                _("Couldn't retreive the report from the server."
                  " The server's status code is {}.")
                .format(request.status_code)
            )

    @api.model
    def render_report(self, res_ids=None, name=None, data=None):
        # If this is a Jasper Server report ...
        if self.is_jasper_report:
            # We'll start by retrieving the session ID of the user specified
            # in the configuration
            session_id = self.log_in_or_restore_session()
            # Next, we'll construct the URL to the Jasper Server's API endpoint
            url = "{}rest_v2/reports/{}.pdf".format(
                self.env['ir.config_parameter']
                    .get_param('jasper_server_integration.address'),
                self.report_full_path
            )

            # Preparing all the parameters specified in the report
            parameters = dict()
            res_object = self.env[self.model].browse(res_ids)
            for parameter in self.parameters_ids:
                parameters[parameter.name] = parameter.evaluate_expression(
                    res_object
                )
            # We make the request and check it's result.
            timeout = int(
                self.env['ir.config_parameter']
                .get_param('jasper_server_integration.timeout', 60)
            )

            try:
                request = requests.get(
                    url, cookies={'JSESSIONID': session_id},
                    params=parameters, allow_redirects=False, timeout=timeout
                )
            except requests.Timeout:
                raise UserError(
                    _("The request took too long to respond. This report may be"
                      " too large.")
                )

            if request.status_code == 200:
                _logger.info(
                    "Successfully retrieved report {}".format(self.name)
                )
                return request.content
            # This status code signifies a forbidden operation. It can be
            # caused by lack of priviledges or an expired session.
            elif request.status_code == 401:
                _logger.warn("Session ID has timeout. Removing the session id"
                             " and throwing a warning")
                _logger.warn(
                    "This can also be caused by lack of priviledges. Make sure"
                    " that the user specified in the configuration file can"
                    " print the reports."
                )
                HttpRequest.session.jasperServerSessionId = \
                    self.log_in_or_restore_session()
                raise UserError(
                    _("Current Jasper Server session has expired. Try again to"
                      " redo the log in and print the report.")
                )
            # This status code specifies that the file wasn't found.
            elif request.status_code == 404:
                _logger.error(
                    "File not found. The report isn't deployed in the"
                    " specified path. Make sure that the repository in"
                    " Jasper Server contains that file and the route is valid."
                )
                raise UserError(
                    _("This report's template wasn't found in the"
                      " specified path. Make sure that the Jasper Server's"
                      " repository contains the file in that path.")
                )
            # In the case we find a strange status code,
            # we'll print it in the screen.
            else:
                _logger.error(
                    "Unexpected status code found when making the"
                    " request for report {}. The status code is {}"
                    .format(self.name, request.status_code)
                )
                raise UserError(
                    _("Couldn't retreive the report from the server."
                      " The server's status code is {}.")
                    .format(request.status_code)
                )
        else:
            return super(IrActionsReportXml, self).render_report(
                res_ids, name, data
            )
