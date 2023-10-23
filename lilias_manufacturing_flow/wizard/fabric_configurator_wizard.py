from odoo import api, fields, models, Command


class FabricConfiguratorWizard(models.TransientModel):
    _name = "fabric.configurator.wizard"

    name = fields.Char('Fabric')
    fabric_front = fields.Many2one('product.product')
    fabric_back = fields.Many2one('product.product')
    sale_order_line_id = fields.Many2one('sale.order.line')
    sale_id = fields.Many2one('sale.order', related="sale_order_line_id.order_id", store=True)
    use_multiple_fabric = fields.Boolean('Use Multiple Fabric?')

    def confirm_fabric(self):
        for record in self:
            fabric_records = record.env['sale.order.line'].search([('related_sale_order_line','=',record.sale_order_line_id.id)])
            qty_1 = record.sale_order_line_id.product_id.front_size
            qty_2 = record.sale_order_line_id.product_id.back_size
            if fabric_records:
                for i in fabric_records:
                    if i.id == i.related_sale_order_line.id or i.display_type == 'line_section':
                        pass
                    else:
                        i.unlink()
            if not record.use_multiple_fabric:
                record.sale_id.write({
                    'order_line': [Command.create({
                        'product_id': record.fabric_front.id,
                        'name': f'Fabric for {record.sale_order_line_id.name}',
                        'fabric_position': 'both',
                        'product_uom_qty' : record.sale_order_line_id.product_uom_qty * (qty_1 + qty_2) ,
                        'related_sale_order_line': record.sale_order_line_id.id,
                        'seq_fabric' : 3
                    })]
                })
            else:
                record.sale_id.write({
                    'order_line': [Command.create({
                        'product_id': record.fabric_front.id,
                        'name': f'Fabric for {record.sale_order_line_id.name}',
                        'fabric_position': 'front',
                        'product_uom_qty': record.sale_order_line_id.product_uom_qty * qty_1,
                        'related_sale_order_line': record.sale_order_line_id.id,
                        'seq_fabric': 3
                    }), Command.create({
                        'product_id': record.fabric_back.id,
                        'name': f'Fabric for {record.sale_order_line_id.name}',
                        'fabric_position': 'back',
                        'product_uom_qty': record.sale_order_line_id.product_uom_qty * qty_2,
                        'related_sale_order_line': record.sale_order_line_id.id,
                        'seq_fabric': 4
                    })
                    ]
                })
