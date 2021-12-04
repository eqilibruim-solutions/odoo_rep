from odoo.http import request
from odoo import http
import logging


class Openacademy(http.Controller):
    @http.route('/openacademy', auth='public', website=True)
    def index(self, **kw):
        courses = request.env['openacademy.course'].search([], order='create_date desc')
        return request.render('openacademy.list_courses', {
            'courses': courses
        })

    @http.route('/create_course', website=True, auth="user", csrf=False)
    def create_course(self, **post):
        if request.httprequest.method == 'GET':  # if request method is get
            return request.render('openacademy.create_course')  # just return the page with a form
        else:  # if request method is post -> save data to the db
            name, description = post['name'], post.get('description', 'No description here...')
            new_course = request.env['openacademy.course'].sudo().create({
                'name': name,
                'description': description
            })

            return request.redirect('/')

