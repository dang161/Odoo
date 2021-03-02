# -*- coding: utf-8 -*-
from odoo import http
from odoo.http import request
from odoo.addons.web.controllers.main import serialize_exception, content_disposition
from io import BytesIO, StringIO
import os
import zipfile

import logging

_logger = logging.getLogger(__name__)


class CreateDocNew(http.Controller):
    @http.route('/web/binary/download_document_new', type='http', auth="public")
    def download_cv_new(self, model, id, filename=None, gender=None, **kwargs):
        invoice = request.env[model].browse(int(id))
        document = request.env['intern.document'].search([('name', '=', 'CV')], limit=1)
        finalDoc = invoice.createHeaderDocNew(gender)
        reponds = BytesIO()
        archive = zipfile.ZipFile(reponds, 'w', zipfile.ZIP_DEFLATED)
        if finalDoc is not None:
            archive.write(finalDoc.name, u"名簿リスト.docx")
            os.unlink(finalDoc.name)
        else:
            return
        listtmp = invoice.interns_exam_doc
        if gender == None:
            for i, intern in enumerate(sorted(listtmp, key=lambda x: x.sequence_exam)):
                childDoc = invoice.createCVDoc(document[0], intern, i)
                archive.write(childDoc.name,
                              'cv_%d_%s.docx' % ((i + 1), intern.name))
                os.unlink(childDoc.name)
        else:
            counter = 0
            for i, intern in enumerate(sorted(listtmp, key=lambda x: x.sequence_exam)):
                if intern.gender == gender:
                    childDoc = invoice.createCVDoc(document[0], intern, counter)
                    archive.write(childDoc.name,
                                  'cv_%d_%s.docx' % ((counter + 1), intern.name))

                    os.unlink(childDoc.name)
                    counter += 1

        archive.close()
        reponds.flush()
        ret_zip = reponds.getvalue()
        reponds.close()

        return request.make_response(ret_zip,
                                     [('Content-Type', 'application/zip'),
                                      ('Content-Disposition', content_disposition(filename))])
