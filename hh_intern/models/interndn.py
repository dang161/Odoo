# -*- coding: utf-8 -*-

from odoo import models, fields, api
from . import intern_utils
import logging
import xlwt, xlsxwriter, calendar, tempfile, base64
from datetime import datetime

_logger = logging.getLogger(__name__)


class interndn(models.Model):
    _inherit = 'intern.intern'



    note_health = fields.Char("Ghi chú sức khỏe")
    surgery_content = fields.Char("Nội dung Phẫu thuật hay xăm hình")
    educations_vi = fields.One2many("intern.educationvi", "lienket", string="Học tập")  # hh_120
    employments_vi = fields.One2many("intern.employmentvi", "lienket", string="Làm việc")  # hh_121
    family_members_vi = fields.One2many("intern.familyvi", "lienket", string="Gia đình")  # hh_122
    strong = fields.Char('Điểm mạnh')  # hh_124
    weak = fields.Char('Điểm yếu')  # hh_125
    favourite = fields.Char('Sở thích')  # hh_126
    family_income = fields.Integer()  # hh_127
    motivation = fields.Char('Lý do đi nhật')  # hh_128
    income_after_three_year = fields.Integer()  # hh_129
    job_after_return = fields.Char('Sau khi về nước bạn muốn làm công việc gì?')  # hh_130
    prefer_object = fields.Char(string="Nếu nhận mức lương gấp 3 hiện tại bạn muốn mua gì ?")  # hh_131
    memory = fields.Char('Kỷ niệm đáng nhớ nhất của bạn là gì?')  # hh_132
    valuable = fields.Char(string="Điều quý giá nhất đối với bạn trong cuộc sống:")  # hh_133
    family_member = fields.Boolean('Người thân ở nhật')
    family_member_in_jp = fields.Char('Người thân ở nhật')  # hh_134
    notice_name = fields.Char('Chú ý', store=False, compute='_calculate_name')

    @api.multi
    @api.depends('name')
    def _calculate_name(self):
        for rec in self:
            rec.notice_name = ""
            if rec.name:
                tmpName = intern_utils.fix_accent_2(rec.name)
                words = tmpName.split()
                for i, word in enumerate(words):
                    jps = self.env['intern.translator'].search([('vi_word', '=', word.upper())], limit=1)
                    if not jps:
                        rec.notice_name = "Một số từ trong tên TTS không có trong từ điển, vui lòng nhập tên tiếng Nhật của TTS"
                        return

    education_content = fields.Char("Nội dung Tình trạng học tập")
    specialized_vi = fields.Char("Chuyên ngành")
    specialized = fields.Char("Chuyên ngành")
    show_specialized = fields.Boolean(store=False, default=False, compute='certification_change')

    @api.multi
    @api.depends('certification')
    @api.onchange('certification')  # if these fields are changed, call method
    def certification_change(self):
        for rec in self:
            if rec.certification:
                if rec.certification.id == 1:
                    rec.specialized = u'無し'
                    rec.show_specialized = False

                elif rec.certification.id == 2:
                    rec.specialized = u'無し'
                    rec.show_specialized = False
                else:
                    rec.specialized = ""
                    rec.show_specialized = True
            else:
                rec.show_specialized = False


class InternEducationVi(models.Model):
    _name = 'intern.educationvi'
    _inherit = 'intern.education'

    @api.onchange('school_type')  # if these fields are changed, call method
    def school_type_change(self):
        _logger.info("")


class InternEmploymentVi(models.Model):
    _name = 'intern.employmentvi'
    _inherit = 'intern.employment'

    def percentage(part, whole):
        return round(100.0 * float(part) / float(whole), 0)


class InternFamilyVi(models.Model):
    _name = 'intern.familyvi'
    _inherit = 'intern.family'
