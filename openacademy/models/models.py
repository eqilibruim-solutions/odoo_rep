from odoo.exceptions import ValidationError
from odoo import models, fields, api
import logging


class ResUserInherit(models.Model):
    _inherit = 'res.users'

    responsible_for_courses = fields.One2many('openacademy.course', 'responsible_user', string='Responsible for courses')


class ResPartnerInherit(models.Model):
    _inherit = 'res.partner'

    sessions = fields.One2many('openacademy.session', 'instructor', string='Session Instructor')
    is_instructor = fields.Boolean('Is Instructor?', default=False)


class Course(models.Model):
    _name = 'openacademy.course'
    _description = 'Contains full information about course'
    _sql_constraints = [
        ('different_course_name_and_desc', 'name != description', 'Name and description must be defferent!'),
        ('unique_course_name', 'UNIQUE(name)', 'Name of the course must be unique. Choose another name!')
    ]

    name = fields.Char('Course\'s name', required=True)
    description = fields.Html('Course\'s description')
    sessions = fields.One2many('openacademy.session', 'course', string='Session')
    responsible_user = fields.Many2one('res.users', string='Responsible User')


class Session(models.Model):
    _name='openacademy.session'
    _description = 'Contains data about course session: it\'s name, start date and duration'

    name = fields.Char('Session\'s name', related='course.name')
    start_date = fields.Datetime('Start Date', default=fields.Datetime.now())
    duration = fields.Integer('Session duration (hours)')
    seats = fields.Integer('Seats number')
    course = fields.Many2one('openacademy.course', ondelete='cascade', string='Course')
    active = fields.Boolean('Is Active?', default=True)
    instructor = fields.Many2one('res.partner', ondelete='cascade', string='Instructor')
    participants = fields.Many2many('res.partner', 'session_partner_rel_participants', 'session_id', 'partner_id', string='Participants')
    taken_seats = fields.Integer('% of Taken Seats', compute='_compute_taken_seats')

    @api.depends('participants', 'seats')
    def _compute_taken_seats(self):
        for r in self:
            if r.seats == 0 and len(r.participants) == 0:  # Just opened form
                return

            r.taken_seats = 100 - int(((r.seats - len(r.participants)) * 100) / r.seats)

    @api.onchange('seats', 'participants', 'duration')
    def _onchange_session_callback(self):
        if self.seats < 0:
            return {
                'warning': {'title': 'Invalid number', 'message': 'The number of seats must be positive!'}
            }

        if len(self.participants) > self.seats:
            return {
                'warning': {'title': 'Extra participant', 'message': 'There are no more available seats!'}
            }

        if self.duration < 0:
            return {
                'warning': {'title': 'Invalid number', 'message': 'Сourse duration must be a positive number!'}
            }

    @api.constrains('participants')
    def _check_instructor_in_participants(self):
        for r in self:
            if r.instructor.id in r.participants.ids:
                # if list of participants' ids contains id of the instructor
                raise ValidationError('An instructor of the course must not be in participants!')

