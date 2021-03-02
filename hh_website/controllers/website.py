# -*- coding: utf-8 -*-
from odoo import http
from odoo.http import request
from datetime import datetime
import logging
from dateutil.relativedelta import relativedelta

_logger = logging.getLogger(__name__)


class Website(http.Controller):
    @http.route('/don_hang', type='http', auth='public', website=True)
    def render_invoices_page(self, **kwargs):
        invoices = request.env['intern.invoice'].sudo().search(
            [('status', '!=', 2), ('status', '!=', 3), ('status', '!=', 6), ('status', '!=', 7),
             ('hoso_created', '!=', True)])

        def tryconvert(date_str):
            try:
                return datetime.strptime(date_str, '%Y-%m-%d')
            except (ValueError, TypeError):
                return datetime(1, 1, 1)

        invoices = sorted(invoices, key=lambda r: (tryconvert(r.date_exam_short), r.id))
        form_tc = []
        form_ct = []
        for invoice in invoices:
            count_promoted = 0
            count_confirm_exam = 0
            for intern in invoice.interns_clone:
                if intern.promoted:
                    count_promoted += 1
                if intern.confirm_exam:
                    count_confirm_exam += 1

            form_tc.append(count_promoted)
            form_ct.append(count_confirm_exam)

        return http.request.render('hh_website.invoices_page',
                                   {'invoices': invoices, 'form_tc': form_tc, 'form_ct': form_ct})

    @http.route('/invoice/<invoice_id>', type='http', auth='public', website=True)
    def render_invoice_detail(self, invoice_id, **kwargs):
        invoice = request.env['intern.invoice'].sudo().browse(int(invoice_id))

        sort_by_room = request.httprequest.cookies.get('sort_by_room', 'false')
        sort_by_time_promotion = request.httprequest.cookies.get('sort_by_time_promotion', 'false')
        sort_by_room_bool = False
        sort_by_time_promotion_bool = False
        if sort_by_room == 'true':
            sort_by_room_bool = True
        if sort_by_time_promotion == 'true':
            sort_by_time_promotion_bool = True
        if not sort_by_room_bool:
            if sort_by_time_promotion_bool:
                interns = sorted(invoice.interns_clone, key=lambda x: x.datetime_promoted, reverse=True)
            else:
                interns = sorted(invoice.interns_clone, key=lambda x: x.condition_count2, reverse=True)
            interns_removed = []
            # if invoice.promotion_removed:
            # removed = [int(x) for x in invoice.promotion_removed.split(',')]
            #     removed = invoice.promotion_removed.split(',')
            #     interns_removed = request.env['intern.intern'].sudo().browse(removed)
            return http.request.render('hh_website.invoices_detail',
                                       {'invoice': invoice, 'interns': interns,
                                        'interns_removed': interns_removed,
                                        'sort_by_room': sort_by_room_bool,
                                        'sort_by_time_promotion': sort_by_time_promotion_bool})
        else:
            def tryconvert(room):
                if room:
                    return room.id
                return 0

            interns = sorted(invoice.interns_clone, key=lambda x: tryconvert(x.room_recruitment), reverse=True)
            room_tmp = None
            counter = 0
            list_interns = []
            while counter < len(interns):
                if interns[counter].promoted:
                    it = []
                    if interns[counter].room_recruitment:
                        room_tmp = interns[counter].room_recruitment.id
                    else:
                        room_tmp = None
                    for j in range(counter, len(interns)):
                        if room_tmp and interns[j].room_recruitment and interns[j].room_recruitment.id == room_tmp:
                            it.append(interns[j])
                            counter += 1
                        elif not room_tmp and not interns[j].room_recruitment:
                            it.append(interns[j])
                            counter += 1
                        else:
                            break
                    if sort_by_time_promotion_bool:
                        tmp = sorted(it, key=lambda x: x.datetime_promoted, reverse=True)
                    else:
                        tmp = sorted(it, key=lambda x: x.condition_count2, reverse=True)
                    list_interns.append(tmp)
                else:
                    counter += 1

            interns_removed = []
            # if invoice.promotion_removed:
            #     removed = [int(x) for x in invoice.promotion_removed.split(',')]
            #     interns_removed = request.env['intern.intern'].sudo().browse(removed)
            return http.request.render('hh_website.invoices_detail_2',
                                       {'invoice': invoice, 'list_interns': list_interns,
                                        'interns_removed': interns_removed,
                                        'sort_by_room': sort_by_room_bool,
                                        'sort_by_time_promotion': sort_by_time_promotion_bool})

    # @http.route('/don_da_thi_tuyen', type='http', auth='public', website=True)
    # def render_invoices_examinated(self, **kwargs):
    #     start_date = datetime.today().replace(day=1)
    #     invoices = request.env['intern.invoice'].sudo().search(
    #         ['|',('status', '=', 2), ('status', '=', 3),
    #          ('hoso_created', '!=', True),('date_exam_short','>=',start_date.strftime("%Y-%m-%d"))
    #             ,('date_exam_short','<',(start_date+relativedelta(months=1)).strftime("%Y-%m-%d"))])
    #     def tryconvert(date_str):
    #         try:
    #             return datetime.strptime(date_str, '%Y-%m-%d')
    #         except (ValueError, TypeError):
    #             return datetime(1, 1, 1)
    #
    #     invoices = sorted(invoices, key=lambda r: (tryconvert(r.date_exam_short), r.id))
    #     form_tc = []
    #     form_ct = []
    #     color_alert = []
    #     for invoice in invoices:
    #         count_promoted = 0
    #         count_confirm_exam = 0
    #         count_not_expire = 0
    #         for intern in invoice.interns_clone:
    #             if intern.promoted:
    #                 count_promoted += 1
    #                 if intern.datetime_promoted and invoice.date_confirm_form and datetime.strptime(intern.datetime_promoted, '%Y-%m-%d %H:%M:%S') + relativedelta(
    #                         hours=7) > datetime.strptime(invoice.date_confirm_form, '%Y-%m-%d'):
    #                     count_not_expire += 1
    #             if intern.confirm_exam:
    #                 count_confirm_exam += 1
    #
    #         if count_not_expire - invoice.source_total >0:
    #             color_alert.append('#91c468')
    #         else:
    #             color_alert.append('#e0596d')
    #
    #         form_tc.append(count_promoted)
    #         form_ct.append(count_confirm_exam)
    #
    #
    #     return http.request.render('hh_website.invoices_examinated',
    #                                {'invoices': invoices, 'form_tc': form_tc, 'form_ct': form_ct,'color_alert':color_alert})

    @http.route('/quay_ve_1tuan', type='http', auth='public', website=True)
    def render_invoices_comeback(self, **kwargs):
        week = (datetime.now() + relativedelta(days=7)).date()
        print(week)
        invoices = request.env['intern.invoice'].sudo().search(
            [('date_departure2', '>=', datetime.now().date()), ('date_departure2', '<', week),
             ('interns_departure.departure', '!=', False)])
        return http.request.render('hh_website.render_invoices_comeback',
                                   {'invoices': invoices, })

    # -------------------------------------------------------------------------
    @http.route('/quay_ve_1thang', type='http', auth='public', website=True)
    def render_invoices_comeback1(self, **kwargs):
        week = (datetime.now() + relativedelta(months=1)).date()
        print(week)
        invoices = request.env['intern.invoice'].sudo().search(
            [('date_departure2', '>=', datetime.now().date()), ('date_departure2', '<', week),
             ('interns_departure.departure', '!=', False)])
        return http.request.render('hh_website.render_invoices_comeback',
                                   {'invoices': invoices, })

    # #-------------------------------------------------------------------------
    @http.route('/quay_ve_3thang', type='http', auth='public', website=True)
    def render_invoices_comeback2(self, **kwargs):
        week = (datetime.now() + relativedelta(months=3)).date()
        print(week)
        invoices = request.env['intern.invoice'].sudo().search(
            [('date_departure2', '>=', datetime.now().date()), ('date_departure2', '<', week),
             ('interns_departure.departure', '!=', False)])
        return http.request.render('hh_website.render_invoices_comeback',
                                   {'invoices': invoices, })
