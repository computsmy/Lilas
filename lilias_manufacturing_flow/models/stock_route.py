from odoo import api,fields,models

class StockRoute(models.Model):
    _inherit = "stock.route"

    enable_fabric = fields.Boolean('enable_fabric')