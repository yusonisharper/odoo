from odoo import _, api, fields, models
from odoo.exceptions import UserError, ValidationError
from dateutil import relativedelta


class vehicle_location(models.Model):
    _name = "vehicle.location"
    _description = "vehicle current location"
    _order = "id desc"

    name = fields.Char('location')
    description = fields.Text('description')
    longitude = fields.Float("longitude", required=True)
    latitude = fields.Float("latitude", required=True)
    vehicle_id = fields.Many2one("vehicle.property")

    @api.model
    def create(self, vals):
        prop = self.env['vehicle.property'].browse(vals['vehicle_id'])
        prop.state = 'vehicle_discovered'
        return super(vehicle_location, self).create(vals)