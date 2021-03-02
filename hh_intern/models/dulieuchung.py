# -*- coding: utf-8 -*-

from odoo import models, fields, api


class School(models.Model):
    _name = 'school'
    _rec_name = 'name_in_vn'

    name_in_vn = fields.Char(string="Tên tiếng việt")  # hh_118
    name_in_jp = fields.Char(string="Tên tiếng Nhật")  # hh_119


class province(models.Model):
    _name = 'province'
    _rec_name = 'name'

    name = fields.Char("Tên có dấu")  # hh_116
    distance_to_hn = fields.Integer("Khoảng cách tới Hà Nội")  # hh_117

    def getDistanceString(self):
        if self.name == u'Hà Nội':
            return u'ハノイ中心から約30分'
        return u"ハノイ中心から約%d時間" % self.distance_to_hn

class JapanProvince(models.Model):
    _name = 'japan.province'
    name = fields.Char('Tên tỉnh')

class certification(models.Model):
    _name = 'intern.certification'
    _description = u'Bằng cấp'
    _rec_name = 'name_in_vn'

    name_in_vn = fields.Char("Tên tiếng Việt")  # hh_114
    name_in_jp = fields.Char("Tên tiếng Nhật")  # hh_115


class translator(models.Model):
    _name = "intern.translator"
    _description = u'Phiên âm tiếng Nhật'
    _rec_name = 'vi_word'
    _sql_constraints = [
        ('vi_word_uniq', 'unique(vi_word)', "Từ này đã tồn tại"),
    ]

    vi_word = fields.Char("Tiếng Việt")  # hh_112
    jp_word = fields.Char("Tiếng Nhật")  # hh_113


class Relation(models.Model):
    _name = 'relation'
    _description = u'Quan hệ với TTS'
    _rec_name = 'relation'
    _sql_constraints = [
        ('relation_uniq', 'unique(relation)', "quan hệ này đã tồn tại"),
    ]

    relation = fields.Char("Tiếng Việt")  # hh_110
    relation_jp = fields.Char("Tiếng Nhật")  # hh_111


class job(models.Model):
    _name = 'intern.job'
    _description = u'Ngành nghề'
    _rec_name = 'name'

    name = fields.Char("Tiếng Việt")  # hh_107
    name_en = fields.Char("Tiếng Anh")  # hh_108
    name_jp = fields.Char("Tiếng Nhật")  # hh_109


class mydocument(models.Model):
    _name = 'intern.document'
    _description = u'Các loại văn bản, báo cáo'
    _rec_name = 'name'

    name = fields.Char("Tên", required=True)  # hh_104

    note = fields.Text("Ghi chú")  # hh_105
    attachment = fields.Binary('Văn bản mẫu', required=True)  # hh_106
