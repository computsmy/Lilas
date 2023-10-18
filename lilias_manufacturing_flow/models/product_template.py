from odoo import api,fields,models,_

class ProductTemplate(models.Model):
    _inherit = "product.template"

    product_is_fabric_or_use_fabric = fields.Selection([
        ('is_fabric','Is Fabric'),
        ('use_fabric','Use Fabric')
    ])
