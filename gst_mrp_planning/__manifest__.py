# -*- encoding: utf-8 -*-
##############################################################################
#
#    Guadaltech Soluciones tecnológicas S.L.  www.guadaltech.es
#    Copyright (C) 2004-2010 Tiny SPRL (http://tiny.be). All Rights Reserved
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
    'name': 'GST MRP Planning',
    'version': '12.0.1.0.0',
    'category': 'Delivery Plan',
    'sequence': 14,
    'summary': 'Delivery Plan',
    'description': """
        Add Menu in the Delivery Plan Management
    """,
    'author': 'Guadaltech',
    'license': 'GPL-3',
    'category': '',
    'depends': ['mrp',
                'stock',
                'gst_massive_search',
    ],
    'data': [
             'views/submenu_view.xml',
             'views/masive_search_view.xml'
    ],
    'installable': True,
    'auto_install': False,
    'application': True,
}
