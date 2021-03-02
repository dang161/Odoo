from odoo import models, fields, api
from datetime import datetime
from dateutil.relativedelta import relativedelta
from . import intern_utils
import xlwt, xlsxwriter, calendar, tempfile, base64
import logging

_logger = logging.getLogger(__name__)


class InternInvoice(models.Model):
    _name = 'intern.internclone'
    _inherits = {'intern.intern': 'intern_id'}
    _description = 'TTS theo đơn hàng'
    _rec_name = 'intern_id'

    _sql_constraints = [('unique_invoice', 'unique(intern_id, invoice_id)',
                         'Lỗi trùng TTS trong danh sách dự kiến tiến cử. F5 nếu bạn ko thấy.')]

    intern_id = fields.Many2one('intern.intern', required=True, on_delete='restrict', auto_join=True,
                                string='Thực tập sinh', help='Intern-related data of the user', index=True)
    invoice_id = fields.Many2many('intern.invoice', relation="intern_invoice_rel", column1="invoice_id",
                                  column2="intern_id", string='Đơn hàng tiến cử')
    # invoice_id = fields.Many2one("intern.invoice", string='Đơn hàng', on_delete='cascade', index=True)

    status = fields.Selection(
        [(4, 'Khởi tạo'), (5, 'Tiến cử'), (1, 'Thi tuyển'), (2, 'Chốt Trúng tuyển'), (3, 'Hoàn thành'),
         (6, 'Tạm dừng'), (7, 'Huỷ bỏ')], store=True, related='invoice_id.status')

    promoted = fields.Boolean('Tiến cử')

    @api.multi
    def action_export_excel(self, arr, arrss, id_invoice):
        emp_obj = self.env['intern.internclone'].search([('id', 'in', arr)])
        print(id_invoice)
        inv = self.env['intern.invoice'].search([('id', '=', id_invoice)])
        wb = xlwt.Workbook(encoding='latin-1')
        sheet1 = wb.add_sheet(u'Nhóm tài chính 1', cell_overwrite_ok=True)
        sheets = [sheet1]
        style = xlwt.easyxf(
            'font: bold on,color black,height 250;align: wrap on,vert centre, horiz center;')
        style_header = xlwt.easyxf('font: bold on,color black,height 200;align: wrap yes,vert centre, horiz center;pattern: pattern solid, \
                                           fore-colour light_orange ;border: left thin,right thin,top thin,bottom thin')
        style_font = xlwt.easyxf('align: wrap yes,vert centre, horiz center;pattern: pattern solid, \
                                           fore-colour white;border: left thin,right thin,top thin,bottom thin')

        report_name = u'Danh sách tiến cử đơn hàng %s' % str(inv.name)
        start_line = 2
        top_row = 0
        bottom_row = 0
        left_column = 4
        right_column = 9

        sheet1.write(top_row, left_column, report_name, style)
        sheet1.merge(top_row, bottom_row, left_column, right_column)
        self.env.cr.execute("""select * from intern_internclone where id in %s""" % str(arrss))
        employee_lst = self.env.cr.fetchall()

        self.env.cr.execute("""select distinct id from intern_internclone where id in %s""" % str(arrss))
        employee_ot_length = self.env.cr.fetchall()
        table_header = ['STT', 'Họ và tên', 'Giới tính', 'Mã số', 'Ngày NH', 'Năm sinh', 'Tuổi',
                        'Cao', 'Nặng', 'Nhóm máu', 'Thị lực', 'Tình trạng HN', 'Trình độ học vấn', 'TB', 'Quê quán',
                        'CBTD']
        botttom_cell = 0
        for i in range(len(table_header)):
            for s in range(len(sheets)):
                sheets[s].row(i).height = 510
                sheets[s].write(start_line, i, table_header[i], style_header)

        start_line += 1
        stt = 1
        print_list = []
        flag = 3
        reset_line1, reset_line2, reset_line3, reset_line4, reset_line5, reset_line6, reset_line7, reset_line8 = 0, 0, 0, 0, 0, 0, 0, 0
        start_line1, start_line2, start_line3, start_line4, start_line5, start_line6, start_line7, start_line8 = start_line, start_line, start_line, start_line, start_line, start_line, start_line, start_line
        print(employee_ot_length, 'employee_ot_length')
        for i in employee_ot_length:
            for s in range(len(sheets)):
                sheets[s].row(start_line).height = 510 * 510
            print(emp_obj, 'emp_obj')
            for rec in emp_obj:
                if i[0] == rec.id:
                    employee_lst_bk = employee_lst
                    strr = "Trái : " + str(rec.vision_left) + " Phải " + str(rec.vision_right) + ""
                    sttrr = "'" + str(rec.date_enter_source) + "'"

                    # for n, i in enumerate(print_list):
                    #             if i == False:
                    #                 print_list[n] = None

                    for e in employee_lst_bk:
                        rec.name, rec.gender, rec.custom_id, sttrr, rec.date_of_birth_short, rec.age, rec.height, strr, rec.marital_status.name_in_vn, rec.certification.name_in_vn, rec.iq_percentage, rec.province.name, rec.recruitment_employee.name
                        print_list = [stt, rec.name, rec.gender, rec.custom_id, sttrr,
                                      rec.date_of_birth_short,
                                      rec.age, rec.height,
                                      rec.weight, rec.blood_group, strr, rec.marital_status.name_in_vn,
                                      rec.certification.name_in_vn, rec.iq_percentage, rec.province.name,
                                      rec.recruitment_employee.name
                                      ]
                        print(print_list, 'Ngay sinh')

            if reset_line1 == 0:
                reset_line1 = 1
                start_line1 = 4
            # print_list[0] = start_line1 - flag
            for x in range(len(print_list)):
                sheet1.write(start_line1, x, print_list[x], style_font)
            start_line1 += 1

        file_path = tempfile.gettempdir() + r"/OT_report_{id_invoice}.xls"
        wb.save(file_path)
        file = self.env['overtime.report.store'].create({'save_file': base64.b64encode(open(file_path, 'rb').read())})
        # print(file.id)
        # print(file.save_file)
        # print('/web/content/overtime.report.store/%s/save_file/bao_cao_lam_them.xls' % file.id)
        return file

    @api.multi
    def action_export_excel_tt(self, arr, arrss, id_invoice):

        emp_obj = self.env['intern.internclone'].search([('id', 'in', arr)])
        inv = self.env['intern.invoice'].search([('id', '=', id_invoice)])

        wb = xlwt.Workbook(encoding='latin-1')
        sheet1 = wb.add_sheet(u'Nhóm tài chính 1', cell_overwrite_ok=True)

        sheets = [sheet1]
        style = xlwt.easyxf(
            'font: bold on,color black,height 250;align: wrap on,vert centre, horiz center;')
        style_header = xlwt.easyxf('font: bold on,color black,height 200;align: wrap yes,vert centre, horiz center;pattern: pattern solid, \
                                               fore-colour light_orange ;border: left thin,right thin,top thin,bottom thin')
        style_font = xlwt.easyxf('align: wrap yes,vert centre, horiz center;pattern: pattern solid, \
                                               fore-colour white;border: left thin,right thin,top thin,bottom thin')
        report_name = u'Danh sách thi tuyển đơn hàng %s' % str(inv.name)
        start_line = 2

        top_row = 0
        bottom_row = 0
        left_column = 4
        right_column = 9

        sheet1.write(top_row, left_column, report_name, style)
        sheet1.merge(top_row, bottom_row, left_column, right_column)

        self.env.cr.execute("""select * from intern_internclone where id in %s""" % str(arrss))
        employee_lst = self.env.cr.fetchall()

        self.env.cr.execute("""select distinct id from intern_internclone where id in %s""" % str(arrss))
        employee_ot_length = self.env.cr.fetchall()
        table_header = ['STT', 'Họ và tên', 'Giới tính', 'Mã số', 'Ngày NH', 'Năm sinh', 'Tuổi',
                        'Cao', 'Nặng', 'Nhóm máu', 'Thị lực', 'Tình trạng HN', 'Trình độ học vấn', 'TB', 'Quê quán',
                        'CBTD']
        botttom_cell = 0
        for i in range(len(table_header)):
            for s in range(len(sheets)):
                sheets[s].row(i).height = 510
                sheets[s].write(start_line, i, table_header[i], style_header)

        start_line += 1
        stt = 1
        print_list = []
        flag = 3
        reset_line1, reset_line2, reset_line3, reset_line4, reset_line5, reset_line6, reset_line7, reset_line8 = 0, 0, 0, 0, 0, 0, 0, 0
        start_line1, start_line2, start_line3, start_line4, start_line5, start_line6, start_line7, start_line8 = start_line, start_line, start_line, start_line, start_line, start_line, start_line, start_line
        print(employee_ot_length, 'employee_ot_length')
        for i in employee_ot_length:
            for s in range(len(sheets)):
                sheets[s].row(start_line).height = 510 * 510
            print(emp_obj, 'emp_obj')
            for rec in emp_obj:
                if i[0] == rec.id:
                    employee_lst_bk = employee_lst
                    strr = "Trái : " + str(rec.vision_left) + " Phải " + str(rec.vision_right) + ""
                    sttrr = "'" + str(rec.date_enter_source) + "'"

                    for e in employee_lst_bk:
                        rec.name, rec.gender, rec.custom_id, sttrr, rec.date_of_birth_short, rec.age, rec.height, strr, rec.marital_status.name_in_vn, rec.certification.name_in_vn, rec.iq_percentage, rec.province.name, rec.recruitment_employee.name
                        print_list = [stt, rec.name, rec.gender, rec.custom_id, sttrr,
                                      rec.date_of_birth_short,
                                      rec.age, rec.height,
                                      rec.weight, rec.blood_group, strr, rec.marital_status.name_in_vn,
                                      rec.certification.name_in_vn, rec.iq_percentage, rec.province.name,
                                      rec.recruitment_employee.name
                                      ]

            if reset_line1 == 0:
                reset_line1 = 1
                start_line1 = 4
            # print_list[0] = start_line1 - flag
            for x in range(len(print_list)):
                sheet1.write(start_line1, x, print_list[x], style_font)
            start_line1 += 1

        file_path = tempfile.gettempdir() + r"/OT_report_{id_invoice}.xls"
        wb.save(file_path)
        file = self.env['overtime.report.store'].create({'save_file': base64.b64encode(open(file_path, 'rb').read())})
        # print(file.id)
        # print(file.save_file)
        # print('/web/content/overtime.report.store/%s/save_file/bao_cao_lam_them.xls' % file.id)
        return file

    @api.multi
    def action_export_excel_dn(self, arr, arrss, id_invoice):

        emp_obj = self.env['intern.internclone'].search([('id', 'in', arr)])
        inv = self.env['intern.invoice'].search([('id', '=', id_invoice)])
        wb = xlwt.Workbook(encoding='latin-1')
        sheet1 = wb.add_sheet(u'Nhóm tài chính 1', cell_overwrite_ok=True)

        sheets = [sheet1]
        style = xlwt.easyxf(
            'font: bold on,color black,height 250;align: wrap on,vert centre, horiz center;')
        style_header = xlwt.easyxf('font: bold on,color black,height 200;align: wrap yes,vert centre, horiz center;pattern: pattern solid, \
                                                   fore-colour light_orange ;border: left thin,right thin,top thin,bottom thin')
        style_font = xlwt.easyxf('align: wrap yes,vert centre, horiz center;pattern: pattern solid, \
                                                   fore-colour white;border: left thin,right thin,top thin,bottom thin')
        report_name = u'DS trúng tuyển chính thức đơn hàng  %s' % str(inv.name)
        start_line = 2

        top_row = 0
        bottom_row = 0
        left_column = 4
        right_column = 9

        sheet1.write(top_row, left_column, report_name, style)
        sheet1.merge(top_row, bottom_row, left_column, right_column)

        self.env.cr.execute("""select * from intern_invoice where id in %s""" % str(arrss))
        employee_lst = self.env.cr.fetchall()

        self.env.cr.execute("""select distinct id from intern_internclone where id in %s""" % str(arrss))
        employee_ot_length = self.env.cr.fetchall()
        table_header = ['STT', 'Mã số', 'Họ và tên', 'Giới tính', 'Năm sinh', 'Quê quán', 'CBTD',
                        'Phòng TD', 'Xí nghiệp', 'Nghiệp Đoàn', 'Địa chỉ làm việc', 'Ngành nghề', 'Hạn HD',
                        'Ngày trúng tuyển', 'Ngày NH trúng tuyển',
                        'Ngày dự kiến xuất cảnh', 'Pháp nhân']
        botttom_cell = 0
        for i in range(len(table_header)):
            for s in range(len(sheets)):
                sheets[s].row(i).height = 510
                sheets[s].write(start_line, i, table_header[i], style_header)

        start_line += 1
        stt = 1
        print_list = []
        flag = 3
        reset_line1, reset_line2, reset_line3, reset_line4, reset_line5, reset_line6, reset_line7, reset_line8 = 0, 0, 0, 0, 0, 0, 0, 0
        start_line1, start_line2, start_line3, start_line4, start_line5, start_line6, start_line7, start_line8 = start_line, start_line, start_line, start_line, start_line, start_line, start_line, start_line
        print(employee_ot_length, 'employee_ot_length')
        for i in employee_ot_length:
            for s in range(len(sheets)):
                sheets[s].row(start_line).height = 510 * 510
            print(emp_obj, 'emp_obj')
            for rec in emp_obj:
                if i[0] == rec.id:
                    employee_lst_bk = employee_ot_length
                    sttr = "'" + str(rec.invoices_promoted.date_departure) + "'"
                    sttr1 = "'" + str(rec.invoices_promoted.date_pass) + "'"
                    sttrr2 = "'" + str(rec.invoices_promoted.date_join_school) + "'"

                    for e in employee_lst_bk:
                        rec.custom_id, rec.name, rec.gender, rec.date_of_birth_short, rec.province.name, rec.recruitment_employee.name, rec.room_recruitment.name, rec.enterprise.name_romaji_enterprise, rec.invoices_promoted.guild.name_acronym, rec.place_to_work.name, rec.invoices_promoted.job_predefine.name
                        print_list = [stt, rec.custom_id, rec.name, rec.gender, rec.date_of_birth_short,
                                      rec.province.name,
                                      rec.recruitment_employee.name, rec.room_recruitment.name,
                                      rec.enterprise.name_romaji_enterprise, rec.invoices_promoted.guild.name_acronym,
                                      rec.place_to_work.name, rec.invoices_promoted.job_predefine.name,
                                      rec.invoices_promoted.year_expire, sttr1, sttrr2, sttr,
                                      rec.invoices_promoted.dispatchcom1.name_short
                                      ]

            if reset_line1 == 0:
                reset_line1 = 1
                start_line1 = 4
            for x in range(len(print_list)):
                sheet1.write(start_line1, x, print_list[x], style_font)
            start_line1 += 1

        file_path = tempfile.gettempdir() + r"/OT_report_{id_invoice}.xls"
        wb.save(file_path)
        file = self.env['overtime.report.store'].create({'save_file': base64.b64encode(open(file_path, 'rb').read())})
        # print(file.id)
        # print(file.save_file)
        # print('/web/content/overtime.report.store/%s/save_file/bao_cao_lam_them.xls' % file.id)
        return file

    def action_export_excel_dn_db(self, arr, arrss, id_invoice):

        emp_obj = self.env['intern.internclone'].search([('id', 'in', arr)])
        inv = self.env['intern.invoice'].search([('id', '=', id_invoice)])
        wb = xlwt.Workbook(encoding='latin-1')
        sheet1 = wb.add_sheet(u'Nhóm tài chính 1', cell_overwrite_ok=True)

        sheets = [sheet1]
        style = xlwt.easyxf(
            'font: bold on,color black,height 250;align: wrap on,vert centre, horiz center;')
        style_header = xlwt.easyxf('font: bold on,color black,height 200;align: wrap yes,vert centre, horiz center;pattern: pattern solid, \
                                                   fore-colour light_orange ;border: left thin,right thin,top thin,bottom thin')
        style_font = xlwt.easyxf('align: wrap yes,vert centre, horiz center;pattern: pattern solid, \
                                                   fore-colour white;border: left thin,right thin,top thin,bottom thin')
        report_name = u'DS trúng tuyển dự bị đơn hàng  %s' % str(inv.name)
        start_line = 2

        top_row = 0
        bottom_row = 0
        left_column = 4
        right_column = 9

        sheet1.write(top_row, left_column, report_name, style)
        sheet1.merge(top_row, bottom_row, left_column, right_column)

        self.env.cr.execute("""select * from intern_invoice where id in %s""" % str(arrss))
        employee_lst = self.env.cr.fetchall()

        self.env.cr.execute("""select distinct id from intern_internclone where id in %s""" % str(arrss))
        employee_ot_length = self.env.cr.fetchall()
        table_header = ['STT', 'Mã số', 'Họ và tên', 'Giới tính', 'Năm sinh', 'Quê quán', 'CBTD',
                        'Phòng TD', 'Xí nghiệp', 'Nghiệp Đoàn', 'Địa chỉ làm việc', 'Ngành nghề', 'Hạn HD',
                        'Ngày trúng tuyển', 'Ngày NH trúng tuyển',
                        'Ngày dự kiến xuất cảnh', 'Pháp nhân']
        botttom_cell = 0
        for i in range(len(table_header)):
            for s in range(len(sheets)):
                sheets[s].row(i).height = 510
                sheets[s].write(start_line, i, table_header[i], style_header)

        start_line += 1
        stt = 1
        print_list = []
        flag = 3
        reset_line1, reset_line2, reset_line3, reset_line4, reset_line5, reset_line6, reset_line7, reset_line8 = 0, 0, 0, 0, 0, 0, 0, 0
        start_line1, start_line2, start_line3, start_line4, start_line5, start_line6, start_line7, start_line8 = start_line, start_line, start_line, start_line, start_line, start_line, start_line, start_line
        print(employee_ot_length, 'employee_ot_length')
        for i in employee_ot_length:
            for s in range(len(sheets)):
                sheets[s].row(start_line).height = 510 * 510
            print(emp_obj, 'emp_obj')
            for rec in emp_obj:
                if i[0] == rec.id:
                    employee_lst_bk = employee_ot_length
                    # strr = "Trái : " + str(rec.vision_left) + " Phải " + str(rec.vision_right) + ""
                    sttr = "'" + str(rec.invoices_promoted.date_departure) + "'"
                    sttr1 = "'" + str(rec.invoices_promoted.date_pass) + "'"
                    sttrr2 = "'" + str(rec.invoices_promoted.date_join_school) + "'"

                    for e in employee_lst_bk:
                        rec.custom_id, rec.name, rec.gender, rec.date_of_birth_short, rec.province.name, rec.recruitment_employee.name, rec.room_recruitment.name, rec.enterprise.name_romaji_enterprise, rec.invoices_promoted.guild.name_acronym, rec.place_to_work.name, rec.invoices_promoted.job_predefine.name
                        print_list = [stt, rec.custom_id, rec.name, rec.gender, rec.date_of_birth_short,
                                      rec.province.name,
                                      rec.recruitment_employee.name, rec.room_recruitment.name,
                                      rec.enterprise.name_romaji_enterprise, rec.invoices_promoted.guild.name_acronym,
                                      rec.place_to_work.name, rec.invoices_promoted.job_predefine.name,
                                      rec.invoices_promoted.year_expire, sttr1, sttrr2, sttr,
                                      rec.invoices_promoted.dispatchcom1.name_short
                                      ]

            if reset_line1 == 0:
                reset_line1 = 1
                start_line1 = 4
            # print_list[0] = start_line1 - flag
            for x in range(len(print_list)):
                sheet1.write(start_line1, x, print_list[x], style_font)
            start_line1 += 1

        file_path = tempfile.gettempdir() + r"/OT_report_{id_invoice}.xls"
        wb.save(file_path)
        file = self.env['overtime.report.store'].create({'save_file': base64.b64encode(open(file_path, 'rb').read())})
        # print(file.id)
        # print(file.save_file)
        # print('/web/content/overtime.report.store/%s/save_file/bao_cao_lam_them.xls' % file.id)
        return file

    def action_export_excel_dn_huy(self, arr, arrss, id_invoice):

        emp_obj = self.env['intern.internclone'].search([('id', 'in', arr)])
        inv = self.env['intern.invoice'].search([('id', '=', id_invoice)])
        wb = xlwt.Workbook(encoding='latin-1')
        sheet1 = wb.add_sheet(u'Nhóm tài chính 1', cell_overwrite_ok=True)

        sheets = [sheet1]
        style = xlwt.easyxf(
            'font: bold on,color black,height 250;align: wrap on,vert centre, horiz center;')
        style_header = xlwt.easyxf('font: bold on,color black,height 200;align: wrap yes,vert centre, horiz center;pattern: pattern solid, \
                                                   fore-colour light_orange ;border: left thin,right thin,top thin,bottom thin')
        style_font = xlwt.easyxf('align: wrap yes,vert centre, horiz center;pattern: pattern solid, \
                                                   fore-colour white;border: left thin,right thin,top thin,bottom thin')
        report_name = u'DS hủy sau trúng tuyển đơn hàng %s' % str(inv.name)
        start_line = 2

        top_row = 0
        bottom_row = 0
        left_column = 4
        right_column = 9

        sheet1.write(top_row, left_column, report_name, style)
        sheet1.merge(top_row, bottom_row, left_column, right_column)

        self.env.cr.execute("""select * from intern_invoice where id in %s""" % str(arrss))
        employee_lst = self.env.cr.fetchall()

        self.env.cr.execute("""select distinct id from intern_internclone where id in %s""" % str(arrss))
        employee_ot_length = self.env.cr.fetchall()
        table_header = ['STT', 'Mã số', 'Họ và tên', 'Giới tính', 'Năm sinh', 'Quê quán', 'CBTD',
                        'Phòng TD', 'Xí nghiệp', 'Nghiệp Đoàn', 'Địa chỉ làm việc', 'Ngành nghề', 'Hạn HD',
                        'Ngày trúng tuyển', 'Ngày NH trúng tuyển',
                        'Ngày dự kiến xuất cảnh', 'Pháp nhân']
        botttom_cell = 0
        for i in range(len(table_header)):
            for s in range(len(sheets)):
                sheets[s].row(i).height = 510
                sheets[s].write(start_line, i, table_header[i], style_header)

        start_line += 1
        stt = 1
        print_list = []
        flag = 3
        reset_line1, reset_line2, reset_line3, reset_line4, reset_line5, reset_line6, reset_line7, reset_line8 = 0, 0, 0, 0, 0, 0, 0, 0
        start_line1, start_line2, start_line3, start_line4, start_line5, start_line6, start_line7, start_line8 = start_line, start_line, start_line, start_line, start_line, start_line, start_line, start_line
        print(employee_ot_length, 'employee_ot_length')
        for i in employee_ot_length:
            for s in range(len(sheets)):
                sheets[s].row(start_line).height = 510 * 510
            print(emp_obj, 'emp_obj')
            for rec in emp_obj:
                if i[0] == rec.id:
                    employee_lst_bk = employee_ot_length
                    # strr = "Trái : " + str(rec.vision_left) + " Phải " + str(rec.vision_right) + ""
                    sttr = "'" + str(rec.invoices_promoted.date_departure) + "'"
                    sttr1 = "'" + str(rec.invoices_promoted.date_pass) + "'"
                    sttrr2 = "'" + str(rec.invoices_promoted.date_join_school) + "'"

                    for e in employee_lst_bk:
                        rec.custom_id, rec.name, rec.gender, rec.date_of_birth_short, rec.province.name, rec.recruitment_employee.name, rec.room_recruitment.name, rec.enterprise.name_romaji_enterprise, rec.invoices_promoted.guild.name_acronym, rec.place_to_work.name, rec.invoices_promoted.job_predefine.name
                        print_list = [stt, rec.custom_id, rec.name, rec.gender, rec.date_of_birth_short,
                                      rec.province.name,
                                      rec.recruitment_employee.name, rec.room_recruitment.name,
                                      rec.enterprise.name_romaji_enterprise, rec.invoices_promoted.guild.name_acronym,
                                      rec.place_to_work.name, rec.invoices_promoted.job_predefine.name,
                                      rec.invoices_promoted.year_expire, sttr1, sttrr2, sttr,
                                      rec.invoices_promoted.dispatchcom1.name_short
                                      ]

            if reset_line1 == 0:
                reset_line1 = 1
                start_line1 = 4
            # print_list[0] = start_line1 - flag
            for x in range(len(print_list)):
                sheet1.write(start_line1, x, print_list[x], style_font)
            start_line1 += 1

        file_path = tempfile.gettempdir() + r"/OT_report_{id_invoice}.xls"
        wb.save(file_path)
        file = self.env['overtime.report.store'].create({'save_file': base64.b64encode(open(file_path, 'rb').read())})
        # print(file.id)
        # print(file.save_file)
        # print('/web/content/overtime.report.store/%s/save_file/bao_cao_lam_them.xls' % file.id)
        return file

    @api.multi
    def toggle_promoted(self):
        self.promoted = True
        print('tạo promoted')
        model_B_obj = self.env['intern.internclone'].create({'intern_id': self.intern_id.id})
        print(model_B_obj)
        return model_B_obj

    @api.multi
    def toggle_pass_exam(self):
        self.pass_exam = True
        self.cancel_pass = False
        self.preparatory_exam = False

    @api.multi
    def toggle_preparatory_exam(self):
        self.preparatory_exam = True
        self.pass_exam = False
        self.cancel_pass = False

    @api.multi
    def toggle_issues_raise(self):
        self.issues_raise = True
        view_id = self.env.ref('hh_intern.view_intern_form_issues_raise').id
        context = self._context.copy()
        return {
            'name': 'Có phát sinh',
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'intern.intern',
            'view_id': view_id,
            'type': 'ir.actions.act_window',
            'res_id': self.id,
            'context': context,
            'target': 'new'
        }

    @api.multi
    def toggle_cancel_pass(self):
        self.cancel_pass = True
        self.preparatory_exam = False
        self.pass_exam = False
        view_id = self.env.ref('hh_intern.view_intern_form_reason_cancel_pass').id
        context = self._context.copy()
        return {
            'name': 'Hủy sau trúng tuyển',
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'intern.intern',
            'view_id': view_id,
            'type': 'ir.actions.act_window',
            'res_id': self.id,
            'context': context,
            'target': 'new'
        }

    @api.multi
    def toggle_confirm_exam(self):
        self.confirm_exam = True

    # chot thi
    confirm_exam = fields.Boolean('Chốt thi tuyển')

    date_escape_exam = fields.Date('Ngày rút bỏ chốt thi')

    # trung tuyen/du bi

    pass_exam = fields.Boolean('Trúng tuyển')

    date_pass = fields.Datetime(string='Ngày trúng tuyển')

    def confirm_pass(self):
        self.write({
            'date_pass': fields.Datetime.now(),
        })

    preparatory_exam = fields.Boolean('Dự bị')

    cancel_pass = fields.Boolean('Huỷ trúng tuyển')

    reason_cancel_pass = fields.Char('Lý do huỷ TT')

    reason_cancel_bool = fields.Selection([('1', 'Do TTS'), ('2', 'Không phải do TTS')], string='Lý do huỷ TT')

    date_cancel_pass = fields.Date('Ngày huỷ trúng tuyển')

    # Phat sinh
    issues_raise = fields.Boolean('Phát sinh trước thi')
    issues_reason = fields.Text('Lý do phát sinh')
    issues_resolve = fields.Text('Hình thức xử lý')
    fine_employee = fields.Integer('Phạt CBTD')
    fine_intern = fields.Integer('Phạt TTS')

    # Phat sinh

    # xin nhap hoc muon
    admission_late = fields.Many2one('intern.admission', "Xin nhập học muộn")  # hh_202

    join_school = fields.Boolean('Đã nhập học')
    date_join_school = fields.Date("Ngày nhập học")

    # hong visa
    visa_failure = fields.Boolean('Hỏng VISA')

    tclt_failure = fields.Boolean('Hỏng TCLT')
    tclt_failure_reason = fields.Char('Lý do hỏng TCLT')

    check_heath_before_departure = fields.Boolean('Sức khoẻ xuất cảnh')
    check_before_fly = fields.Boolean('Kiểm tra trước bay')
    departure = fields.Boolean('Xuất cảnh')
    date_departure = fields.Date('Ngày xuất cảnh')

    comeback = fields.Boolean('Đã về nước')
    date_comeback = fields.Date('Ngày về nước')
    liquidated = fields.Boolean('Đã thanh lý HĐ')
    date_liquidated = fields.Date('Ngày thanh lý hợp đồng')
    reason_comeback = fields.Char('Lý do về nước')

    exam = fields.Boolean('Đã chốt thi')
    done_exam = fields.Boolean('Đã thi')
    cancel_exam = fields.Boolean('Đã huỷ')  # DON HANG BI HUY

    sequence_exam = fields.Integer('sequence', help="Sequence for the handle.", default=100)
    sequence_pass = fields.Integer('sequence', help="Sequence for the handle.", default=100)

    @api.model
    def create(self, vals):
        if 'issues_raise' in vals:
            if vals['issues_raise']:
                vals['date_escape_exam'] = fields.date.today()
            else:
                vals['date_escape_exam'] = False
        if 'cancel_pass' in vals:
            if vals['cancel_pass']:
                vals['date_cancel_pass'] = fields.date.today()
            else:
                vals['date_cancel_pass'] = False
        if 'comeback' in vals:
            if vals['comeback']:
                vals['date_comback'] = fields.date.today()
            else:
                vals['date_comback'] = False
        if 'liquidated' in vals:
            if vals['liquidated']:
                vals['date_liquidated'] = fields.date.today()
            else:
                vals['date_liquidated'] = False
        if 'promoted' in vals:
            if vals['promoted']:
                str_date = str(datetime.now() + relativedelta(hours=7))
                vals['datetime_promoted'] = str_date[0:16]
            else:
                vals['datetime_promoted'] = False

        record = super(InternInvoice, self).create(vals)
        return record

    @api.one
    def write(self, vals):
        if 'issues_raise' in vals:
            if vals['issues_raise']:
                vals['date_escape_exam'] = fields.date.today()
            else:
                vals['date_escape_exam'] = False
        if 'cancel_pass' in vals:
            if vals['cancel_pass']:
                vals['date_cancel_pass'] = fields.date.today()
            else:
                vals['date_cancel_pass'] = False
        if 'departure' in vals:
            if vals['departure']:
                vals['date_departure'] = fields.date.today()
            else:
                vals['date_departure'] = False
        if 'join_school' in vals:
            if vals['join_school']:
                vals['date_join_school'] = fields.date.today()
            else:
                vals['date_join_school'] = False
        if 'promoted' in vals:
            if vals['promoted']:
                str_date = str(datetime.now() + relativedelta(hours=7))
                vals['datetime_promoted'] = str_date[0:16]
            else:
                vals['datetime_promoted'] = False
        super(InternInvoice, self).write(vals)

    # danh sach xin tclt
    phieutraloi_id = fields.Many2one('intern.phieutraloi', string='Phiếu trả lời', index=True)

    date_duration_previous_in_jp = fields.Char(u'Ngày và thời gian ở Nhật lần trước', default='NO')

    time_at_pc_month = fields.Integer('Tổng thời gian làm việc tại công ty PC2 (tháng)', compute='compute_time_at_pc')
    time_at_pc_year = fields.Integer('Tổng thời gian làm việc tại công ty PC2 (năm)', compute='compute_time_at_pc')

    @api.multi
    @api.onchange('time_start_at_pc_from_month', 'time_start_at_pc_from_year')
    def compute_time_at_pc(self):
        for rec in self:
            if rec.invoice_id_hs:
                if rec.invoice_id_hs.month_create_letter_promotion and rec.invoice_id_hs.year_create_letter_promotion \
                        and rec.time_start_at_pc_from_month and rec.time_start_at_pc_from_year:
                    try:
                        total_month = (int(rec.invoice_id_hs.year_create_letter_promotion) - int(
                            rec.time_start_at_pc_from_year)) * 12 + int(
                            rec.invoice_id_hs.month_create_letter_promotion) - int(rec.time_start_at_pc_from_month)
                        rec.time_at_pc_month = '%d' % (total_month % 12)
                        rec.time_at_pc_year = '%d' % (total_month / 12)
                    except Exception:
                        rec.time_at_pc_month = False
                        rec.time_at_pc_year = False

                else:
                    rec.time_at_pc_month = False
                    rec.time_at_pc_year = False
            elif rec.invoices_promoted:
                if rec.invoices_promoted.month_create_letter_promotion and rec.invoices_promoted.year_create_letter_promotion \
                        and rec.time_start_at_pc_from_month and rec.time_start_at_pc_from_year:
                    try:
                        total_month = (int(rec.invoices_promoted.year_create_letter_promotion) - int(
                            rec.time_start_at_pc_from_year)) * 12 + int(
                            rec.invoices_promoted.month_create_letter_promotion) - int(rec.time_start_at_pc_from_month)
                        rec.time_at_pc_month = total_month % 12
                        rec.time_at_pc_year = total_month / 12
                    except Exception:
                        rec.time_at_pc_month = False
                        rec.time_at_pc_year = False

                else:
                    rec.time_at_pc_month = False
                    rec.time_at_pc_year = False

    current_status_2 = fields.Char("Trạng thái", store=False, compute='_compute_status_2')

    @api.multi
    def _compute_status_2(self):
        for obj in self:
            if 'id' in obj and type(obj['id']) is int:
                self._cr.execute(
                    "SELECT * FROM intern_internclone WHERE intern_internclone.id !=%d AND intern_internclone.intern_id = %d AND COALESCE(intern_internclone.promoted, FALSE) = TRUE AND intern_internclone.create_date > now()::date - interval '3 y'" %
                    (obj['id'], obj['intern_id']))
            else:
                self._cr.execute(
                    "SELECT * FROM intern_internclone WHERE intern_internclone.intern_id = %d AND COALESCE(intern_internclone.promoted, FALSE) = TRUE AND intern_internclone.create_date > now()::date - interval '3 y'" %
                    obj['intern_id'])
            tmpresult = self._cr.dictfetchall()
            count_exam = 0
            for record in tmpresult:
                if record['confirm_exam'] and not record['issues_raise']:
                    count_exam += 1
            obj.current_status_2 = u'Đã TC %d lần, TT %d lần' % (len(tmpresult), count_exam)

    enterprise = fields.Many2one('xinghiep.xinghiep', string='Xí nghiệp')
    dispatchcom2 = fields.Many2one('hoso.hoso', string=u'Công ty phái cử thứ 2')

    @api.model
    def search_read(self, domain=None, fields=None, offset=0, limit=None, order=None):
        if domain is not None:
            _logger.info("DOMAIN %s" % str(domain))
            ids = False
            for x in domain:
                if x[0] == 'name':
                    x[0] = 'name_without_signal'
                    x[2] = x[2]
                if x[0] == 'identity' and len(domain) == 1:
                    term = x[2]
                    domain = ['|', ['identity', 'ilike', term], ['identity_2', 'ilike', term]]
                    break
                if x[0] == 'id':
                    ids = True
        _logger.info("DOMAIN %s" % str(domain))

        clones = self.env['intern.internclone'].search([('id', 'in', domain[-1][2])])
        if ids and 0 < len(domain[-1][2]) == len(domain[0][2]):
            domain[0] = domain[-1]
        return super(InternInvoice, self).search_read(domain, fields, offset, limit, order)

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

    @api.onchange('name')  # if these fields are changed, call method
    def name_change(self):
        if self.name:
            self.name_without_signal = self.name
            tmp = self.convertToJP(intern_utils.fix_accent_2(self.name))
            if tmp is not None:
                self.name_in_japan = tmp

    def convertToJP(self, name):
        words = name.split()
        final = ""
        for i, word in enumerate(words):
            jps = self.env['intern.translator'].search([('vi_word', '=', word.upper())], limit=1)
            if jps:
                if i > 0:
                    final = final + u"・"
                final = final + jps[0].jp_word
            else:
                return ""
        return final

    @api.multi
    @api.depends('certification')
    @api.onchange('certification')
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

    # use for split invoice
    invoice_id_hs = fields.Many2one("intern.invoice", string='Đơn hàng', on_delete='restrict', index=True)

    place_to_work = fields.Many2one('japan.province', string='Địa điểm làm việc')

    datetime_promoted = fields.Datetime('Ngày tiến cử')
