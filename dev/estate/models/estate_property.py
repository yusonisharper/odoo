from odoo import _, api, fields, models
from odoo.exceptions import UserError, ValidationError
from dateutil import relativedelta
from odoo.tools import float_compare, float_is_zero

class EstateProperty(models.Model):
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
                             required=True, copy=False, default='new', readonly=True)
    active = fields.Boolean('Active', default=True)
    property_type_id = fields.Many2one("estate.property.type", string='Property Type')
    user_id = fields.Many2one('res.users', string='salesman', default=lambda self: self.env.user)
    buyer_id = fields.Many2one('res.partner', string='buyer', readonly=True, copy=False)
    tag_ids = fields.Many2many('estate.property.tag', string='Tag')
    offer_ids = fields.One2many("estate.property.offer", "property_id", string='Offer')

    total_area = fields.Float(string="Total Area", compute='_compute_total')
    best_price = fields.Float(string="Best Offer", compute='_compute_best_price')

    offer_accepted = fields.Boolean(default=False)

    _sql_constraints = [
        ('check_expected_price', 'CHECK(expected_price > 0)', 'The expected_price is strictly a positive number.'),
        ('check_selling_price', 'CHECK(selling_price >= 0)', 'The selling price must be a positive number.'),
    ]

    @api.constrains("expected_price", "selling_price")
    def _check_price_difference(self):
        for prop in self:
            if (
                not float_is_zero(prop.selling_price, precision_rounding=0.01)
                and float_compare(prop.selling_price, prop.expected_price * 90.0 / 100.0, precision_rounding=0.01) < 0
            ):
                raise ValidationError(
                    "The selling price must be at least 90% of the expected price! "
                    + "You must reduce the expected price if you want to accept this offer."
                )

    @api.depends('living_area', 'garden_area')
    def _compute_total(self):
        for record in self:
            record.total_area = record.living_area + record.garden_area

    @api.depends('offer_ids.price')
    def _compute_best_price(self):
        for record in self:
            record.best_price = max(record.offer_ids.mapped('price'), default=0)

    @api.onchange('garden')
    def _onchange_partner(self):
        if self.garden:
            self.garden_area = 10
            self.garden_orientation = 'south'
        else:
            self.garden_area = 0
            self.garden_orientation = None
        # return {'warning': {
        #     'title': _("Warning"),
        #     'message': ('You changed the garden option.')}}

    def cancel(self):
        for record in self:
            if record.state == 'sold':
                raise UserError("Sold property cannot be canceled.")
                continue
            record.state = 'canceled'
        return True

    def sold(self):
        for record in self:
            if record.state == 'canceled':
                raise UserError("Canceled property cannot be sold.")
                continue
            record.state = 'sold'
        return True

    @api.ondelete(at_uninstall=False)
    def _delete(self):
        if any(record.state not in ['new', 'canceled'] for record in self):
            raise UserError("Only new and canceled properties can be delete.")