# -*- coding: utf-8 -*-

from odoo import models, fields, api


class DispatchCom1(models.Model):
    _name = 'dispatchcom1'
    _rec_name = 'name_short'
    _description = u'Công ty phái cử thứ nhất'


    name_short = fields.Char("Tên thường gọi")  # hh_236
    name_jp = fields.Char("Pháp nhân - Chữ Hán", required=True)  # hh_237
    name_en = fields.Char("Pháp nhân - Tiếng Anh", required=True)  # hh_238
    name = fields.Char("Pháp nhân - Tiếng Việt", required=True)  # hh_239
    director = fields.Char("Tên người đại diện", required=True)  # hh_240
    position_director = fields.Char("Chức vụ (Tiếng Nhật)", default=u'社長', required=True)  # hh_241
    position_director_vi = fields.Char("Chức vụ (Tiếng Việt)", default=u'Giám đốc', required=True)  # hh_242
    address_vi = fields.Char("Địa chỉ công ty - Tiếng Việt", required=True)  # hh_243
    address_en = fields.Char("Địa chỉ công ty - tiếng Anh (Thư TC tiếng Nhật)", required=True)  # hh_244
    phone_number = fields.Char("Số điện thoại")  # hh_245
    fax_number = fields.Char("Số fax")  # hh_246
    license_number = fields.Char("Số giấy phép")  # hh_247
    day_create = fields.Char("Ngày", size=2, required=True)  # hh_252
    month_create = fields.Selection([('01', '01'), ('02', '02'), ('03', '03'), ('04', '04'),
                                     ('05', '05'), ('06', '06'), ('07', '07'), ('08', '08'),
                                     ('09', '09'), ('10', '10'), ('11', '11'), ('12', '12'), ], "Tháng",
                                    required=True)  # hh_253

    year_create = fields.Char("Năm", size=4, required=True) #hh_254

    date_create = fields.Char("Ngày thành lập công ty", store=False,
                              compute='_date_create') #hh_255

    @api.multi
    @api.depends('day_create', 'month_create',
                 'year_create')
    def _date_create(self):
        for rec in self:
            if rec.day_create and rec.month_create and rec.year_create:
                rec.date_create = u"Ngày %s tháng %s năm %s" % (
                    rec.day_create, rec.month_create,
                    rec.year_create)
            elif rec.month_create and rec.year_create:
                rec.date_create = u"Tháng %s năm %s" % (
                    rec.month_create, rec.year_create)
            elif rec.year_create:
                rec.date_create = u'Năm %s' % rec.year_create
            else:
                rec.date_create = ""

    mission = fields.Text("Ngành nghề, nhiệm vụ (Tiếng Nhật)")  # hh_248
    number_of_employee = fields.Integer("Số nhân viên")  # hh_249
    capital = fields.Char("Tiền vốn (Tiếng Nhật)")  # hh_250
    revenue = fields.Char("Doanh thu (Tiếng Nhật)")  # hh_251
