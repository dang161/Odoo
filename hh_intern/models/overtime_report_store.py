from odoo import api, fields, models


class OvertimeReportStore(models.TransientModel):
    _name = "overtime.report.store"

    save_file = fields.Binary('file lưu', store=True)
