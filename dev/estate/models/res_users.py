from odoo import _, api, fields, models
from odoo.exceptions import UserError, ValidationError


class EstatePropertyUser(models.Model):
    _inherit = "res.users"