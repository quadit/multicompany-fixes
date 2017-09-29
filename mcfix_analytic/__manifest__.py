# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
{
    'name': 'Multi Company Fix Analytic',
    'version': '10.0.1.0.0',
    'summary': 'Creu Blanca configuration',
    'author': 'Creu Blanca, '
              'Odoo Community Association (OCA)',
    "license": "LGPL-3",
    'sequence': 30,
    'category': 'Creu Blanca',
    'website': 'http://www.creublanca.es',
    'depends': ['analytic', 'mcfix_base'],
    'data': [
        'views/analytic_account_views.xml'
    ],
    'installable': True,
    'application': False,
    'auto_install': True,
}
