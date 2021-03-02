# -*- coding: utf-8 -*-
from odoo import http
from odoo.http import request
from odoo.addons.web.controllers.main import serialize_exception, content_disposition
from io import BytesIO, StringIO
import os
import zipfile
import logging

_logger = logging.getLogger(__name__)


class createdoc(http.Controller):
    @http.route('/web/binary/download_document_hoso', type='http', auth="public")
    def download_document_hoso(self, model, id, filename=None, **kwargs):
        invoice = request.env[model].browse(int(id))
        docs = request.env['intern.document'].search([('name', '=', 'CV')], limit=1)
        reponds = BytesIO()
        archive = zipfile.ZipFile(reponds, 'w', zipfile.ZIP_DEFLATED)
        finalDoc = invoice.createHeaderDoc()

        if finalDoc is not None:
            archive.write(finalDoc.name, u"名簿リスト.docx")
            os.unlink(finalDoc.name)
        else:
            return
        listtmp = sorted(invoice.interns_exam_doc, key=lambda x: x.sequence_exam)
        for i, intern in enumerate(listtmp):
            if intern.pass_exam:
                childDoc = invoice.createCVDoc(docs[0], intern, i)
                archive.write(childDoc.name,
                              'cv_%d_%s.docx' % ((i + 1), intern.name))
                os.unlink(childDoc.name)

        archive.close()
        reponds.flush()
        ret_zip = reponds.getvalue()
        reponds.close()

        return request.make_response(ret_zip,
                                     [('Content-Type', 'application/zip'),
                                      ('Content-Disposition', content_disposition(filename))])

    @http.route('/download_extern_document/<string:id>', type='http', auth="public")
    def download_extern_document(self, id=False, **kwargs):
        reponds = BytesIO()
        archive = zipfile.ZipFile(reponds, 'w', zipfile.ZIP_DEFLATED)
        file_maps = {}
        document = request.env['report.doccument'].browse(int(id))
        invoice = request.env['intern.invoice']
        infor = document.enterprise
        list_interns = invoice.interns_pass_doc
        interns_pass = sorted(list_interns, key=lambda x: x.sequence_pass)

        doc_type = document.document
        data = document.enterprise.lienket.interns_pass_doc

        if doc_type == 'Doc1-3':
            for thuctapsinh in data:
                doc1_3 = invoice.create_Doc_1_3(infor, thuctapsinh.id)
                file_maps.update({u'1-3_%s.docx' % thuctapsinh.name: doc1_3.name})
        elif doc_type == 'Doc1-10':
            counter = 0
            for thuctapsinh in data:
                counter += 1
                doc1_10 = invoice.create_Doc_1_10(infor, thuctapsinh.id)
                file_maps.update({u'1-10_%s.docx' % thuctapsinh.name: doc1_10.name})
        elif doc_type == 'Doc1-13':
            doc1_13_1 = invoice.create_Doc_1_13_1(infor)
            file_maps.update({u'1-13-1号 HOANG HUNG JAPAN 訓連センター.docx': doc1_13_1.name})
            doc1_13_2 = invoice.create_Doc_1_13_2(infor)
            file_maps.update({u'1-13-2号HOANG HUNG 会社.docx': doc1_13_2.name})
        elif doc_type == 'Doc1-20':
            doc1_20 = invoice.create_Doc_1_20(infor)
            file_maps.update({u'1-20.docx': doc1_20.name})
        elif doc_type == 'Doc1-21':
            counter = 0
            for thuctapsinh in data:
                counter += 1
                doc1_21 = invoice.create_Doc_1_21(infor, thuctapsinh.id)
                file_maps.update({u'1-21_%s.docx' % thuctapsinh.name: doc1_21.name})
        elif doc_type == 'Doc1-27':
            doc1_27 = invoice.create_Doc_1_27(infor)
            file_maps.update({u'1-27.docx': doc1_27.name})
        elif doc_type == 'Doc1-28':
            for thuctapsinh in data:
                doc1_28 = invoice.create_Doc_1_28(infor, thuctapsinh.id)
                file_maps.update({u'1_28_%s.docx' % thuctapsinh.name: doc1_28.name})
        elif doc_type == 'Doc1-29':
            doc1_29 = invoice.create_Doc_1_29(infor)
            file_maps.update({u'1_29.docx': doc1_29.name})
        elif doc_type == 'DocCCDT':
            docCCDT = invoice.create_certification_end_train(infor)
            file_maps.update({u'DocCCDT.docx': docCCDT.name})
        elif doc_type == 'HDPC':
            counter = 0
            for thuctapsinh in data:
                counter += 1
                dochdtn = invoice.create_hdtn(infor, thuctapsinh.id)
                file_maps.update({u'HDPCTN_%s.docx' % thuctapsinh.name: dochdtn.name})
                dochdtv = invoice.create_hdtv(infor, thuctapsinh.id)
                file_maps.update({u'HDPCTV_%s.docx' % thuctapsinh.name: dochdtv.name})
        elif doc_type == 'PROLETTER':
            doc_list_send = invoice.create_list_of_sent_en(infor)
            file_maps.update({u'推薦書 - ENG.docx': doc_list_send.name})
            doc_list_send_jp = invoice.create_list_of_sent_jp(infor)
            file_maps.update({u'推薦書.docx': doc_list_send_jp.name})
        elif doc_type == 'DSLD':
            DSLD = invoice.create_danh_sach_lao_dong(infor)
            file_maps.update({u'DSLD.docx': DSLD.name})
        elif doc_type == 'CheckList':
            CheckList = invoice.create_check_list(infor)
            file_maps.update({u'CheckList.docx': CheckList.name})
        elif doc_type == 'Doc4-8':
            Doc4_8 = invoice.create_48(infor)
            file_maps.update({u'Doc48.docx': Doc4_8.name})
        elif doc_type == 'Master':
            Master = invoice.create_master(infor)
            file_maps.update({u'Master.docx': Master.name})
        elif doc_type == 'Doc-ALL':
            for thuctapsinh in data:
                doc1_3 = invoice.create_Doc_1_3(infor, thuctapsinh.id)
                file_maps.update({u'1-3_%s.docx' % thuctapsinh.name: doc1_3.name})

            for thuctapsinh in data:
                doc1_10 = invoice.create_Doc_1_10(infor, thuctapsinh.id)
                file_maps.update({u'1-10_%s.docx' % thuctapsinh.name: doc1_10.name})

            doc1_13_1 = invoice.create_Doc_1_13_1(infor)
            file_maps.update({u'1-13-1号 HOANG HUNG JAPAN 訓連センター.docx': doc1_13_1.name})
            doc1_13_2 = invoice.create_Doc_1_13_2(infor)
            file_maps.update({u'1-13-2号HOANG HUNG 会社.docx': doc1_13_2.name})

            doc1_20 = invoice.create_Doc_1_20(infor)
            file_maps.update({u'1-20.docx': doc1_20.name})

            for thuctapsinh in data:
                doc1_21 = invoice.create_Doc_1_21(infor, thuctapsinh.id)
                file_maps.update({u'1-21_%s.docx' % thuctapsinh.name: doc1_21.name})

            doc1_27 = invoice.create_Doc_1_27(infor)
            file_maps.update({u'1-27.docx': doc1_27.name})

            for thuctapsinh in data:
                doc1_28 = invoice.create_Doc_1_28(infor, thuctapsinh.id)
                file_maps.update({u'1_28_%s.docx' % thuctapsinh.name: doc1_28.name})
            doc1_29 = invoice.create_Doc_1_29(infor)
            file_maps.update({u'1_29.docx': doc1_29.name})

            docCCDT = invoice.create_certification_end_train(infor)
            file_maps.update({u'DocCCDT.docx': docCCDT.name})

            doc_list_send = invoice.create_list_of_sent_en(infor)
            file_maps.update({u'推薦書 - ENG.docx': doc_list_send.name})
            doc_list_send_jp = invoice.create_list_of_sent_jp(infor)
            file_maps.update({u'推薦書.docx': doc_list_send_jp.name})

            for thuctapsinh in data:
                dochdtn = invoice.create_hdtn(infor, thuctapsinh.id)
                file_maps.update({u'HDPCTN_%s.docx' % thuctapsinh.name: dochdtn.name})
                dochdtv = invoice.create_hdtv(infor, thuctapsinh.id)
                file_maps.update({u'HDPCTV_%s.docx' % thuctapsinh.name: dochdtv.name})

            DSLD = invoice.create_danh_sach_lao_dong(infor)
            file_maps.update({u'DSLD.docx': DSLD.name})

            CheckList = invoice.create_check_list(infor)
            file_maps.update({u'CheckList.docx': CheckList.name})

            Doc4_8 = invoice.create_48(infor)
            file_maps.update({u'Doc48.docx': Doc4_8.name})

            Master = invoice.create_master(infor)
            file_maps.update({u'Master.docx': Master.name})

        for key in file_maps:
            archive.write(file_maps[key], key)
            os.unlink(file_maps[key])

        archive.close()
        reponds.flush()
        ret_zip = reponds.getvalue()
        reponds.close()
        # ---------------------------------------------------------------------------------------------------
        if doc_type == 'Doc1-3':
            doc1_3 = 'Doc1_3.zip'
            return request.make_response(ret_zip,
                                         [('Content-Type', 'application/zip'),
                                          ('Content-Disposition', content_disposition(doc1_3))])
        if doc_type == 'Doc1-10':
            doc1_10 = 'Doc1_10.zip'
            return request.make_response(ret_zip,
                                         [('Content-Type', 'application/zip'),
                                          ('Content-Disposition', content_disposition(doc1_10))])
        if doc_type == 'Doc1-13':
            doc1_13_1 = 'Doc1_13_1.zip'
            return request.make_response(ret_zip,
                                         [('Content-Type', 'application/zip'),
                                          ('Content-Disposition', content_disposition(doc1_13_1))])
            doc1_13_2 = 'Doc1_13_2.zip'
            return request.make_response(ret_zip,
                                         [('Content-Type', 'application/zip'),
                                          ('Content-Disposition', content_disposition(doc1_13_2))])
        if doc_type == 'Doc1-20':
            doc1_20 = 'Doc1_20.zip'
            return request.make_response(ret_zip,
                                         [('Content-Type', 'application/zip'),
                                          ('Content-Disposition', content_disposition(doc1_20))])
        if doc_type == 'Doc1-21':
            doc1_21 = 'Doc1_21.zip'
            return request.make_response(ret_zip,
                                         [('Content-Type', 'application/zip'),
                                          ('Content-Disposition', content_disposition(doc1_21))])
        if doc_type == 'Doc1-27':
            doc1_27 = 'Doc1_27.zip'
            return request.make_response(ret_zip,
                                         [('Content-Type', 'application/zip'),
                                          ('Content-Disposition', content_disposition(doc1_27))])
        if doc_type == 'Doc1-28':
            doc1_28 = 'Doc1_28.zip'
            return request.make_response(ret_zip,
                                         [('Content-Type', 'application/zip'),
                                          ('Content-Disposition', content_disposition(doc1_28))])
        if doc_type == 'Doc1-29':
            doc1_29 = 'Doc1_29.zip'
            return request.make_response(ret_zip,
                                         [('Content-Type', 'application/zip'),
                                          ('Content-Disposition', content_disposition(doc1_29))])
        if doc_type == 'DocCCDT':
            docCCDT = 'DocCCDT.zip'
            return request.make_response(ret_zip,
                                         [('Content-Type', 'application/zip'),
                                          ('Content-Disposition', content_disposition(docCCDT))])
        if doc_type == 'HDPC':
            dochdtn = 'HDPC.zip'
            return request.make_response(ret_zip,
                                         [('Content-Type', 'application/zip'),
                                          ('Content-Disposition', content_disposition(dochdtn))])
        if doc_type == 'PROLETTER':
            doc_list_send = 'PROLETTER.zip'
            return request.make_response(ret_zip,
                                         [('Content-Type', 'application/zip'),
                                          ('Content-Disposition', content_disposition(doc_list_send))])
        if doc_type == 'DSLD':
            DSLD = 'DSLD.zip'
            return request.make_response(ret_zip,
                                         [('Content-Type', 'application/zip'),
                                          ('Content-Disposition', content_disposition(DSLD))])
        if doc_type == 'CheckList':
            CheckList = 'CheckList.zip'
            return request.make_response(ret_zip,
                                         [('Content-Type', 'application/zip'),
                                          ('Content-Disposition', content_disposition(CheckList))])
        if doc_type == 'Doc4-8':
            Doc4_8 = 'Doc4-8.zip'
            return request.make_response(ret_zip,
                                         [('Content-Type', 'application/zip'),
                                          ('Content-Disposition', content_disposition(Doc4_8))])
        if doc_type == 'Master':
            Master = 'Master.zip'
            return request.make_response(ret_zip,
                                         [('Content-Type', 'application/zip'),
                                          ('Content-Disposition', content_disposition(Master))])
        if doc_type == 'Doc-ALL':
            demo = 'Full.zip'
            return request.make_response(ret_zip,
                                         [('Content-Type', 'application/zip'),
                                          ('Content-Disposition', content_disposition(demo))])
