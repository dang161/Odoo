# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.exceptions import UserError, ValidationError
from datetime import datetime, date
import logging
from dateutil.relativedelta import relativedelta

_logger = logging.getLogger(__name__)


class danhsachdonhang(models.Model):
    _inherit = 'intern.invoice'

    date_departure1 = fields.Char("Ngày xuất cảnh Dự kiến", store=True, compute='_date_departure1')  # hh_154

    @api.multi
    @api.depends('day_departure_doc', 'month_departure_doc', 'year_exam')
    def _date_departure1(self):
        strdate = ""
        for rec in self:
            if rec.day_departure_doc and rec.month_departure_doc and rec.year_departure_doc:
                strdate = datetime.strptime(
                    '%s-%s-%s' % (rec.year_departure_doc, rec.month_departure_doc, rec.day_departure_doc),
                    '%Y-%m-%d')
            else:
                strdate = None
        arr = str(strdate).split()
        self.date_departure1 = arr[0]
        print(self.date_departure1)

    @api.model
    def _get_current_year(self):
        return str(datetime.now().year)

    date_receive_hard_profile = fields.Date("Ngày nhận hồ sơ cứng")
    date_receive_contract = fields.Date("Ngày nhận HĐL")
    date_send_letter_pro = fields.Date("Ngày trình thư")
    date_expected_send_to_customer = fields.Date("Ngày dự kiến gửi hồ sơ cho KH")
    date_real_send_to_customer = fields.Date("Ngày thực tế gửi hồ sơ cho KH")
    note_hs = fields.Char("Ghi chú")
    enterprise = fields.Many2one(comodel_name="xinghiep.xinghiep", string="Tên xí nghiệp")
    # =============================================================================================
    day_start_training = fields.Char("Ngày")
    month_start_training = fields.Selection([('01', '01'), ('02', '02'), ('03', '03'), ('04', '04'),
                                             ('05', '05'), ('06', '06'), ('07', '07'), ('08', '08'),
                                             ('09', '09'), ('10', '10'), ('11', '11'), ('12', '12'), ], "Tháng")

    year_start_training = fields.Char("Năm")
    date_start_training = fields.Char("Ngày bắt đầu khóa học chú ý Chủ Nhật(Trước ngày bắt đầu 1 tháng)", store=False,
                                      compute='_date_start_training')

    @api.multi
    @api.depends('day_start_training', 'month_start_training', 'year_start_training')
    def _date_start_training(self):
        for rec in self:
            if rec.day_start_training and rec.month_start_training and rec.year_start_training:
                rec.date_start_training = u"Ngày %s tháng %s năm %s" % (
                    rec.day_start_training, rec.month_start_training, rec.year_start_training)
                tmp_date = datetime.strptime('%s/%s/%s' % (
                    rec.day_start_training, rec.month_start_training, rec.year_start_training),
                                             '%d/%m/%Y')
                tmp_date_create_plan = tmp_date - relativedelta(days=3)
                if not rec.day_create_plan_training or not rec.month_create_plan_training or not rec.year_create_plan_training:
                    rec.day_create_plan_training = '%02d' % tmp_date_create_plan.day
                    rec.month_create_plan_training = '%02d' % tmp_date_create_plan.month
                    rec.year_create_plan_training = '%d' % tmp_date_create_plan.year

                tmp_date_end_plan = tmp_date + relativedelta(months=1)
                if not rec.day_end_training or not rec.month_end_training or not rec.year_end_training:
                    rec.day_end_training = '%02d' % tmp_date_end_plan.day
                    rec.month_end_training = '%02d' % tmp_date_end_plan.month
                    rec.year_end_training = '%d' % tmp_date_end_plan.year
                tmp_date_report_customer = tmp_date_end_plan + relativedelta(days=1)

                if not rec.day_create_plan_training_report_customer or not rec.month_create_plan_training_report_customer or not rec.year_create_plan_training_report_customer:
                    rec.day_create_plan_training_report_customer = '%02d' % tmp_date_report_customer.day
                    rec.month_create_plan_training_report_customer = '%02d' % tmp_date_report_customer.month
                    rec.year_create_plan_training_report_customer = '%d' % tmp_date_report_customer.year

                if not rec.day_pay_finance1 or not rec.month_pay_finance1 or not rec.year_pay_finance1:
                    rec.day_pay_finance1 = rec.day_create_plan_training
                    rec.month_pay_finance1 = rec.month_create_plan_training
                    rec.year_pay_finance1 = rec.year_create_plan_training

            elif rec.month_start_training and rec.year_start_training:
                rec.date_start_training = u"Tháng %s năm %s" % (
                    rec.month_start_training, rec.year_start_training)
            elif rec.year_start_training:
                rec.date_start_training = u'Năm %s' % rec.year_start_training
            else:
                rec.date_start_training = ""

    # @api.one
    # @api.depends('day_start_training', 'month_start_training', 'year_start_training')
    # def _date_start_training(self):
    #     if self.day_start_training and self.month_start_training and self.year_start_training:
    #         self.date_start_training = u"Ngày %s tháng %s năm %s" % (
    #             self.day_start_training, self.month_start_training, self.year_start_training)
    #     elif self.month_start_training and self.year_start_training:
    #         self.date_start_training = u"Tháng %s năm %s" % (
    #             self.month_start_training, self.year_start_training)
    #     elif self.year_start_training:
    #         self.date_start_training = u'Năm %s' % self.year_start_training
    #     else:
    #         self.date_start_training = ""

    # -------------------------------------------------------------------------------------------
    day_end_training = fields.Char("Ngày")
    month_end_training = fields.Selection([('01', '01'), ('02', '02'), ('03', '03'), ('04', '04'),
                                           ('05', '05'), ('06', '06'), ('07', '07'), ('08', '08'),
                                           ('09', '09'), ('10', '10'), ('11', '11'), ('12', '12'), ], "Tháng")

    year_end_training = fields.Char("Năm")
    date_end_training = fields.Char(
        "Ngày kết thúc khóa học(chú ý Chủ Nhật) Tính từ thời điểm làm hồ sơ sau khoảng 10 ngày", store=False,
        compute='_date_end_training')

    @api.multi
    @api.depends('day_end_training', 'month_end_training', 'year_end_training')
    def _date_end_training(self):
        for rec in self:
            if rec.day_end_training and rec.month_end_training and rec.year_end_training:
                rec.date_end_training = u"Ngày %s tháng %s năm %s" % (
                    rec.day_end_training, rec.month_end_training, rec.year_end_training)
            elif rec.month_end_training and rec.year_end_training:
                rec.date_end_training = u"Tháng %s năm %s" % (
                    rec.month_end_training, rec.year_end_training)
            elif rec.year_end_training:
                rec.date_end_training = u'Năm %s' % rec.year_end_training
            else:
                rec.date_end_training = ""

    # ----------------------------------------------------------------------------------------
    day_create_plan_training = fields.Char("Ngày")
    month_create_plan_training = fields.Selection([('01', '01'), ('02', '02'), ('03', '03'), ('04', '04'),
                                                   ('05', '05'), ('06', '06'), ('07', '07'), ('08', '08'),
                                                   ('09', '09'), ('10', '10'), ('11', '11'), ('12', '12'), ], "Tháng")

    year_create_plan_training = fields.Char("Năm")
    date_create_plan_training = fields.Char(
        "Ngày lập kế hoạch đào tạo theo ủy thác(Trước ngày bắt đầu ít nhất 1 ngày, chú ý Chủ Nhật)", store=False,
        compute='_date_create_plan_training')

    @api.multi
    @api.depends('day_create_plan_training', 'month_create_plan_training', 'year_create_plan_training')
    def _date_create_plan_training(self):
        for rec in self:
            if rec.day_create_plan_training and rec.month_create_plan_training and rec.year_create_plan_training:
                rec.date_create_plan_training = u"Ngày %s tháng %s năm %s" % (
                    rec.day_create_plan_training, rec.month_create_plan_training, rec.year_create_plan_training)
            elif rec.month_create_plan_training and rec.year_create_plan_training:
                rec.date_create_plan_training = u"Tháng %s năm %s" % (
                    rec.month_create_plan_training, rec.year_create_plan_training)
            elif rec.year_create_plan_training:
                rec.date_create_plan_training = u'Năm %s' % rec.year_create_plan_training
            else:
                rec.date_create_plan_training = ""

    # --------------------------------------------------------------------------------------------
    day_create_plan_training_report_customer = fields.Char("Ngày")
    month_create_plan_training_report_customer = fields.Selection(
        [('01', '01'), ('02', '02'), ('03', '03'), ('04', '04'),
         ('05', '05'), ('06', '06'), ('07', '07'), ('08', '08'),
         ('09', '09'), ('10', '10'), ('11', '11'), ('12', '12'), ], "Tháng")

    year_create_plan_training_report_customer = fields.Char("Năm")
    date_create_plan_training_report_customer = fields.Char(
        "Ngày lập kế hoạch đào tạo BÁO CÁO KHÁCH HÀNG trước ngày bắt đầu ít nhất 1 ngày chú ý CHỦ NHẬT", store=False,
        compute='_date_create_plan_training_report_customer')

    @api.multi
    @api.depends('day_create_plan_training_report_customer', 'month_create_plan_training_report_customer',
                 'year_create_plan_training_report_customer')
    def _date_create_plan_training_report_customer(self):
        for rec in self:
            if rec.day_create_plan_training_report_customer and rec.month_create_plan_training_report_customer and rec.year_create_plan_training_report_customer:
                rec.date_create_plan_training_report_customer = u"Ngày %s tháng %s năm %s" % (
                    rec.day_create_plan_training_report_customer, rec.month_create_plan_training_report_customer,
                    rec.year_create_plan_training_report_customer)
            elif rec.month_create_plan_training_report_customer and rec.year_create_plan_training_report_customer:
                rec.date_create_plan_training_report_customer = u"Tháng %s năm %s" % (
                    rec.month_create_plan_training_report_customer, rec.year_create_plan_training_report_customer)
            elif rec.year_create_plan_training_report_customer:
                rec.date_create_plan_training_report_customer = u'Năm %s' % rec.year_create_plan_training_report_customer
            else:
                rec.date_create_plan_training_report_customer = ""

    # -------------------------------------------------------------------------------
    day_pay_finance1 = fields.Char("Ngày")
    month_pay_finance1 = fields.Selection([('01', '01'), ('02', '02'), ('03', '03'), ('04', '04'),
                                           ('05', '05'), ('06', '06'), ('07', '07'), ('08', '08'),
                                           ('09', '09'), ('10', '10'), ('11', '11'), ('12', '12'), ], "Tháng")

    year_pay_finance1 = fields.Char("Năm")
    date_pay_finance1 = fields.Char("Ngày nộp tài chính đợt 1 (Sau ngày trúng tuyển 7 ngày)", store=False,
                                    compute='_date_pay_finance1')

    @api.multi
    @api.depends('day_pay_finance1', 'month_pay_finance1', 'year_pay_finance1')
    def _date_pay_finance1(self):
        for rec in self:
            if rec.day_pay_finance1 and rec.month_pay_finance1 and rec.year_pay_finance1:
                rec.date_pay_finance1 = u"Ngày %s tháng %s năm %s" % (
                    rec.day_pay_finance1, rec.month_pay_finance1,
                    rec.year_pay_finance1)
            elif rec.month_pay_finance1 and rec.year_pay_finance1:
                rec.date_pay_finance1 = u"Tháng %s năm %s" % (
                    rec.month_pay_finance1, rec.year_pay_finance1)
            elif rec.year_pay_finance1:
                rec.date_pay_finance1 = u'Năm %s' % rec.year_pay_finance1
            else:
                rec.date_pay_finance1 = ""

    # -------------------------------------------------------------------------
    day_pay_finance2 = fields.Char("Ngày")
    month_pay_finance2 = fields.Selection([('01', '01'), ('02', '02'), ('03', '03'), ('04', '04'),
                                           ('05', '05'), ('06', '06'), ('07', '07'), ('08', '08'),
                                           ('09', '09'), ('10', '10'), ('11', '11'), ('12', '12'), ], "Tháng")

    year_pay_finance2 = fields.Char("Năm")
    date_pay_finance2 = fields.Char("Ngày nộp tài chính đợt 2 (Trước ngày dự kiến xuất cảnh 10 ngày)", store=False,
                                    compute='_date_pay_finance2')

    @api.multi
    @api.depends('day_pay_finance2', 'month_pay_finance2', 'year_pay_finance2')
    def _date_pay_finance2(self):
        for rec in self:
            if rec.day_pay_finance2 and rec.month_pay_finance2 and rec.year_pay_finance2:
                rec.date_pay_finance2 = u"Ngày %s tháng %s năm %s" % (
                    rec.day_pay_finance2, rec.month_pay_finance2,
                    rec.year_pay_finance2)
            elif rec.month_pay_finance2 and rec.year_pay_finance2:
                rec.date_pay_finance2 = u"Tháng %s năm %s" % (
                    rec.month_pay_finance2, rec.year_pay_finance2)
            elif rec.year_pay_finance2:
                rec.date_pay_finance2 = u'Năm %s' % rec.year_pay_finance2
            else:
                rec.date_pay_finance2 = ""

    # -------------------------------------------------------------------------
    day_sign_proletter = fields.Char("Ngày")
    month_sign_proletter = fields.Selection([('01', '01'), ('02', '02'), ('03', '03'), ('04', '04'),
                                             ('05', '05'), ('06', '06'), ('07', '07'), ('08', '08'),
                                             ('09', '09'), ('10', '10'), ('11', '11'), ('12', '12'), ], "Tháng")

    year_sign_proletter = fields.Char("Năm")
    date_sign_proletter = fields.Char("Ngày ký hợp đồng phái cử", store=False,
                                      compute='_date_sign_proletter')  # a122

    @api.multi
    @api.depends('day_sign_proletter', 'month_sign_proletter', 'year_sign_proletter')
    def _date_sign_proletter(self):
        for rec in self:
            if rec.day_sign_proletter and rec.month_sign_proletter and rec.year_sign_proletter:
                rec.date_sign_proletter = u"Ngày %s tháng %s năm %s" % (
                    rec.day_sign_proletter, rec.month_sign_proletter,
                    rec.year_sign_proletter)
            elif rec.month_sign_proletter and rec.year_sign_proletter:
                rec.date_sign_proletter = u"Tháng %s năm %s" % (
                    rec.month_sign_proletter, rec.year_sign_proletter)
            elif rec.year_pay_finance2:
                rec.date_sign_proletter = u'Năm %s' % rec.year_sign_proletter
            else:
                rec.date_sign_proletter = ""

    # ------------------------------------------------------------------------
    training_center = fields.Many2one("trainingcenter", string="Trung tâm đào tạo")
    length_training = fields.Char("Thời gian đào tạo khóa học (Chữ Hán)")
    hours_training = fields.Char("Tổng số thời gian đào tạo (số giờ học)")
    dispatchcom2 = fields.Many2one("hoso.hoso", string="Công Ty Phái Cử thứ 2")

    @api.multi
    @api.onchange('dispatchcom2')
    def _onchange_dispatchcom2(self):
        for rec in self:
            for intern in rec.interns_clone:
                if rec.dispatchcom2:
                    intern.dispatchcom2 = rec.dispatchcom2[0]
                else:
                    intern.dispatchcom2 = False
            for intern in rec.interns_pass_doc:
                if rec.dispatchcom2:
                    intern.dispatchcom2 = rec.dispatchcom2[0]
                else:
                    intern.dispatchcom2 = False
            for intern in rec.interns_pass_doc_hs:
                if rec.dispatchcom2:
                    intern.dispatchcom2 = rec.dispatchcom2[0]
                else:
                    intern.dispatchcom2 = False

    @api.multi
    @api.onchange('enterprise')
    def _onchange_enterprise(self):
        for rec in self:
            for intern in rec.interns_clone:
                if rec.enterprise:
                    intern.enterprise = rec.enterprise[0]
                else:
                    intern.enterprise = False
            for intern in rec.interns_pass_doc:
                if rec.enterprise:
                    intern.enterprise = rec.enterprise[0]
                else:
                    intern.enterprise = False
            for intern in rec.interns_pass_doc_hs:
                if rec.enterprise:
                    intern.enterprise = rec.enterprise[0]
                else:
                    intern.enterprise = False

    back_to_pc2 = fields.Boolean("Sau khi về nước sẽ quay lại Cty PC2")
    name_working_department = fields.Char(
        "Tên bộ phận TTS sẽ làm việc trong xí nghiệp (có trong hợp đồng lương) - Tiếng Nhật")
    # ----------------------------------------------------------------------------------------

    # Thong tin bo sung cho ho so noi

    day_create_letter_promotion = fields.Char("Ngày", size=2)
    month_create_letter_promotion = fields.Selection([('01', '01'), ('02', '02'), ('03', '03'), ('04', '04'),
                                                      ('05', '05'), ('06', '06'), ('07', '07'), ('08', '08'),
                                                      ('09', '09'), ('10', '10'), ('11', '11'), ('12', '12'), ],
                                                     "Tháng")

    year_create_letter_promotion = fields.Char("Năm", size=4, default=lambda self: self._get_current_year())
    date_create_letter_promotion_short = fields.Char('Ngày làm thư tiến cử', store=True,
                                                     compute='_date_create_letter_promotion_short')

    @api.multi
    @api.depends('day_create_letter_promotion', 'month_create_letter_promotion', 'year_create_letter_promotion')
    def _date_create_letter_promotion_short(self):
        for rec in self:
            if rec.day_create_letter_promotion and rec.month_create_letter_promotion and rec.year_create_letter_promotion:
                rec.date_create_letter_promotion_short = datetime.strptime('%s-%s-%s' %
                                                                           (rec.year_create_letter_promotion,
                                                                            rec.month_create_letter_promotion,
                                                                            rec.day_create_letter_promotion),
                                                                           '%Y-%m-%d')
            else:
                rec.date_create_letter_promotion_short = None

    date_create_letter_promotion = fields.Char("Ngày làm thư tiến cử", store=False,
                                               compute='_date_create_letter_pro')

    @api.multi
    @api.depends('day_create_letter_promotion', 'month_create_letter_promotion', 'year_create_letter_promotion')
    def _date_create_letter_pro(self):

        for rec in self:
            if rec.day_create_letter_promotion and rec.month_create_letter_promotion and rec.year_create_letter_promotion:
                rec.date_create_letter_promotion = u"Ngày %s tháng %s năm %s" % (
                    rec.day_create_letter_promotion, rec.month_create_letter_promotion,
                    rec.year_create_letter_promotion)
            elif rec.month_create_letter_promotion and rec.year_create_letter_promotion:
                rec.date_create_letter_promotion = u"Tháng %s năm %s" % (
                    rec.month_create_letter_promotion, rec.year_create_letter_promotion)
            elif rec.year_create_letter_promotion:
                rec.date_create_letter_promotion = u'Năm %s' % rec.year_create_letter_promotion
            else:
                rec.date_create_letter_promotion = ""

    person_sign_proletter = fields.Char("Tên người ký thư tiến cử (kiểm tra thường xuyên tránh sai)",
                                        default=u"Nguyễn Thị Ánh Hằng")
    position_person_sign = fields.Char("Chức danh người ký thư tiến cử - Tiếng Anh",
                                       default=u'Head of Division for Japan -  Southeast Asia')
    position_person_sign_jp = fields.Char("Chức danh người ký thư tiến cử - Tiếng Nhật", default=u'日本東南アジア部長')
    date_arrival_jp = fields.Date('Ngày tới Nhật')
    port_of_entry_jp = fields.Char('Cảng nhập cảnh')
    name_of_airline = fields.Char('Tên hãng hàng không')

    @api.one
    def pass_exam(self):
        if self.status < 2:
            self.status = 2

    @api.one
    def finish_invoice(self):
        if self.status < 3:
            self.status = 3

    @api.multi
    def create_extern_doc(self, enterprise_id, document):

        if document and document == 'PROLETTER':
            return self.create_proletter_doc(enterprise_id)

    def add_to_phieutraloi(self):
        phieutraloi = self.env['intern.phieutraloi'].search([('has_full', '=', False)])
        count_man = 0
        count_women = 0
        for rec in phieutraloi:
            count_man += rec.total_intern_men - rec.len_interns_man
            count_women += rec.total_intern_women - rec.len_interns_women
        count_current_invoice_man = 0
        count_current_invoice_women = 0

        list_interns = self.interns_pass_doc
        if self.hoso_created:
            list_interns = self.interns_pass_doc_hs

        for intern in list_interns:
            if not intern.phieutraloi_id:
                if intern.gender and intern.gender == 'nam':
                    count_current_invoice_man += 1
                else:
                    count_current_invoice_women += 1
        if count_current_invoice_man > count_man and count_current_invoice_women > count_women:
            raise ValidationError(u'Cần tạo phiếu trả lời mới, thiếu vị trí cho %d nam và %d nữ' % (
                (count_current_invoice_man - count_man), (count_current_invoice_women - count_women)))
        elif count_current_invoice_man > count_man:
            raise ValidationError(
                u'Cần tạo phiếu trả lời mới, thiếu vị trí cho %d nam' % (count_current_invoice_man - count_man))
        elif count_current_invoice_women > count_women:
            raise ValidationError(
                u'Cần tạo phiếu trả lời mới, thiếu vị trí cho %d nữ' % (count_current_invoice_women - count_women))
        else:
            for intern in list_interns:
                for rec in phieutraloi:
                    if intern.gender and intern.gender == 'nam' and rec.total_intern_men > rec.len_interns_man:
                        rec.interns = [(4, intern.id)]
                        rec.len_interns_man += 1
                    elif intern.gender and intern.gender == 'nu' and rec.total_intern_women > rec.len_interns_women:
                        rec.interns = [(4, intern.id)]
                        rec.len_interns_women += 1
