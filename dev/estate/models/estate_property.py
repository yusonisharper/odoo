from odoo import api, fields, models
from dateutil import relativedelta

class estate_property(models.Model):
    _name = "estate.property"
    _description = "estate description"
    _order = "id desc"

    name = fields.Char('Title', required=True, translate=True)
    description = fields.Text('description')
    postcode = fields.Integer('Postcode')
    date_availability = fields.Date('Available from', copy=False, default=fields.date.today() + relativedelta.relativedelta(months=3))
    expected_price = fields.Float('Expected Price', required=True)
    selling_price = fields.Float('Selling Price', copy=False, readonly=True)
    bedrooms = fields.Integer('Bedrooms', default=2)
    living_area = fields.Integer('Living Area')
    facades = fields.Integer('Facades')
    garage = fields.Boolean('Garage')
    garden = fields.Boolean('Garden')
    garden_area = fields.Integer('Garden Area')
    garden_orientation = fields.Selection(string='Garden Orientation',
                                          selection=[('north', 'North'), ('south', 'South'), ('east', 'East'), ('west', 'West')])
    state = fields.Selection(string='Status', selection=[('new', 'New'), ('offer_received', 'Offer Received'),
                                                  ('offer_accepted', 'Offer Accepted'), ('sold', 'Sold'), ('canceled', 'Canceled')],
                             required=True, copy=False, default='new')
    active = fields.Boolean('Active', default=True)
    property_type_id = fields.Many2one("estate.property.type", string='Property Type')
    user_id = fields.Many2one('res.users', string='salesman', default=lambda self: self.env.user)
    buyer_id = fields.Many2one('res.partner', string='buyer', readonly=True, copy=False)
    tag_ids = fields.Many2many('estate.property.tag', string='Tag')
    offer_ids = fields.One2many("estate.property.offer", "property_id", string='Offer')

    total_area = fields.Float(string="Total Area", compute='_compute_total')
    best_price = fields.Float(string="Best Offer", compute='_compute_best_price')

    @api.depends('living_area', 'garden_area')
    def _compute_total(self):
        for record in self:
            record.total_area = record.living_area + record.garden_area

    @api.depends('offer_ids.price')
    def _compute_best_price(self):
        for record in self:
            record.best_price = max(record.offer_ids.mapped('price'), default=0)