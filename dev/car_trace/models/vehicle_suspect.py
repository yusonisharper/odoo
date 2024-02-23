from odoo import _, api, fields, models
from odoo.exceptions import UserError, ValidationError
from dateutil import relativedelta


class vehicle_suspect(models.Model):
    _name = "vehicle.suspect"
    _description = "suspect description"
    _order = "id desc"

    name = fields.Char('suspect name')
    color = fields.Char('skin color')
    height = fields.Integer('height')
    race = fields.Char("suspect's race")
    description = fields.Text('description')