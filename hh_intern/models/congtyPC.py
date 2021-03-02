# -*- coding: utf-8 -*-

from odoo import models, fields, api

class hoso(models.Model):
    _name = 'hoso.hoso'
    _rec_name = 'name'

    name = fields.Char(u"Tên công ty (Tiếng Anh)", required=True)  # hh_256
    name_vn = fields.Char(u"Tên công ty (Tiếng Việt)", required=True)  # hh_257
    address = fields.Char(u"Địa chỉ công ty (Tiếng Anh)", required=True)  # hh_258
    director = fields.Char(u"Tên giám đốc công ty (Tiếng Việt)", required=True)  # hh_259
    position_person_sign = fields.Char(u"Chức danh của ký thư PC (Tiếng Nhật)", required=True)  # hh_260
    phone_number = fields.Char(u"Số ĐT", required=True)  # hh_261
    fax_number = fields.Char(u"Số fax")  # hh_262
    day_create = fields.Char(u"Ngày", size=2, required=True)  # hh_263
    month_create = fields.Selection([('01', '01'), ('02', '02'), ('03', '03'), ('04', '04'),
                                     ('05', '05'), ('06', '06'), ('07', '07'), ('08', '08'),
                                     ('09', '09'), ('10', '10'), ('11', '11'), ('12', '12'), ], "Tháng",
                                    required=True)  # hh_264

    year_create = fields.Char(u"Năm", size=4, required=True)  # hh_265

    date_create = fields.Char("Ngày thành lập công ty", store=False,
                              compute='_date_create')  # hh_266

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
