from odoo import api, fields, models


class DownloadFile(models.TransientModel):
    _name = 'download.file'

    invoice = fields.Many2one('intern.invoice')

    link = fields.Char('Link Download')