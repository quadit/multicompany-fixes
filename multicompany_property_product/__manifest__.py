# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
{
    'name': 'Multi Company Product',
    'version': '10.0.1.0.0',
    'summary': 'Creu Blanca configuration',
    'author': 'Creu Blanca, '
              'Odoo Community Association (OCA)',
    'sequence': 30,
    'category': 'Creu Blanca',
    'website': 'http://www.creublanca.es',
    'depends': ['product', 'multicompany_property'],
    'data': [
        'views/product_views.xml',
        'views/product_category_views.xml'
    ],
    'installable': True,
    'application': False,
    'auto_install': True,
}
