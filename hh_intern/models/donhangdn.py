# -*- coding: utf-8 -*-

from odoo import models, fields, api
import datetime


class doingoai(models.Model):
    _inherit = 'intern.invoice'

    day_departure_doc = fields.Char("Ngày", size=2)
    month_departure_doc = fields.Selection([('01', '01'), ('02', '02'), ('03', '03'), ('04', '04'),
                                            ('05', '05'), ('06', '06'), ('07', '07'), ('08', '08'),
                                            ('09', '09'), ('10', '10'), ('11', '11'), ('12', '12'), ], "Tháng")

    year_departure_doc = fields.Char("Năm", size=4, default=lambda self: self._get_current_year())

    date_departure_doc = fields.Char("Ngày xuất cảnh Dự kiến", store=False, compute='_date_departure_doc')

    @api.multi
    @api.depends('day_departure_doc', 'month_departure_doc', 'year_departure_doc')
    def _date_departure_doc(self):
        for rec in self:
            if rec.day_departure_doc and rec.month_departure_doc and rec.year_departure_doc:
                rec.date_departure_doc = u"Ngày %s tháng %s năm %s" % (
                    rec.day_departure_doc, rec.month_departure_doc, rec.year_departure_doc)
            elif rec.month_departure_doc and rec.year_departure_doc:
                rec.date_departure_doc = u"Tháng %s năm %s" % (
                    rec.month_departure_doc, rec.year_departure_doc)
            elif rec.year_departure_doc:
                rec.date_departure_doc = u'Năm %s' % rec.year_departure_doc
            else:
                rec.date_departure_doc = ""

    date_pass = fields.Date("Ngày trúng tuyển")  # hh_224
    date_join_school = fields.Date('Ngày nhập học trúng tuyển')  # hh_225
    hoso_created = fields.Boolean('Đơn hàng của HS')  # hh_223

    date_departure = fields.Date("Ngày xuất cảnh Dự kiến")  # hh_154

    # Hàm tính thời gian 7 ngày sau
    # @api.onchange('date_departure')
    # def onchange_method_date_departure(self):
    #     if self.date_departure:
    #         start = datetime.datetime.now()
    #         end = start + datetime.timedelta(days=7)
    #         date_array = (start + datetime.timedelta(days=x) for x in range(0, (end - start).days))
    #         print(date_array)
    #         for item in date_array:
    #             print(item)
    date_departure2 = fields.Date("Ngày xuất cảnh 3 năm sau")

    @api.onchange('date_departure')
    def _date_departure(self):
        if self.date_departure:
            startDate = self.date_departure
            endDate = datetime.date(startDate.year + 3, startDate.month, startDate.day)
            self.date_departure2 = endDate
            print(self.date_departure2)

    @api.multi
    def download_pass_report(self):
        arr = []

        for record in self.interns_pass_new:
            arr.append((record.id))
        arrs = str(arr).replace('[', '(')
        arrss = str(arrs).replace(']', ')')
        file = self.interns_pass_new.action_export_excel_dn(arr, arrss, self.id)
        url = '/web/content/overtime.report.store/%s/save_file/DS trúng tuyển chính thức.xls?download=true' % file.id
        return {
            'type': 'ir.actions.act_window',
            'res_model': 'download.file',
            'view_mode': 'form',
            'view_type': 'form',
            'views': [(False, 'form')],
            'target': 'new',
            'context': {'default_link': url}
        }

    @api.multi
    def download_db_report(self):
        arr = []

        for record in self.interns_preparatory:
            arr.append((record.id))
        arrs = str(arr).replace('[', '(')
        arrss = str(arrs).replace(']', ')')
        file = self.interns_preparatory.action_export_excel_dn_db(arr, arrss, self.id)
        url = '/web/content/overtime.report.store/%s/save_file/DS trúng tuyển dự bị.xls?download=true' % file.id
        return {
            'type': 'ir.actions.act_window',
            'res_model': 'download.file',
            'view_mode': 'form',
            'view_type': 'form',
            'views': [(False, 'form')],
            'target': 'new',
            'context': {'default_link': url}
        }

    @api.multi
    def download_huy_report(self):
        arr = []

        for record in self.interns_cancel_pass:
            arr.append((record.id))
        arrs = str(arr).replace('[', '(')
        arrss = str(arrs).replace(']', ')')
        file = self.interns_cancel_pass.action_export_excel_dn_huy(arr, arrss, self.id)
        url = '/web/content/overtime.report.store/%s/save_file/DS hủy sau trúng tuyển.xls?download=true' % file.id
        return {
            'type': 'ir.actions.act_window',
            'res_model': 'download.file',
            'view_mode': 'form',
            'view_type': 'form',
            'views': [(False, 'form')],
            'target': 'new',
            'context': {'default_link': url}
        }
