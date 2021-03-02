# -*- coding: utf-8 -*-

from odoo import models, fields, api
import logging
from odoo import tools, _

_logger = logging.getLogger(__name__)


class nhanvien(models.Model):
    _name = 'nhanvien.nhanvien'
    _inherits = {'resource.resource': "resource_id"}

    phongban_nhanvien = fields.Many2one(comodel_name="phongban.phongban")  # hh_401
    name_related = fields.Char(related='resource_id.name', string="Resource Name", readonly=True, store=True)  # hh_402
    gender = fields.Selection([('nam', 'Nam'), ('nu', 'Nữ')], string='Giới tính')  # hh_403
    image = fields.Binary("Ảnh", attachment=True)  # hh_404
    image_medium = fields.Binary("Medium-sized photo", attachment=True)  # hh_405
    image_small = fields.Binary("Small-sized photo", attachment=True)  # hh_406

    @api.model
    def create(self, vals):
        tools.image_resize_images(vals)
        return super(nhanvien, self).create(vals)

    @api.multi
    def write(self, vals):
        tools.image_resize_images(vals)
        return super(nhanvien, self).write(vals)

    @api.onchange('user_id')
    def _onchange_user(self):
        self.name = self.user_id.name

    date_of_birth = fields.Date("Ngày sinh")  # hh_407

    room_type = fields.Selection(
        [('0', 'Tuyển dụng'), ('1', 'Phát triển thị trường'), ('2', 'Kiểm soát'), ('3', 'Đối ngoại'),
         ('4', 'Hồ sơ'), ('5', 'Kế toán'), ('6', 'Hành chính NS'), ('7', 'Đào tạo'), ('8', 'Tuyển dụng NS')],
        string="Kiểu Phòng ban")  # hh_408

    department_id = fields.Many2one('phongban.phongban', string="Phòng")  # hh_409

    #
    @api.multi
    @api.depends('department_id')
    @api.onchange('department_id')
    def onchage_department_id(self):
        for rec in self:
            if rec.department_id:
                rec.room_type = rec.department_id.room_type
