from odoo import api,fields,models,_,Command

class Manufacturing(models.Model):
    _inherit = "mrp.production"

    @api.model
    def create(self,vals):
        res = super(Manufacturing,self).create(vals)
        for data in res:
            if data.product_id:
                sales_order_id = self.env['sale.order'].search([('name','=',data.origin)])
                sale_order_line_id = self.env['sale.order.line'].search([('order_id','=',sales_order_id.id),('product_is_fabric_or_use_fabric','=','use_fabric'),('product_id','=',data.product_id.id)],limit=1)
                fabric_ids = self.env['sale.order.line'].search([('product_is_fabric_or_use_fabric','=','is_fabric'),('related_sale_order_line','=',sale_order_line_id.id)])
                if sale_order_line_id:
                    if len(fabric_ids) == 1:
                        res.write({
                            'move_raw_ids': [Command.create({
                                'product_id': fabric_ids.product_id.id,
                                'product_uom_qty' : sale_order_line_id.product_uom_qty * (sale_order_line_id.product_id.front_size + sale_order_line_id.product_id.back_size)
                            })]
                        })
                    else:
                        res.write({
                            'move_raw_ids': [Command.create({
                                'product_id': fabric_ids[0].product_id.id,
                                'product_uom_qty' : sale_order_line_id.product_uom_qty * sale_order_line_id.product_id.front_size
                            }),
                            Command.create({
                                'product_id': fabric_ids[1].product_id.id,
                                'product_uom_qty': sale_order_line_id.product_uom_qty * sale_order_line_id.product_id.back_size
                            })
                            ]
                        })
        return res

class StockMove(models.Model):
    _inherit = "stock.move"

    product_is_fabric_or_use_fabric = fields.Selection(related='product_id.product_tmpl_id.product_is_fabric_or_use_fabric')