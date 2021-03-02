# -*- coding: utf-8 -*-
from odoo import api, fields, models
import logging

_logger = logging.getLogger(__name__)


class CancelInvoiceWizard(models.TransientModel):
    _name = "invoice.cancel.wizard"

    reason = fields.Char('Lý do')

    @api.multi
    def confirm_request(self):
        if 'action' in self._context and 'active_ids' in self._context:
            recs = self.env['intern.invoice'].browse(self._context['active_ids'])
            if self._context['action'] == 'pause':
                for rec in recs:
                    rec.pause_invoice(self.reason)
            elif self._context['action'] == 'cancel':
                for rec in recs:
                    rec.cancel_invoice(self.reason)
        return True


class PrintDocWizard(models.TransientModel):
    _name = "report.doccument"
    document = fields.Selection([('Doc1-3', '1-3'), ('Doc1-10', '1-10'), ('Doc1-13', '1-13'), ('Doc1-20', '1-20'),
                                 ('Doc1-21', '1-21'), ('Doc1-27', '1-27'), ('Doc1-28', '1-28'), ('Doc1-29', '1-29'),
                                 ('DocCCDT', 'Chứng chỉ kết thúc Đào tạo'), ('HDPC', 'Hợp đồng PC'),
                                 ('PROLETTER', 'Thư tiến cử'), ('DSLD', 'Danh sách lao động')
                                    , ('CheckList', 'Check List'), ('Doc4-8', '4-8'), ('Master', 'Master'),
                                 ('Doc-ALL', 'Tất cả')], string='Hồ sơ in')  # hh_298

    enterprise = fields.Many2one('xinghiep.xinghiep', string='Xí nghiệp', required=True)  # hh_299

    def _get_enterprise_domain(self):
        invoice_id = self._context['active_id']
        invoice = self.env['intern.invoice'].browse(invoice_id)
        return invoice.enterprise.id

    enterprise_ids = fields.Integer(default=_get_enterprise_domain)

    @api.multi
    def confirm_request(self):
        _logger.info("confirm")

        information_id = self.enterprise.id if self.enterprise.id else self.env.context.get('active_id')
        model_activate = self.env.context.get('active_model')
        infor = self.env[model_activate].browse(information_id)
        self.enterprise = infor.id

        return {
            'type': 'ir.actions.act_url',
            'url': '/download_extern_document/%s' % (self.id),
            'target': 'self', }
