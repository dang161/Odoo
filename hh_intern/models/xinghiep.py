# -*- coding: utf-8 -*-
from odoo import models, fields, api

import logging
_logger = logging.getLogger(__name__)

class xinghiep(models.Model):
    _name = 'xinghiep.xinghiep'
    _rec_name = 'name_romaji_enterprise'

    name_vi = fields.Char("Tên xí nghiệp - tiếng Việt")  # hh_288
    name_jp_enterprise = fields.Char("Tên xí nghiệp - Tiếng Hán", required=True)  # hh_289
    name_romaji_enterprise = fields.Char("Tên xí nghiệp - Tiếng Romaji", required=True)  # hh_290
    address_jp_enterprise = fields.Char("Địa chỉ làm việc - Tiếng Hán(lấy từ bảng hợp đồng lương)")  # hh_291
    address_romoji_enterprise = fields.Char(
        "Địa chỉ làm việc - Tiếng Romaji (Tự phiên âm, kiểm tra với khách hàng và PTTT trước khi điền vào HS)")  # hh_292
    phone_number_enterprise = fields.Char("Số điện thoại")  # hh_293
    fax_number_enterprise = fields.Char("Số fax")  # hh_294
    name_of_responsive_jp_enterprise = fields.Char("Tên người đại diện - Tiếng Anh")  # hh_295
    name_of_responsive_en_enterprise = fields.Char("Tên người đại diện - Tiếng Nhật")  # hh_296
    lienket = fields.One2many(comodel_name="intern.invoice", inverse_name="enterprise", required=False,)

    @api.model
    def name_search(self, name, args=None, operator='ilike', limit=100):
        if name:
            args = args or []
            recs = self.search([('name_romaji_enterprise', 'ilike', name)] + args, limit=limit)
            if not recs:
                recs = self.search([('name_jp_enterprise', operator, name)] + args, limit=limit)
            return recs.name_get()
        else:
            return super(xinghiep, self).name_search(name, args, operator, limit)