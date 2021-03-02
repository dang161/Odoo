# -*- coding: utf-8 -*-
from odoo import models, fields, api
from datetime import datetime
from dateutil.relativedelta import relativedelta
from odoo.exceptions import ValidationError
from . import intern_utils
import xlwt, xlsxwriter, calendar, tempfile, base64
import logging

_logger = logging.getLogger(__name__)


def percentage(part, whole):
    return round(100.0 * float(part) / float(whole), 0)


class Intern(models.Model):
    _name = 'intern.intern'
    _rec_name = 'name'

    cmnd_or_tcc = fields.Char(string="CMND/Thẻ CC", compute="_compute_identity")  # hh_202

    @api.multi
    @api.depends('date_of_birth_short')
    def _compute_age(self):
        for emp in self:
            age = (datetime.now().date().year - int(emp.year))
            print(age)
            emp.age = str(age) + " Years"

    age = fields.Char(string="Age", compute='_compute_age')

    @api.multi
    def _compute_identity(self):
        for rec in self:
            if rec.identity:
                rec.cmnd_or_tcc = rec.identity
            else:
                rec.cmnd_or_tcc = rec.identity_2

    have_iq = fields.Boolean(string='IQ', compute='_compute_have_iq')  # hh_205

    @api.multi
    def _compute_have_iq(self):
        for rec in self:
            try:
                if rec.iq_percentage and int(rec.iq_percentage) > 0:
                    rec.have_iq = True
                else:
                    rec.have_iq = False
            except:
                rec.have_iq = False

    have_form = fields.Boolean(string="Có Form")  # hh_139
    have_health = fields.Boolean(string="Có giấy khám SK")  # hh_207
    have_deposit = fields.Boolean(string="Đặt cọc")  # hh_208
    room_recruitment = fields.Many2one('phongban.phongban', 'Phòng tuyển dụng')  # hh_209
    recruitment_employee = fields.Many2one('nhanvien.nhanvien', 'Cán bộ tuyển dụng')  # hh_210
    user_access = fields.Many2many("res.users", default=lambda self: self.env.user,
                                   string="User có quyền xem")  # hh_140
    recruitment_r_employee = fields.Many2one('nhanvien.nhanvien', string=u"Cán bộ phụ trách thực tế")  # hh_211
    deportation = fields.Boolean('Bị đuổi học')  # hh_206
    custom_id = fields.Char(string="Mã số")  # hh_01
    _sql_constraints = [('unique_id', 'UNIQUE(custom_id)', "Đã tồn tại TTS có mã số này"), ]
    # ---------------------------asdasdasdasd
    #     promoted = fields.Boolean('Tiến cử', default=False)  # hh_212
    #
    #     reason_cancel_pass = fields.Char('Lý do huỷ TT')  # hh_201
    #     join_school = fields.Boolean('Đã nhập học')  # hh_302
    #     date_join_school = fields.Date("Ngày nhập học")  # hh_303
    #     visa_failure = fields.Boolean('Hỏng VISA')  # hh_304
    #     tclt_failure = fields.Boolean('Hỏng TCLT')  # hh_305
    #     check_heath_before_departure = fields.Boolean('Sức khoẻ xuất cảnh')  # hh_306
    #     check_before_fly = fields.Boolean('Kiểm tra trước bay')  # hh_307
    #     departure = fields.Boolean('Xuất cảnh')  # hh_308
    #
    #     cancel_pass = fields.Boolean('Huỷ trúng tuyển', default=False)  # hh_310
    #     preparatory_exam = fields.Boolean('Dự bị')  # hh_311
    #     pass_exam = fields.Boolean('Trúng tuyển')  # hh_312
    #     reason_cancel_bool = fields.Selection([('1', 'Do TTS'), ('2', 'Không phải do TTS')],
    #                                           string='Lý do huỷ TT')  # hh_313
    #     date_cancel_pass = fields.Date('Ngày huỷ trúng tuyển')  # hh_314
    #     issues_raise = fields.Boolean('Phát sinh trước thi')  # hh_315
    #     issues_reason = fields.Text('Lý do phát sinh')  # hh_316
    #     issues_resolve = fields.Text('Hình thức xử lý')  # hh_317
    #     fine_employee = fields.Integer('Phạt CBTD')  # hh_318
    #     fine_intern = fields.Integer('Phạt TTS')  # hh_319
    #     comeback = fields.Boolean('Đã về nước')  # hh_320
    #     reason_comeback = fields.Char('Lý do về nước')  # hh_321
    #
    #     exam = fields.Boolean('Đã chốt thi')  # hh_322
    #     done_exam = fields.Boolean('Đã thi')  # hh_323
    #     cancel_exam = fields.Boolean('Đã huỷ')  # hh_324
    #
    #     sequence_exam = fields.Integer('sequence', help="Sequence for the handle.", default=100)  # hh_325
    #     sequence_pass = fields.Integer('sequence', help="Sequence for the handle.", default=100)  # hh_326
    #
    #     liquidated = fields.Boolean('Đã thanh lý HĐ')  # hh_327
    #     date_liquidated = fields.Date('Ngày thanh lý hợp đồng')
    #
    #     confirm_exam = fields.Boolean('Chốt thi tuyển')  # hh_221
    #     enterprise = fields.Many2one('xinghiep.xinghiep', string=u'Xí nghiệp')  # hh_222
    #     dispatchcom2 = fields.Many2one('hoso.hoso', string=u'Công ty phái cử thứ 2')  # hh_329
    #
    #
    #     date_pass = fields.Datetime(string='Ngày trúng tuyển')
    #
    #     def confirm_pass(self):
    #         print('thành công')
    #         self.write({
    #             'date_pass': fields.Datetime.now(),
    #         })
    #
    #     datetime_promoted = fields.Datetime('Ngày tiến cử')
    #     phieutraloi_id = fields.Many2one('intern.phieutraloi', string='Phiếu trả lời', index=True)  # hh_138
    # ---------------------------asdasdasdasd
    name = fields.Char(string="Họ tên", required=True)  # hh_02
    exp_sew = fields.Boolean(string="Tay nghề may")  # hh_70
    exp_mechanical = fields.Boolean(string='Tay nghề cơ khí,hàn')  # hh_71
    exp_building = fields.Boolean(string='KN xây dựng')  # hh_72
    exp_note = fields.Text(string='Ghi chú tay nghề')  # hh_73
    had_go_abroad = fields.Boolean(string='Đã từng đi nước ngoài')  # hh_74
    country_go_abroad = fields.Char(string='Nước nào')  # hh_75
    year_go_abroad = fields.Char(string='Năm nào')  # hh_76
    had_visa_jp = fields.Boolean(string='Đã từng xin VISA đi Nhật')  # hh_77

    # ngày tháng năm sinh-------------------------------------------------------------------------------
    day = fields.Char("Ngày", size=2)  # hh_14
    month = fields.Selection([('01', '01'), ('02', '02'), ('03', '03'), ('04', '04'),
                              ('05', '05'), ('06', '06'), ('07', '07'), ('08', '08'),
                              ('09', '09'), ('10', '10'), ('11', '11'), ('12', '12'), ], "Tháng")  # hh_15

    year = fields.Char("Năm", size=4)  # hh_16

    date_of_birth = fields.Char("Ngày sinh", store=True, compute='_date_of_birth')  # hh_03

    @api.one
    @api.depends('day', 'month', 'year')
    def _date_of_birth(self):
        strdate = ""
        for rec in self:
            if rec.day and rec.month and rec.year:
                strdate = datetime.strptime('%s-%s-%s' % (rec.year, rec.month, rec.day),
                                            '%Y-%m-%d')
            else:
                strdate = None
        arr = str(strdate).split()
        self.date_of_birth = arr[0]

    date_of_birth_short = fields.Char("Ngày sinh", store=True, compute='_date_of_birth_short')  # hh_203

    @api.multi
    @api.depends('day', 'month', 'year')
    def _date_of_birth_short(self):
        if self.day and self.month and self.year:
            self.date_of_birth_short = u"Ngày %s Tháng %s Năm %s" % (self.day, self.month, self.year)
        else:
            self.date_of_birth_short = ""

    current_status = fields.Char("Trạng thái", store=False, compute='_compute_status')

    issued = fields.Boolean('Có phát sinh', store=False, compute='_compute_status')

    @api.multi
    def _compute_status(self):
        for obj in self:
            self._cr.execute(
                "SELECT * FROM intern_internclone WHERE intern_internclone.intern_id = %d AND COALESCE(intern_internclone.cancel_exam, FALSE) = FALSE AND intern_internclone.create_date > now()::date - interval '3 y'" %
                obj['id'])
            tmpresult = self._cr.dictfetchall()
            promoteds = []
            exams = []
            obj.pass_issued_accounting = ''
            obj.issued = False
            for record in tmpresult:
                if record['issues_raise']:
                    obj.current_status = 'Phát sinh rút bỏ thi'
                    obj.pass_issued_accounting = 'Đã bỏ thi'
                    obj.issued = True
                    break
                if record['cancel_pass'] and record['reason_cancel_bool'] == '1':
                    obj.current_status = 'Phát sinh huỷ TT'
                    obj.pass_issued_accounting = 'Đã trúng tuyển'
                    obj.issued = True
                    break
                if record['departure'] and not record['comeback']:
                    obj.current_status = 'Đã xuất cảnh'
                    break
                if record['pass_exam'] and record['done_exam']:
                    obj.current_status = 'Đã trúng tuyển'
                    obj.pass_issued_accounting = 'Đã trúng tuyển'
                    break
                # if record['confirm_exam'] and not record['done_exam']:
                #     # obj.current_status = 'Đã chốt thi'
                #     # break
                #     invoice = self.env['intern.invoice'].browse(record['invoice_id'])
                #     if invoice:
                #         exams.append(invoice.name)
                # if record['promoted'] and not record['done_exam']:
                #     # obj.current_status = 'Đang tiến cử'
                #     invoice = self.env['intern.invoice'].browse(record['invoice_id'])
                #     if invoice:
                #         promoteds.append(invoice.name)
                #     # break
            if len(exams) > 0:
                obj.current_status = u'Đã chốt thi đơn %s' % (', '.join(exams))
            elif len(promoteds) > 0:
                obj.current_status = u'Đang tiến cử đơn %s' % (', '.join(promoteds))

    # Ngày cấp---------------------------------------------------------------------------------------------
    day_identity = fields.Char("Ngày", size=2)  # hh_27
    month_identity = fields.Selection([('01', '01'), ('02', '02'), ('03', '03'), ('04', '04'),
                                       ('05', '05'), ('06', '06'), ('07', '07'), ('08', '08'),
                                       ('09', '09'), ('10', '10'), ('11', '11'), ('12', '12'), ], "Tháng")  # hh_28
    year_identity = fields.Char("Năm", size=4)  # hh_29
    date_identity = fields.Char("Ngày cấp", store=False, compute='_date_of_identity')  # hh_07

    @api.one
    @api.depends('day_identity', 'month_identity', 'year_identity')
    def _date_of_identity(self):
        if self.day_identity and self.month_identity and self.year_identity:
            self.date_identity = u"Ngày %s Tháng %s Năm %s" % (
                self.day_identity, self.month_identity, self.year_identity)
        else:
            self.date_identity = ""

    # Ngày nộp hồ sơ--------------------------------------------------------------------------------------
    day_sent_doc = fields.Char("Ngày", size=2)  # hh_10
    month_sent_doc = fields.Selection([('01', '01'), ('02', '02'), ('03', '03'), ('04', '04'),
                                       ('05', '05'), ('06', '06'), ('07', '07'), ('08', '08'),
                                       ('09', '09'), ('10', '10'), ('11', '11'), ('12', '12'), ], "Tháng")  # hh_11

    year_sent_doc = fields.Char("Năm", size=4)  # hh_12
    date_sent_doc = fields.Char("Ngày gửi hồ sơ", store=False, compute='_date_send_doc')  # hh_13

    @api.one
    @api.depends('day_sent_doc', 'month_sent_doc', 'year_sent_doc')
    def _date_send_doc(self):
        if self.day_sent_doc and self.month_sent_doc and self.year_sent_doc:
            self.date_sent_doc = u"%s Tháng %s Năm %s" % (self.day_sent_doc, self.month_sent_doc, self.year_sent_doc)
        else:
            self.date_sent_doc = ""
        # -----------------------------------------------------------------------------------------------

    gender = fields.Selection([('nam', 'Nam'), ('nu', 'Nữ')], string='Giới tính')  # hh_04
    identity = fields.Char(string="CMND")  # hh_05
    identity_2 = fields.Char(string="Thẻ căn cước")  # hh_06
    place_cmnd = fields.Many2one("province", string="Nơi cấp")  # hh_08
    enter_source = fields.Selection([('1', 'Ngắn hạn'), ('2', 'Dài hạn'), ('3', 'Ban chỉ đạo'), ('4', 'Rút bỏ nguồn')],
                                    'Đăng ký nguồn')  # hh_09
    address = fields.Char('Địa chỉ liên hệ')  # hh_17
    province = fields.Many2one("province", string="Tỉnh/TP")  # hh_19
    avatar = fields.Binary("Ảnh")  # hh_18
    marital_status = fields.Many2one('marital', string="Tình trạng hôn nhân")  # hh_22
    height = fields.Integer("Chiều cao (cm)")  # hh_32
    weight = fields.Integer("Cân nặng (kg)")  # hh_33
    vision_left = fields.Integer("Mắt trái")  # hh_34
    vision_right = fields.Integer("Mắt phải")  # hh_35
    blood_group = fields.Selection([('A', 'A'), ('B', 'B'), ('AB', 'AB'), ('O', 'O')], 'Nhóm máu')  # hh_39
    note_health_vi = fields.Char('Ghi chú sức khỏe')  # hh_44
    phone_number = fields.Char("Số điện thoại")  # hh_20
    phone_number_relative = fields.Char("Số điện thoại người thân")  # hh_21
    relative_note = fields.Many2one('relation', string='Quan hệ với TTS')  # hh_24
    phone_number_relative_2 = fields.Char("Số điện thoại người thân")  # hh_25
    relative_note_2 = fields.Many2one('relation', string='Quan hệ với TTS')  # hh_26
    certification = fields.Many2one('intern.certification', "Bằng cấp")  # hh_23
    date_enter_source = fields.Date('Ngày vào nguồn')  # hh_30
    date_escape_source = fields.Date('Ngày rời nguồn')  # hh_31
    preferred_hand = fields.Selection((('0', 'Tay phải'), ('1', 'Tay trái'), ('2', 'Cả 2 tay')), string="Tay thuận",
                                      default='0')  # hh_36
    blindness = fields.Boolean("Bệnh mù màu")  # hh_37
    smoking = fields.Boolean("Có hút thuốc")  # hh_38
    diseases = fields.Boolean("Tiền sử bệnh lý")  # hh_40
    drink_alcohol = fields.Boolean("Uống rượu bia")  # hh_41
    surgery = fields.Boolean("Phẫu thuật hay xăm hình")  # hh_42
    surgery_content_vi = fields.Char("Nội dung Phẫu thuật hay xăm hình")  # hh_43
    check_kureperin = fields.Selection([('A+', 'A+'), ('A', 'A'), ('B', 'B'), ('C', 'C'), ('D', 'D')],
                                       "Điểm cộng dồn")  # hh_54
    # test----------------------------------------------------------------------------------

    logic_correct = fields.Integer()
    logic_done = fields.Integer()
    logic_percentage = fields.Char(string='Điểm logic', store=False, compute='_cal_logic_percentage')

    @api.one
    def _cal_logic_percentage(self):
        if self.logic_done is not 0:
            self.logic_percentage = "%d" % (percentage(self.logic_correct, self.logic_done))

    add_correct = fields.Integer()
    add_done = fields.Integer()
    add_percentage = fields.Char(string='Điểm cộng(IQ)', store=False, compute='_cal_add_percentage')

    @api.one
    def _cal_add_percentage(self):
        if self.add_done is not 0:
            self.add_percentage = "%d" % (percentage(self.add_correct, self.add_done))

    calculation_correct = fields.Integer()  # hh_45
    calculation_done = fields.Integer()  # hh_46
    calculation_percentage = fields.Char(string='Điểm cộng trừ nhân chia(IQ)', store=False,
                                         compute='_cal_calculation_percentage')  # hh_47

    @api.one
    def _cal_calculation_percentage(self):
        if self.calculation_done is not 0:
            self.calculation_percentage = "%d" % (percentage(self.calculation_correct, self.calculation_done))

    notice_correct = fields.Integer()  # hh_48
    notice_done = fields.Integer()  # hh_49
    notice_percentage = fields.Char(string='Điểm chú ý(IQ)', store=False, compute='_cal_notice_percentage')  # hh_50

    @api.one
    def _cal_notice_percentage(self):
        if self.notice_done is not 0:
            self.notice_percentage = "%d" % (percentage(self.notice_correct, self.notice_done))

    total_correct = fields.Integer(store=False, compute='_cal_total_corect')  # hh_51
    total_question = fields.Integer("Tổng số câu", default=48)  # hh_52
    iq_percentage = fields.Char("Trung bình cộng")  # hh_53

    @api.multi
    def _cal_total_corect(self):
        for rec in self:
            rec.total_correct = rec.logic_correct + rec.add_correct + rec.calculation_correct + rec.notice_correct
            if rec.total_question is not 0:
                rec.iq_percentage = "%d" % (percentage(rec.total_correct, rec.total_question))

    @api.multi
    @api.onchange('total_question', 'total_correct')
    def _cal_total_percentage(self):
        for rec in self:
            if rec.total_question is not 0:
                rec.iq_percentage = "%d" % (percentage(rec.total_correct, rec.total_question))

    @api.multi
    @api.onchange('logic_correct', 'logic_done')
    @api.depends('logic_correct', 'logic_done')
    def _cal_logic_percentage(self):
        for rec in self:
            if rec.logic_done is not 0:
                rec.logic_percentage = "%d" % (percentage(rec.logic_correct, rec.logic_done))

    @api.multi
    @api.onchange('add_correct', 'add_done')
    @api.depends('add_correct', 'add_done')
    def _cal_add_percentage(self):
        for rec in self:
            if rec.add_done is not 0:
                rec.add_percentage = "%d" % (percentage(rec.add_correct, rec.add_done))

    @api.multi
    @api.onchange('calculation_correct', 'calculation_done')
    @api.depends('calculation_correct', 'calculation_done')
    def _cal_calculation_percentage(self):
        for rec in self:
            if rec.calculation_done is not 0:
                rec.calculation_percentage = "%d" % (percentage(rec.calculation_correct, rec.calculation_done))

    @api.multi
    @api.onchange('notice_correct', 'notice_done')
    @api.depends('notice_correct', 'notice_done')
    def _cal_notice_percentage(self):
        for rec in self:
            if rec.notice_done is not 0:
                rec.notice_percentage = "%d" % (percentage(rec.notice_correct, rec.notice_done))

    @api.multi
    @api.onchange('logic_correct', 'add_correct', 'calculation_correct', 'notice_correct', 'total_question')
    @api.depends('logic_correct', 'add_correct', 'calculation_correct', 'notice_correct', 'total_question')
    def _cal_total_percentage(self):
        for rec in self:
            rec.total_correct = rec.logic_correct + rec.add_correct + rec.calculation_correct + rec.notice_correct
            if rec.total_question is not 0:
                rec.iq_percentage = "%d" % (percentage(rec.total_correct, rec.total_question))

    # --------------------------------------------------------------------------------------
    family_accept = fields.Boolean("Gia đình có đồng ý cho đi Nhật không?", default=True)
    strong_vi = fields.Char(string="Điểm mạnh")  # hh_55
    weak_vi = fields.Char(string="Điểm yếu")  # hh_56
    favourite_vi = fields.Char("Sở thích")  # hh_57
    family_income_vi = fields.Float("Tổng thu nhập gia đình(VNĐ)")  # hh_58
    teammate = fields.Boolean("Có kinh nghiệm sống tập thể")  # hh_59
    cooking = fields.Boolean("Biết nấu ăn")  # hh_60
    motivation_vi = fields.Char("Lý do đi Nhật")  # hh_61
    income_after_three_year_vi = fields.Float("Sau 3 năm bạn muốn kiếm được bao nhiêu ?")  # hh_62
    job_after_return_vi = fields.Char("Sau khi về nước bạn muốn làm công việc gì ?")  # hh_63
    prefer_object_vi = fields.Char("Nếu nhận mức lương gấp 3 hiện tại bạn muốn mua gì ?")  # hh_64
    memory_vi = fields.Char("Kỷ niệm đáng nhớ nhất của bạn:")  # hh_65
    valuable_vi = fields.Char("Điều quý giá nhất đối với bạn trong cuộc sống:")  # hh_66
    family_member_in_jp_vi = fields.Char("Người thân ở Nhật")  # hh_67
    education_status = fields.Selection([('1', 'Nhập học sớm'), ('2', 'Nhập học muộn'), ('3', 'Lưu ban')],
                                        string="Tình trạng học tập")  # hh_68
    education_content_vi = fields.Char("Nội dung Tình trạng học tập")  # hh_69
    educations = fields.One2many(comodel_name="intern.education", inverse_name="lienket",
                                 string="Lý lịch học tập")  # hh_78
    employments = fields.One2many(comodel_name="intern.employment", inverse_name="lienket",
                                  string="Lý lịch làm việc")  # hh_79
    familys = fields.One2many(comodel_name="intern.family", inverse_name="lienket", string="Gia đình")  # hh_80

    @api.multi
    def _count_condition(self):
        for rec in self:
            rec.condition_count = 0
            if rec.have_iq:
                rec.condition_count = rec.condition_count + 5
            if rec.have_health:
                rec.condition_count = rec.condition_count + 5
            if rec.have_deposit:
                rec.condition_count = rec.condition_count + 5
            if rec.avatar:
                rec.condition_count = rec.condition_count + 5
            rec.condition_count2 = 5
            if rec.have_health and rec.have_deposit and rec.avatar and rec.have_iq:
                rec.condition_count2 = 10
            elif not rec.have_health or not rec.have_deposit:
                rec.condition_count2 = 0

    condition_count = fields.Integer("", store=False, compute=_count_condition)
    condition_count2 = fields.Integer("", store=False, compute=_count_condition)

    name_without_signal = fields.Char("Tên tiếng Việt ko dấu")

    invoices_promoted = fields.Many2many('intern.invoice', compute="_compute_invoice_promoted",
                                         string='Đơn hàng tiến cử')

    @api.one
    def _compute_invoice_promoted(self):
        related_ids = []
        internsclone = self.env['intern.internclone'].search([('intern_id', '=', self.id), ('promoted', '=', True)])
        for intern in internsclone:
            for iv in intern.invoice_id:
                related_ids.append(iv.id)
        self.invoices_promoted = self.env['intern.invoice'].search([('id', 'in', related_ids)])

    # ------Thực tập sinh của hồ sơ-----------------------------------------------------------
    name_in_japan = fields.Char("Họ tên tiếng Nhật")  # hh_331
    hktt = fields.Char("Địa chỉ hộ khẩu thường trú của TTS (Tiếng Việt có dấu)")  # hh_332
    contact_person = fields.Char("Khi cần liên lạc với ai ")  # hh_333
    contact_relative = fields.Many2one('relation', "Quan hệ với TTS")  # hh_334
    contact_phone = fields.Char("Số điện thoại của người quan hệ với TTS")  # hh_335
    contact_address = fields.Char("Địa chỉ của người liên lạc (Tiếng Việt có dấu)")  # hh_336
    last_education_from_month = fields.Selection([('01', '01'), ('02', '02'), ('03', '03'), ('04', '04'),
                                                  ('05', '05'), ('06', '06'), ('07', '07'), ('08', '08'),
                                                  ('09', '09'), ('10', '10'), ('11', '11'), ('12', '12'), ], "Tháng",
                                                 default='09')  # hh_337

    last_education_from_year = fields.Char("Năm", size=4)  # hh_338

    last_education_to_month = fields.Selection([('01', '01'), ('02', '02'), ('03', '03'), ('04', '04'),
                                                ('05', '05'), ('06', '06'), ('07', '07'), ('08', '08'),
                                                ('09', '09'), ('10', '10'), ('11', '11'), ('12', '12'), ], "Tháng",
                                               default='06')  # hh_339
    last_education_to_year = fields.Char("Năm", size=4)  # hh_340
    last_time_education = fields.Char(
        "Thời gian học từ năm nào tới năm nào (Trường học mới nhất ghi trong hồ sơ TTS) - Chữ Hán", store=False,
        compute='_last_time_education')  # hh_341

    @api.multi
    @api.depends('last_education_from_month', 'last_education_from_year', 'last_education_to_month',
                 'last_education_to_year')
    def _last_time_education(self):
        for rec in self:
            if rec.last_education_from_month and rec.last_education_from_year:
                rec.last_time_education = intern_utils.date_time_in_jp(None, rec.last_education_from_month,
                                                                       rec.last_education_from_year)
            else:
                rec.last_time_education = ""
            if rec.last_education_from_year and rec.last_education_to_year:
                rec.last_time_education = rec.last_time_education + u'～ '

            if rec.last_education_to_month and rec.last_education_to_year:
                rec.last_time_education = rec.last_time_education + \
                                          intern_utils.date_time_in_jp(None, rec.last_education_to_month,
                                                                       rec.last_education_to_year)

    last_education_from_month2 = fields.Selection([('01', '01'), ('02', '02'), ('03', '03'), ('04', '04'),
                                                   ('05', '05'), ('06', '06'), ('07', '07'), ('08', '08'),
                                                   ('09', '09'), ('10', '10'), ('11', '11'), ('12', '12'), ],
                                                  "Tháng")  # hh_342

    last_education_from_year2 = fields.Char("Năm", size=4)  # hh_343

    last_education_to_month2 = fields.Selection([('01', '01'), ('02', '02'), ('03', '03'), ('04', '04'),
                                                 ('05', '05'), ('06', '06'), ('07', '07'), ('08', '08'),
                                                 ('09', '09'), ('10', '10'), ('11', '11'), ('12', '12'), ],
                                                "Tháng")  # hh_344
    last_education_to_year2 = fields.Char("Năm", size=4)  # hh_345
    last_time_education2 = fields.Char(
        "Thời gian học từ năm nào tới năm nào - Chữ Hán", store=False,
        compute='_last_time_education2')  # hh_346

    @api.multi
    @api.depends('last_education_from_month2', 'last_education_from_year2', 'last_education_to_month2',
                 'last_education_to_year2')
    def _last_time_education2(self):
        for rec in self:
            if rec.last_education_from_month2 and rec.last_education_from_year2:
                rec.last_time_education2 = intern_utils.date_time_in_jp(None, rec.last_education_from_month2,
                                                                        rec.last_education_from_year2)
            else:
                rec.last_time_education2 = ""
            if rec.last_education_from_year2 and rec.last_education_to_year2:
                rec.last_time_education2 = rec.last_time_education2 + u'～ '

            if rec.last_education_to_month2 and rec.last_education_to_year2:
                rec.last_time_education2 = rec.last_time_education2 + \
                                           intern_utils.date_time_in_jp(None, rec.last_education_to_month2,
                                                                        rec.last_education_to_year2)

    last_school_education = fields.Char("TÊN TRƯỜNG gần nhất của TTS - tiếng Việt")  # hh_347
    last_school_education_jp = fields.Char("TÊN TRƯỜNG gần nhất của TTS - chữ Hán")  # hh_348

    last_school_education2 = fields.Char("TÊN TRƯỜNG gần nhất của TTS - tiếng Việt")  # hh_349
    last_school_education_jp2 = fields.Char("TÊN TRƯỜNG gần nhất của TTS - chữ Hán")  # hh_350

    time_employee = fields.Char(
        "THỜI GIAN làm việc tại CÔNG TY HOẶC NƠI LÀM VIỆC THỨ NHẤT tiếng Nhật(trước khi vào công ty PC thứ 2 nếu có",
        store=False, compute='_time_employee')  # hh_351

    time_employee_from_month = fields.Selection([('01', '01'), ('02', '02'), ('03', '03'), ('04', '04'),
                                                 ('05', '05'), ('06', '06'), ('07', '07'), ('08', '08'),
                                                 ('09', '09'), ('10', '10'), ('11', '11'), ('12', '12'), ],
                                                "Tháng")  # hh_352

    time_employee_from_year = fields.Char("Năm", size=4)  # hh_353

    time_employee_to_month = fields.Selection([('01', '01'), ('02', '02'), ('03', '03'), ('04', '04'),
                                               ('05', '05'), ('06', '06'), ('07', '07'), ('08', '08'),
                                               ('09', '09'), ('10', '10'), ('11', '11'), ('12', '12'), ],
                                              "Tháng")  # hh_354
    time_employee_to_year = fields.Char("Năm", size=4)  # hh_355

    @api.depends('time_employee_from_month', 'time_employee_from_year', 'time_employee_to_month',
                 'time_employee_to_year')
    def _time_employee(self):
        for rec in self:
            if rec.time_employee_from_year:
                rec.time_employee = intern_utils.date_time_in_jp(None, rec.time_employee_from_month,
                                                                 rec.time_employee_from_year)
            else:
                rec.time_employee = ""

            if rec.time_employee_from_year and rec.time_employee_to_year:
                rec.time_employee = rec.time_employee + u'～ '

            if rec.time_employee_to_year:
                rec.time_employee = rec.time_employee + \
                                    intern_utils.date_time_in_jp(None, rec.time_employee_to_month,
                                                                 rec.time_employee_to_year)

    job_employee_jp = fields.Char("Ngành nghề - TIẾNG NHẬT")  # hh_356
    job_employee_vi = fields.Char("Ngành nghề - TIẾNG VIỆT")  # hh_357

    time_employee2 = fields.Char(
        "THỜI GIAN làm việc tại CÔNG TY HOẶC NƠI LÀM VIỆC THỨ HAI tiếng Nhật(trước khi vào công ty PC thứ 2 nếu có",
        store=False, compute='_time_employee2')  # hh_358

    time_employee2_from_month = fields.Selection([('01', '01'), ('02', '02'), ('03', '03'), ('04', '04'),
                                                  ('05', '05'), ('06', '06'), ('07', '07'), ('08', '08'),
                                                  ('09', '09'), ('10', '10'), ('11', '11'), ('12', '12'), ],
                                                 "Tháng")  # hh_359

    time_employee2_from_year = fields.Char("Năm", size=4)  # hh_360

    time_employee2_to_month = fields.Selection([('01', '01'), ('02', '02'), ('03', '03'), ('04', '04'),
                                                ('05', '05'), ('06', '06'), ('07', '07'), ('08', '08'),
                                                ('09', '09'), ('10', '10'), ('11', '11'), ('12', '12'), ],
                                               "Tháng")  # hh_361
    time_employee2_to_year = fields.Char("Năm", size=4)  # hh_362

    @api.depends('time_employee2_from_month', 'time_employee2_from_year', 'time_employee2_to_month',
                 'time_employee2_to_year')
    def _time_employee2(self):
        for rec in self:
            if rec.time_employee2_from_year:
                rec.time_employee2 = intern_utils.date_time_in_jp(None, rec.time_employee2_from_month,
                                                                  rec.time_employee2_from_year)
            else:
                rec.time_employee2 = ""

            if rec.time_employee2_from_year and rec.time_employee2_to_year:
                rec.time_employee2 = rec.time_employee2 + u'～ '

            if rec.time_employee2_to_year:
                rec.time_employee2 = rec.time_employee2 + \
                                     intern_utils.date_time_in_jp(None, rec.time_employee2_to_month,
                                                                  rec.time_employee2_to_year)

    job_employee2_jp = fields.Char(
        "Ngành nghề - TIẾNG NHẬT")  # hh_363
    job_employee2_vi = fields.Char(
        "Ngành nghề - TIẾNG VIỆT")  # hh_364

    time_employee3 = fields.Char(
        "THỜI GIAN làm việc tại CÔNG TY HOẶC NƠI LÀM VIỆC THỨ BA tiếng Nhật(trước khi vào công ty PC thứ 2 nếu có",
        store=False, compute='_time_employee3')  # hh_365
    job_employee3_jp = fields.Char(
        "Ngành nghề - TIẾNG NHẬT")  # hh_366
    job_employee3_vi = fields.Char(
        "Ngành nghề - TIẾNG VIỆT")  # hh_367

    time_employee3_from_month = fields.Selection([('01', '01'), ('02', '02'), ('03', '03'), ('04', '04'),
                                                  ('05', '05'), ('06', '06'), ('07', '07'), ('08', '08'),
                                                  ('09', '09'), ('10', '10'), ('11', '11'), ('12', '12'), ],
                                                 "Tháng")  # hh_368

    time_employee3_from_year = fields.Char("Năm", size=4)  # hh_369

    time_employee3_to_month = fields.Selection([('01', '01'), ('02', '02'), ('03', '03'), ('04', '04'),
                                                ('05', '05'), ('06', '06'), ('07', '07'), ('08', '08'),
                                                ('09', '09'), ('10', '10'), ('11', '11'), ('12', '12'), ],
                                               "Tháng")  # hh_370
    time_employee3_to_year = fields.Char("Năm", size=4)  # hh_371

    @api.depends('time_employee3_from_month', 'time_employee3_from_year', 'time_employee3_to_month',
                 'time_employee3_to_year')
    def _time_employee3(self):
        for rec in self:
            if rec.time_employee3_from_year:
                rec.time_employee3 = intern_utils.date_time_in_jp(None, rec.time_employee3_from_month,
                                                                  rec.time_employee3_from_year)
            else:
                rec.time_employee3 = ""

            if rec.time_employee3_from_year and rec.time_employee3_to_year:
                rec.time_employee3 = rec.time_employee3 + u'～ '

            if rec.time_employee3_to_year:
                rec.time_employee3 = rec.time_employee3 + \
                                     intern_utils.date_time_in_jp(None, rec.time_employee3_to_month,
                                                                  rec.time_employee3_to_year)

    #
    time_employee4 = fields.Char(
        "THỜI GIAN làm việc tại CÔNG TY HOẶC NƠI LÀM VIỆC THỨ TƯ tiếng Nhật(trước khi vào công ty PC thứ 2 nếu có",
        store=False, compute='_time_employee4')  # hh_372
    job_employee4_jp = fields.Char(
        "Ngành nghề - TIẾNG NHẬT")  # hh_373
    job_employee4_vi = fields.Char(
        "Ngành nghề - TIẾNG VIỆT")  # hh_374

    time_employee4_from_month = fields.Selection([('01', '01'), ('02', '02'), ('03', '03'), ('04', '04'),
                                                  ('05', '05'), ('06', '06'), ('07', '07'), ('08', '08'),
                                                  ('09', '09'), ('10', '10'), ('11', '11'), ('12', '12'), ],
                                                 "Tháng")  # hh_375

    time_employee4_from_year = fields.Char("Năm", size=4)  # hh_376

    time_employee4_to_month = fields.Selection([('01', '01'), ('02', '02'), ('03', '03'), ('04', '04'),
                                                ('05', '05'), ('06', '06'), ('07', '07'), ('08', '08'),
                                                ('09', '09'), ('10', '10'), ('11', '11'), ('12', '12'), ],
                                               "Tháng")  # hh_377
    time_employee4_to_year = fields.Char("Năm", size=4)  # hh_378

    @api.depends('time_employee4_from_month', 'time_employee4_from_year', 'time_employee4_to_month',
                 'time_employee4_to_year')
    def _time_employee4(self):
        for rec in self:
            if rec.time_employee4_from_year:
                rec.time_employee4 = intern_utils.date_time_in_jp(None, rec.time_employee4_from_month,
                                                                  rec.time_employee4_from_year)
            else:
                rec.time_employee4 = ""

            if rec.time_employee4_from_year and rec.time_employee4_to_year:
                rec.time_employee4 = rec.time_employee4 + u'～ '

            if rec.time_employee4_to_year:
                rec.time_employee4 = rec.time_employee4 + \
                                     intern_utils.date_time_in_jp(None, rec.time_employee4_to_month,
                                                                  rec.time_employee4_to_year)

    #
    time_employee5 = fields.Char(
        "THỜI GIAN làm việc tại CÔNG TY HOẶC NƠI LÀM VIỆC THỨ NĂM tiếng Nhật(trước khi vào công ty PC thứ 2 nếu có",
        store=False, compute='_time_employee5')  # hh_379
    job_employee5_jp = fields.Char(
        "Ngành nghề - TIẾNG NHẬT")  # hh_380
    job_employee5_vi = fields.Char(
        "Ngành nghề - TIẾNG VIỆT")  # hh_381

    time_employee5_from_month = fields.Selection([('01', '01'), ('02', '02'), ('03', '03'), ('04', '04'),
                                                  ('05', '05'), ('06', '06'), ('07', '07'), ('08', '08'),
                                                  ('09', '09'), ('10', '10'), ('11', '11'), ('12', '12'), ],
                                                 "Tháng")  # hh_382

    time_employee5_from_year = fields.Char("Năm", size=4)  # hh_383

    time_employee5_to_month = fields.Selection([('01', '01'), ('02', '02'), ('03', '03'), ('04', '04'),
                                                ('05', '05'), ('06', '06'), ('07', '07'), ('08', '08'),
                                                ('09', '09'), ('10', '10'), ('11', '11'), ('12', '12'), ],
                                               "Tháng")  # hh_384
    time_employee5_to_year = fields.Char("Năm", size=4)  # hh_385

    @api.depends('time_employee5_from_month', 'time_employee5_from_year', 'time_employee5_to_month',
                 'time_employee5_to_year')
    def _time_employee5(self):
        for rec in self:
            if rec.time_employee5_from_year:
                rec.time_employee5 = intern_utils.date_time_in_jp(None, rec.time_employee5_from_month,
                                                                  rec.time_employee5_from_year)
            else:
                rec.time_employee5 = ""

            if rec.time_employee5_from_year and rec.time_employee5_to_year:
                rec.time_employee5 = rec.time_employee5 + u'～ '

            if rec.time_employee5_to_year:
                rec.time_employee5 = rec.time_employee5 + \
                                     intern_utils.date_time_in_jp(None, rec.time_employee5_to_month,
                                                                  rec.time_employee5_to_year)

    time_start_at_pc = fields.Char("Thời gian bắt đầu làm công ty PC thứ 2(từ tháng, năm, đến nay) TIẾNG NHẬT",
                                   store=False, compute='_time_start_at_pc')  # hh_386

    time_start_at_pc_from_month = fields.Selection([('01', '01'), ('02', '02'), ('03', '03'), ('04', '04'),
                                                    ('05', '05'), ('06', '06'), ('07', '07'), ('08', '08'),
                                                    ('09', '09'), ('10', '10'), ('11', '11'), ('12', '12'), ],
                                                   "Tháng")  # hh_387

    time_start_at_pc_from_year = fields.Char("Năm", size=4)  # hh_388

    @api.multi
    @api.depends('time_start_at_pc_from_month', 'time_start_at_pc_from_year')
    def _time_start_at_pc(self):
        for rec in self:
            if rec.time_start_at_pc_from_year:
                rec.time_start_at_pc = intern_utils.date_time_in_jp(None, rec.time_start_at_pc_from_month,
                                                                    rec.time_start_at_pc_from_year)
            else:
                rec.time_start_at_pc = ""

            if rec.time_start_at_pc_from_year:
                rec.time_start_at_pc = rec.time_start_at_pc + u'～ 現在'

    # ---------------------------asdasdasdasd
    # time_at_pc_month = fields.Integer('Tổng thời gian làm việc tại công ty PC2 (tháng)')  # hh_389
    # time_at_pc_year = fields.Integer('Tổng thời gian làm việc tại công ty PC2 (năm)')  # hh_390
    # date_duration_previous_in_jp = fields.Char(u'Ngày và thời gian ở Nhật lần trước', default='NO')  # hh_397
    # ---------------------------asdasdasdasd
    passport_no = fields.Char('Passport No.')  # hh_391
    passport_type = fields.Selection([('0', 'Ngoại giao'), ('1', 'Công vụ'), ('2', 'Phổ thông'), ('3', 'Khác')],
                                     string='Loại passport')  # hh_392
    passport_place = fields.Many2one('province', string="Nơi cấp")  # hh_393
    passport_date_issue = fields.Date(string='Ngày cấp')  # hh_394
    passport_issuing_authority = fields.Char('Cơ quan cấp')  # hh_395
    passport_date_expire = fields.Date('Ngày hết hạn')  # hh_396

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

    @api.model
    def create(self, vals):
        if 'identity' not in vals and 'identity_2' not in vals:
            raise ValidationError('Bạn chưa nhập CMND hoặc thẻ căn cước')
        if 'identity' in vals and vals['identity']:
            vals['identity'] = vals['identity'].strip()
            tmp = self.env['intern.intern'].search([('identity', '=', vals['identity'])], limit=1)
            if tmp and len(tmp) == 1:
                raise ValidationError('Đã tồn tại TTS có số CMND này')
        if 'identity_2' in vals and vals['identity_2']:
            vals['identity_2'] = vals['identity_2'].strip()
            tmp = self.env['intern.intern'].search([('identity_2', '=', vals['identity_2'])], limit=1)
            if tmp and len(tmp) == 1:
                raise ValidationError('Đã tồn tại TTS có số thẻ căn cước này')
        if 'certification' in vals and 'educations' in vals:
            contain_check = False
            specilization_check = False
            if not vals['certification'] or not vals['educations']:
                contain_check = True
                specilization_check = True
            if vals['certification'] == 1:  # THCS
                specilization_check = True
                for education in vals['educations']:
                    if 'certificate' in education[2] and education[2]['certificate'] == 2:
                        contain_check = True
                        break
            if vals['certification'] == 2:  # THPT
                specilization_check = True
                for education in vals['educations']:
                    if 'certificate' in education[2] and education[2]['certificate'] == 3:
                        contain_check = True
                        break
            if vals['certification'] == 3:  # Trung cap
                for education in vals['educations']:
                    if 'certificate' in education[2] and education[2]['certificate'] == 6:
                        contain_check = True
                        if 'specialized' in vals and 'specialization' in education[2]:
                            if education[2]['specialization'] and vals['specialized'] and vals['specialized'].upper() == \
                                    education[2]['specialization'].upper():
                                specilization_check = True
                        else:
                            specilization_check = True
                        break
            if vals['certification'] == 4:  # Cao dang
                for education in vals['educations']:
                    if 'certificate' in education[2] and education[2]['certificate'] == 4:
                        contain_check = True
                        if 'specialized' in vals and 'specialization' in education[2]:
                            if education[2]['specialization'] and vals['specialized'] and vals['specialized'].upper() == \
                                    education[2]['specialization'].upper():
                                specilization_check = True
                        else:
                            specilization_check = True
                        break
            if vals['certification'] == 5:  # Dai hoc
                for education in vals['educations']:
                    if 'certificate' in education[2] and education[2]['certificate'] == 5:
                        contain_check = True
                        if 'specialized' in vals and 'specialization' in education[2]:
                            if education[2]['specialization'] and vals['specialized'] and vals['specialized'].upper() == \
                                    education[2]['specialization'].upper():
                                specilization_check = True
                        else:
                            specilization_check = True
                        break
            if not contain_check:
                raise ValidationError('Lý lịch học tập chưa tương ứng với trình độ học vấn')
            elif not specilization_check:
                raise ValidationError('Lý lịch học tập chưa tương ứng với chuyên ngành')
        if 'enter_source' in vals:
            if vals['enter_source'] is not False:
                if vals['enter_source'] != '4' and ('date_enter_source' not in vals or not vals['date_enter_source']):
                    raise ValidationError('TTS đã nhập nguồn nhưng chưa có ngày vào nguồn')
                elif vals['enter_source'] == '4' and (
                        'date_escape_source' not in vals or not vals['date_escape_source']):
                    raise ValidationError('TTS đã rút nguồn nhưng chưa có ngày rút nguồn')
            if vals['enter_source'] != False and vals['enter_source'] != '4':
                vals['enter_source_tmp'] = vals['enter_source']
        if 'enter_source' in vals:
            history = {}
            history['enter_source'] = vals['enter_source']
            if vals['enter_source']:
                if vals['enter_source'] == '4':
                    history['date_enter_source'] = vals['date_escape_source']
                else:
                    history['date_enter_source'] = vals['date_enter_source']
            vals['entersource_history'] = [(0, 0, history)]
        record = super(Intern, self).create(vals)
        self.env['intern.internclone'].create({'intern_id': record.id})
        try:
            splitName = vals['name'].split()
            tempSplitName = intern_utils.fix_accent_2(intern_utils.no_accent_vietnamese2(vals['name'])).split()
            if u'・' in vals['name_in_japan']:
                tempSplitJp = vals['name_in_japan'].split(u'・')
            elif u' ' in vals['name_in_japan']:
                tempSplitJp = vals['name_in_japan'].split(u' ')
            else:
                tempSplitJp = []
            if len(tempSplitName) == len(tempSplitJp):
                for i, s in enumerate(tempSplitName):
                    s = s.strip()
                    jps = self.env['intern.translator'].search([('vi_word', '=', s.upper())], limit=1)
                    if not jps:
                        self.env['intern.translator'].create({
                            'vi_word': s.upper(), 'jp_word': tempSplitJp[i]
                        })
        except:
            print('Loi roi')
        return record

    @api.onchange('identity', 'identity_2')
    @api.multi
    def check_identity(self):
        for rec in self:
            if rec.identity:
                if type(rec.id) == int:
                    tmp = self.env['intern.intern'].search([('identity', '=', rec.identity), ('id', '!=', rec.id)],
                                                           limit=1)
                    if tmp and len(tmp) == 1:
                        raise ValidationError('Đã tồn tại TTS có số CMND này')
                else:
                    tmp = self.env['intern.intern'].search([('identity', '=', rec.identity)],
                                                           limit=1)
                    if tmp and len(tmp) == 1:
                        raise ValidationError('Đã tồn tại TTS có số CMND này')

            elif rec.identity_2:
                if type(rec.id) == int:
                    tmp = self.env['intern.intern'].search([('identity_2', '=', rec.identity_2), ('id', '!=', rec.id)],
                                                           limit=1)
                    if tmp and len(tmp) == 1:
                        raise ValidationError('Đã tồn tại TTS có số thẻ cc này')
                else:
                    tmp = self.env['intern.intern'].search([('identity_2', '=', rec.identity_2)],
                                                           limit=1)
                    if tmp and len(tmp) == 1:
                        raise ValidationError('Đã tồn tại TTS có số thẻ cc này')

    @api.one
    def write(self, vals):
        _logger.info("WRITE")
        if 'identity' in vals and vals['identity']:
            vals['identity'] = vals['identity'].strip()
            tmp = self.env['intern.intern'].search([('identity', '=', vals['identity']), ('id', '!=', self.id)],
                                                   limit=1)
            if tmp and len(tmp) == 1:
                raise ValidationError('Đã tồn tại TTS có số CMND này')
        if 'identity_2' in vals and vals['identity_2']:
            vals['identity_2'] = vals['identity_2'].strip()
            tmp = self.env['intern.intern'].search([('identity_2', '=', vals['identity_2']), ('id', '!=', self.id)],
                                                   limit=1)
            if tmp and len(tmp) == 1:
                raise ValidationError('Đã tồn tại TTS có số thẻ căn cước này')
        if 'certification' in vals and 'educations' in vals:
            contain_check = False
            specilization_check = False
            if not vals['certification'] or not vals['educations']:
                contain_check = True
                specilization_check = True

            if vals['certification'] == 1:  # THCS
                specilization_check = True
                for education in vals['educations']:
                    if education[2] and 'certificate' in education[2] and education[2]['certificate'] == 2:
                        contain_check = True
                        break
            if vals['certification'] == 2:  # THPT
                specilization_check = True
                for education in vals['educations']:
                    if education[2] and 'certificate' in education[2] and education[2]['certificate'] == 3:
                        contain_check = True
                        break
            if vals['certification'] == 3:  # Trung cap
                for education in vals['educations']:
                    if education[2] and 'certificate' in education[2] and education[2]['certificate'] == 6:
                        contain_check = True
                        if 'specialized' in vals and 'specialization' in education[2]:
                            if education[2]['specialization'] and vals['specialized'] and vals['specialized'] and vals[
                                'specialized'].upper() == education[2]['specialization'].upper():
                                specilization_check = True
                        else:
                            specilization_check = True
                        break
            if vals['certification'] == 4:  # Cao dang
                for education in vals['educations']:
                    if education[2] and 'certificate' in education[2] and education[2]['certificate'] == 4:
                        contain_check = True
                        if 'specialized' in vals and 'specialization' in education[2]:
                            if education[2]['specialization'] and vals['specialized'] and vals['specialized'] and vals[
                                'specialized'].upper() == education[2]['specialization'].upper():
                                specilization_check = True
                        else:
                            specilization_check = True
                        break
            if vals['certification'] == 5:  # Dai hoc
                for education in vals['educations']:
                    if education[2] and 'certificate' in education[2] and education[2]['certificate'] == 5:
                        contain_check = True
                        if 'specialized' in vals and 'specialization' in education[2]:
                            if education[2]['specialization'] and vals['specialized'] and vals['specialized'] and vals[
                                'specialized'].upper() == education[2]['specialization'].upper():
                                specilization_check = True
                        else:
                            specilization_check = True
                        break
            if not contain_check:
                raise ValidationError('Lý lịch học tập chưa tương ứng với trình độ học vấn')
            elif not specilization_check:
                raise ValidationError('Lý lịch học tập chưa tương ứng với chuyên ngành')
        if 'enter_source' in vals:
            if vals['enter_source'] is not False:
                if vals['enter_source'] != '4' and ('date_enter_source' not in vals or not vals['date_enter_source']):
                    raise ValidationError('TTS đã nhập nguồn nhưng chưa có ngày vào nguồn')
                elif vals['enter_source'] == '4' and (
                        'date_escape_source' not in vals or not vals['date_escape_source']):
                    raise ValidationError('TTS đã rút nguồn nhưng chưa có ngày rút nguồn')
            if vals['enter_source'] != False and vals['enter_source'] != '4':
                vals['enter_source_tmp'] = vals['enter_source']
        if vals.get('name_in_japan'):
            tempSplitName = intern_utils.fix_accent_2(self.name).split()
            if u'・' in vals['name_in_japan']:
                tempSplitJp = vals['name_in_japan'].split(u'・')
            elif u' ' in vals['name_in_japan']:
                tempSplitJp = vals['name_in_japan'].split(u' ')
            else:
                tempSplitJp = []
            if len(tempSplitName) == len(tempSplitJp):
                for i, s in enumerate(tempSplitName):
                    s = s.strip()
                    jps = self.env['intern.translator'].search([('vi_word', '=', s.upper())], limit=1)
                    if not jps:
                        self.env['intern.translator'].create({
                            'vi_word': s.upper(), 'jp_word': tempSplitJp[i]
                        })
        if 'enter_source' in vals:
            history = {}
            history['enter_source'] = vals['enter_source']

            if vals['enter_source']:
                if vals['enter_source'] == '4':
                    history['date_enter_source'] = vals['date_escape_source']
                else:
                    history['date_enter_source'] = vals['date_enter_source']
            vals['entersource_history'] = [(0, 0, history)]
        record = super(Intern, self).write(vals)

    admission_late = fields.Many2one('intern.admission', "Xin nhập học muộn")  # hh_202
    discipline = fields.Many2one(comodel_name="intern.discipline", string="Bị kỷ luật")


class Discipline(models.Model):
    _name = 'intern.discipline'
    _rec_name = 'discipline'

    discipline = fields.Integer('id', default="0")
    name = fields.Char('Nội dung')  # hh_398


class admission_late(models.Model):
    _name = 'intern.admission'
    _rec_name = 'admission_late'

    admission_late = fields.Integer("Xin nhập học muộn")  # hh_202
    admission_late_des = fields.Text('Nội dung muộn')  # hh_301


class InternEducation(models.Model):
    _name = 'intern.education'
    _rec_name = 'school'

    lienket = fields.Many2one(comodel_name="intern.intern")  # hh_135
    month_start = fields.Selection([('01', '01'), ('02', '02'), ('03', '03'), ('04', '04'),
                                    ('05', '05'), ('06', '06'), ('07', '07'), ('08', '08'),
                                    ('09', '09'), ('10', '10'), ('11', '11'), ('12', '12'), ], "Tháng",
                                   default='09')  # hh_81

    year_start = fields.Char("Năm bắt đầu", size=4, required=True)  # hh_82

    month_end = fields.Selection([('01', '01'), ('02', '02'), ('03', '03'), ('04', '04'),
                                  ('05', '05'), ('06', '06'), ('07', '07'), ('08', '08'),
                                  ('09', '09'), ('10', '10'), ('11', '11'), ('12', '12'), ], "Tháng",
                                 default='06')  # hh_83
    year_end = fields.Char("Năm kết thúc", size=4, required=True)  # hh_84
    school = fields.Char("Tên trường", required=True)  # hh_85
    school_type = fields.Many2one(comodel_name="school", required=True)  # hh_86
    specialization = fields.Char("Chuyên ngành", required=True)  # hh_87
    certificate = fields.Many2one(comodel_name="intern.certification",
                                  string="Bằng cấp")  # hh_88
    graduated = fields.Boolean("Đã tốt nghiệp", default=True)  # hh_89
    show_specialization = fields.Boolean(store=False)
    sequence = fields.Integer('sequence', help="Sequence for the handle.", default=10)

    @api.onchange('school_type')
    def school_type_change(self):
        if self.school_type:
            if self.school_type.name_in_vn == u'Tiểu học':
                self.specialization = self.school_type.name_in_jp
                self.show_specialization = False
            elif self.school_type.name_in_vn == u'Trung học cơ sở':
                self.specialization = self.school_type.name_in_jp
                self.show_specialization = False
            elif self.school_type.name_in_vn == u'Trung học phổ thông':
                self.specialization = self.school_type.name_in_jp
                self.show_specialization = False
            else:
                self.specialization = ""
                self.show_specialization = True
            self.certificate = self.school_type
        else:
            self.show_specialization = False


class InternEmployment(models.Model):
    _name = 'intern.employment'
    _rec_name = 'company'

    lienket = fields.Many2one(comodel_name="intern.intern")  # hh_136
    month_start = fields.Selection([('01', '01'), ('02', '02'), ('03', '03'), ('04', '04'),
                                    ('05', '05'), ('06', '06'), ('07', '07'), ('08', '08'),
                                    ('09', '09'), ('10', '10'), ('11', '11'), ('12', '12'), ], "Tháng")  # hh_90

    year_start = fields.Char("Năm bắt đầu", size=4, required=True)  # hh_91

    month_end = fields.Selection([('01', '01'), ('02', '02'), ('03', '03'), ('04', '04'),
                                  ('05', '05'), ('06', '06'), ('07', '07'), ('08', '08'),
                                  ('09', '09'), ('10', '10'), ('11', '11'), ('12', '12'), ], "Tháng")  # hh_92
    year_end = fields.Char("Năm kết thúc", size=4, required=True)  # hh_93

    company = fields.Char("Tên công ty", required=True)  # hh_94
    description = fields.Char("Lý lịch làm việc")  # hh_95
    sequence = fields.Integer('sequence', help="Sequence for the handle.", default=10)


class InternFamily(models.Model):
    _name = 'intern.family'
    _rec_name = 'relationship'

    lienket = fields.Many2one(comodel_name="intern.intern")  # hh_137
    name = fields.Char("Tên", required=True)  # hh_96
    relationship = fields.Char("Quan hệ", required=True)  # hh_97
    ages = fields.Integer("Tuổi")  # hh_98
    birth_year = fields.Integer("Năm sinh")  # hh_99
    job = fields.Char("Nghề nghiệp")  # hh_101
    live_together = fields.Boolean("Sống chung", default=10)  # hh_100

    @api.onchange('ages')
    def age_change(self):
        if self.ages:
            self.birth_year = (datetime.now().year) - self.ages
        else:
            self.birth_year = 0

    @api.multi
    def read(self, fields=None, load='_classic_read'):
        result = super(InternFamily, self).read(fields, load)
        for record in result:
            if 'birth_year' in record and 'ages' in record:
                record['ages'] = datetime.now().year - record['birth_year']
        return result

    sequence = fields.Integer('sequence', help="Sequence for the handle.")
