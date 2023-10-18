# -*- coding: utf-8 -*-
{
    'name': "Lilias Manufacturing Flow",

    'summary': """
        Custom Flow For Lilias Company to Manufacture Sofa's
        """,

    'description': """
        The purpose of this module is to add the fabric option in the product configurator and include it in the calculation of price and quantity in the Sales Order and Manufacturing process.
    """,

    'author': "Computs Sdn Bhd",
    'website': "https://www.computs.com.my",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/16.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Manufacturing',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base','sale','mrp','product'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'views/product_template.xml',
        'views/sale.xml',
        'wizard/fabric_configurator_wizard.xml',
        # 'static/src/views/templates.xml'
    ],
    # 'assets':{
    #     'sale_product_configurator.assets': [
    #         'static/src/js/configure_variant.js'
    #     ]
    # }

}
