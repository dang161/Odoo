# -*- coding: utf-8 -*-

from odoo import models, fields, api
from . import intern_utils


class nghiepdoan(models.Model):
    _name = 'nghiepdoan.nghiepdoan'
    _rec_name = 'name_acronym'

    name_acronym = fields.Char("Tên viết tắt - chữ Romaji")  # hh_267
    name_in_jp = fields.Char("Tên đầy đủ - chữ Hán")  # hh_268
    name_in_en = fields.Char("Tên tiếng Anh")  # hh_269
    address_in_jp = fields.Char("Địa chỉ - tiếng Nhật ")  # hh_270
    address_in_romaji = fields.Char("Địa chỉ - chữ ROMAJI")  # hh_271
    post_code = fields.Char("Mã bưu điện (bằng số)")  # hh_272
    license_number = fields.Char("Số giấy phép")  # hh_273
    phone_number = fields.Char("Số điện thoại")  # hh_274
    fax_number = fields.Char("Số fax (nếu có)")  # hh_275
    position_of_responsive_vi = fields.Char("Chức vụ của người đại diện (ký trong hợp đồng)-Tiếng Việt")  # hh_276
    position_of_responsive_jp = fields.Char("Chức vụ của người đại diện (ký trong hợp đồng)-Chữ Hán")  # hh_277
    name_of_responsive_jp = fields.Char("Tên người đại diện - Chữ Hán")  # hh_278
    name_of_responsive_romaji = fields.Char("Tên người đại diện - Chữ Romaji")  # hh_279

    day_sign = fields.Char("Ngày", size=2)  # hh_280
    month_sign = fields.Selection([('01', '01'), ('02', '02'), ('03', '03'), ('04', '04'),
                                   ('05', '05'), ('06', '06'), ('07', '07'), ('08', '08'),
                                   ('09', '09'), ('10', '10'), ('11', '11'), ('12', '12'), ], "Tháng")  # hh_281

    year_sign = fields.Char("Năm", size=4)  # hh_282
    date_sign_agreement = fields.Char("Ngày ký hiệp định giữa Nghiệp đoàn với pháp nhân", store=False,
                                      compute='_date_sign_agreement')  # hh_283

    @api.multi
    @api.depends('day_sign', 'month_sign',
                 'year_sign')
    def _date_sign_agreement(self):
        for rec in self:
            rec.date_sign_agreement = intern_utils.date_time_in_jp(rec.day_sign, rec.month_sign, rec.year_sign)

    fee_training_nd_to_pc = fields.Integer("Phí ủy thác đào tạo (Yên)")  # hh_284

    subsidize_start_month = fields.Integer("Trợ cấp đào tạo tháng đầu(Yên)")  # hh_285

    note_subsize_jp = fields.Char("Ghi chú tiếng Nhật")  # hh_286
    note_subsize_vi = fields.Char("Ghi chú tiếng Việt")  # hh_287
