from odoo import api, fields, models, Command


class FabricConfiguratorWizard(models.TransientModel):
    _name = "fabric.configurator.wizard"

    name = fields.Char('Fabric')
    fabric_top = fields.Many2one('product.product')
    fabric_bottom = fields.Many2one('product.product')
    sale_order_line_id = fields.Many2one('sale.order.line')
    sale_id = fields.Many2one('sale.order', related="sale_order_line_id.order_id", store=True)
    both_same_fabric = fields.Boolean('Both use same fabric?')

    def confirm_fabric(self):
        for record in self:
            fabric_records = record.env['sale.order.line'].search([('related_sale_order_line','=',record.sale_order_line_id.id)])
            if fabric_records:
                for i in fabric_records:
                    i.unlink()
            if not record.both_same_fabric:
                record.sale_id.write({
                    'order_line': [Command.create({
                        'product_id': record.fabric_top.id,
                        'name': f'Fabric for {record.sale_order_line_id.name}',
                        'fabric_position': 'both',
                        'related_sale_order_line': record.sale_order_line_id.id
                    })]
                })
            else:
                record.sale_id.write({
                    'order_line': [Command.create({
                        'product_id': record.fabric_top.id,
                        'name': f'Fabric for {record.sale_order_line_id.name}',
                        'fabric_position': 'top',
                        'related_sale_order_line': record.sale_order_line_id.id
                    }), Command.create({
                        'product_id': record.fabric_bottom.id,
                        'name': f'Fabric for {record.sale_order_line_id.name}',
                        'fabric_position': 'bottom',
                        'related_sale_order_line': record.sale_order_line_id.id
                    })
                    ]
                })