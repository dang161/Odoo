# -*- coding: utf-8 -*-

from odoo import models, fields, api


class phongban(models.Model):
    _name = 'phongban.phongban'
    _description = u'Phòng ban'

    room_type = fields.Selection(
        [('0', 'Tuyển dụng'), ('1', 'Phát triển thị trường'), ('2', 'Kiểm soát'), ('3', 'Đối ngoại'),
         ('4', 'Hồ sơ'), ('5', 'Kế toán'), ('6', 'Hành chính NS'), ('7', 'Đào tạo'), ('8', 'Tuyển dụng NS')],
        string="Kiểu Phòng ban")  # hh_188
    name = fields.Char("Tên phòng")  # hh_189
    manager = fields.Many2one('hr.employee', string="Trưởng phòng")  # hh_190
    member_ids = fields.One2many(comodel_name="nhanvien.nhanvien", inverse_name="phongban_nhanvien")  # hh_297
