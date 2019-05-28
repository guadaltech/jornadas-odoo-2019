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

{
    'name': "Jasper Server Integration",
    'category': "Reporting",
    'version': "10.0.1.0.0",
    'description': """
        This package integrates the reporting engine Jasper Server with Odoo, allowing to print reports made in Jasper Server with data facilitated with Odoo.
    """,
    'author': "Ignacio José Alés López & Carlos Jimeno Cordero",
    'website': "https://www.guadaltech.es/",
    'depends': [
        'web',
        'report'
    ],
    'data': [
        'views/jasper_server_integration_configuration_views.xml',
        'views/ir_actions_report_views.xml',
        'views/ir_actions_report_jasper_server_parameter_views.xml'
    ]
}