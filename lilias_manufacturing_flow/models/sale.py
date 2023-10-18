from odoo import api,fields,models,_
from odoo.exceptions import *

class SalesOrder(models.Model):
    _inherit = "sale.order"
    
class SalesOrderLine(models.Model):
    _inherit = "sale.order.line"

    fabric_position = fields.Selection([
        ('front','Front'),
        ('back','Back'),
        ('both','Both')
    ])
    product_is_fabric_or_use_fabric = fields.Selection(related='product_template_id.product_is_fabric_or_use_fabric')
    related_sale_order_line = fields.Many2one('sale.order.line')


    def fabric_configurator(self):
        wizard = self.env['fabric.configurator.wizard'].create({

            'name': 'Fabric Configurator'
        })
        return {
            'name': _('Fabric Configurator'),
            'type': 'ir.actions.act_window',
            'res_model': 'fabric.configurator.wizard',
            'view_mode': 'form',
            'res_id': wizard.id,
            'target': 'new',
            'context': {'default_sale_order_line_id': 'active_id'}
        }
        print('it runs actually')

