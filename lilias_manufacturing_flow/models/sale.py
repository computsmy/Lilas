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
    is_fabric = fields.Boolean('Is Fabric',related='product_template_id.is_fabric')
    use_fabric = fields.Boolean('Use Fabric',related='product_template_id.use_fabric')
    related_sale_order_line = fields.Many2one('sale.order.line')
    r_id = fields.Integer(related='related_sale_order_line.id')
    seq_fabric = fields.Integer('Sequence Fabric')

    @api.model
    def create(self,vals):
        res = super(SalesOrderLine,self).create(vals)
        if res.use_fabric:
            res['related_sale_order_line'] = res.id
            res['seq_fabric'] = 2
            self.env['sale.order.line'].create({
                'display_type':'line_section',
                'name':res.product_id.name,
                'related_sale_order_line': res.id,
                'order_id' : res.order_id.id,
                'seq_fabric' : 1
            })
        return res
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



