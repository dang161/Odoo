# -*- coding: utf-8 -*-

from odoo import models, fields, api
from . import intern_utils

class TrainingCenter(models.Model):
    _name = "trainingcenter"
    _description = u'Trung tâm đào tạo'
    _rec_name = 'name_jp'

    name_jp = fields.Char("Tên trung tâm đào tạo - Chữ Hán", required=True)  # hh_226
    address_en = fields.Char("Địa chỉ TTĐT - Tiếng Anh", required=True)  # hh_227

    day_create = fields.Char("Ngày", size=2)  # hh_228
    month_create = fields.Selection([('01', '01'), ('02', '02'), ('03', '03'), ('04', '04'),
                                     ('05', '05'), ('06', '06'), ('07', '07'), ('08', '08'),
                                     ('09', '09'), ('10', '10'), ('11', '11'), ('12', '12'), ], "Tháng")  # hh_229

    year_create = fields.Char("Năm", size=4)  # hh_230

    date_create = fields.Char("Ngày thành lập trung tâm đào tạo", store=False,
                              compute='_date_create')  # hh_231

    @api.multi
    @api.depends('day_create', 'month_create','year_create')
    def _date_create(self):
        for rec in self:
            rec.date_create = intern_utils.date_time_in_jp(rec.date_create, rec.month_create, rec.year_create)

    phone_number = fields.Char("SĐT")  # hh_232
    responsive_person = fields.Char("Người đại diện", required=True)  # hh_233

    mission = fields.Text("Ngành nghề, nhiệm vụ (Tiếng Nhật)")  # hh_234
    number_of_employee = fields.Integer("Số nhân viên")  # hh_235
