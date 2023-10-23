from odoo import api,fields,models,_

class ProductTemplate(models.Model):
    _inherit = "product.template"

    is_fabric = fields.Boolean('Is Fabric')
    use_fabric = fields.Boolean('Use Fabric')
    front_size = fields.Float('Front LM')
    back_size = fields.Float('Back LM')

    show_use_fabric = fields.Boolean(compute='_show_use_fabric')
    def _show_use_fabric(self):
        for record in self:
            count = 0
            for i in record.route_ids:
                if i.enable_fabric == True:
                    count += 1
                else:
                    pass
            if count == 2:
                record['show_use_fabric'] = True
            else:
                record['show_use_fabric'] = False
                record['use_fabric'] = False

    @api.onchange('is_fabric')
    def is_fabric_mutual_exclusive(self):
        if self.use_fabric:
            self['is_fabric'] = False
    @api.onchange('use_fabric')
    def use_fabric_mutual_exclusive(self):
        if self.is_fabric:
            self['use_fabric'] = False
