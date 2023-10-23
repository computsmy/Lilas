from odoo import api,fields,models,_,Command
from odoo.exceptions import *
import json
class Manufacturing(models.Model):
    _inherit = "mrp.production"

    @api.model
    def create(self,vals):
        res = super(Manufacturing,self).create(vals)
        for data in res:
            # raise UserError(res.move_raw_ids.mapped('product_id.name'))
            old_data = res.move_raw_ids
            if data.product_id:
                sales_order_id = self.env['sale.order'].search([('name','=',data.origin)])
                sale_order_line_id = self.env['sale.order.line'].search([('order_id','=',sales_order_id.id),('use_fabric','=',True),('product_id','=',data.product_id.id)],limit=1)
                fabric_ids = self.env['sale.order.line'].search([('is_fabric','=',True),('related_sale_order_line','=',sale_order_line_id.id)])
                if sale_order_line_id:
                    if len(fabric_ids) == 1:
                        data.write({
                            'move_raw_ids': [Command.create({
                                'product_id': fabric_ids.product_id.id,
                                'product_uom_qty' : sale_order_line_id.product_uom_qty * (sale_order_line_id.product_id.front_size + sale_order_line_id.product_id.back_size)
                            })]
                        })
                    else:
                        data.write({
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
                # raise UserError(res.move_raw_ids)
        return res

class StockMove(models.Model):
    _inherit = "stock.move"

    is_fabric = fields.Boolean('Is Fabric', related='product_tmpl_id.is_fabric')
    use_fabric = fields.Boolean('Use Fabric', related='product_tmpl_id.use_fabric')