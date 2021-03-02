from odoo import models, fields, api


class TargetDeparment(models.Model):
    _name = 'intern.department'

    invoice_id = fields.Many2one("intern.invoice", string='Đơn hàng', ondelete='cascade')
    department_id = fields.Many2one(comodel_name="phongban.phongban", string="Phòng TD", required=False, )  # hh_218
    target_men = fields.Integer('Chỉ tiêu nam', default=0)  # hh_219
    target_women = fields.Integer('Chỉ tiêu nữ', default=0)  # hh_220


class kiemsoat(models.Model):
    _inherit = 'intern.invoice'

    name_of_guild = fields.Char("Tên nghiệp đoàn")
    targets = fields.One2many('intern.department', 'invoice_id', string=u'Khoán chỉ tiêu')
    enterprise_doc = fields.Many2one(comodel_name="xinghiep.xinghiep", string="Xí nghiệp")  # hh_213
    guild = fields.Many2one(comodel_name="nghiepdoan.nghiepdoan", string="Nghiệp đoàn")  # hh_214
    note_report = fields.Char("Note báo cáo")  # hh_215
    dispatchcom1 = fields.Many2one(comodel_name="dispatchcom1", string="Pháp nhân")  # hh_216
    color_notice = fields.Char('Cảnh báo màu')

    @api.multi
    @api.onchange('enterprise_doc')
    def _onchange_enterprise_doc(self):
        for rec in self:
            for intern in rec.interns_clone:
                intern.enterprise = rec.enterprise_doc

    @api.one
    def toggle_red(self):

        self.color_notice = '#F02121'
        self.note = True

    @api.one
    def toggle_yellow(self):

        self.color_notice = '#E9F021'
        self.note = True

    @api.one
    def toggle_green(self):

        self.color_notice = '#39F021'
        self.note = True

    @api.one
    def toggle_remove_notice(self):

        self.color_notice = False


@api.one
def revert_destroy(self):
    if self.status == 6 or self.status == 7:
        if self.previous_stt == 0:
            self.write({'status': 4})
        else:
            self.write({'status': self.previous_stt})
