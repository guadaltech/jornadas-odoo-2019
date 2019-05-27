# -*- encoding: utf-8 -*-
##############################################################################
#
#    Guadaltech Soluciones tecnológicas S.L.  www.guadaltech.es
#    Author: Alfonso Muñoz Baena
#    Copyright (C) 2017 Tiny SPRL (http://tiny.be). All Rights Reserved
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
##############################################################################

{
    'name': 'GST Massive Search',
    'version': '12.0.1.0.0',
    'category': 'Tools',
    'summary': 'Tools',
    'description': """
        Tools Massive Search
    """,
    'author': 'Guadaltech S.L.',
    'license': 'GPL-3',
    'category': '',
    'depends': ['base'],
    'data': ['views/ir_model_fields_views.xml',
             'views/masive_search_view.xml',
             'views/massive_menu_view.xml'],
    'installable': True,
    'auto_install': False,
    'application': True,
}