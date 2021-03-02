# -*- coding: utf-8 -*-
from odoo import http
from odoo.http import request
import json
from odoo.addons.web.controllers.main import serialize_exception, content_disposition
import logging
from io import BytesIO

_logger = logging.getLogger(__name__)


class WebFormController(http.Controller):

    @http.route('/odoo/maps', type='http',
                auth='public', methods=['GET'])
    def index(self, **args):
        _logger.info('CONNECTION SUCCESSFUL')
        _logger.info(args)

        invoice_id = args.get('invoice', False)
        _logger.info("INVOICE  %s" % str(invoice_id))
        invoice = request.env['intern.invoice'].sudo().browse(int(invoice_id))
        maps = {}

        _logger.info("avatar %s " % request.httprequest.host_url)

        if invoice:
            i = 0
            data_map = []
            listPro = []
            tts = ""
            list_intern = sorted(invoice.interns_exam_doc, key=lambda x: x.sequence_exam)
            for i, intern in enumerate(list_intern):
                mapschild = {}
                avatars = {}

                mapschild['tieng_viet'] = intern.province.name
                mapschild['tieng_nhat'] = '+'
                tts = "%d" % (i + 1)
                tts = tts + "%s" % (intern.name)
                mapschild['tts'] = tts
                avatars['%d' % (i + 1)] = "%sodoo/get_avatar?intern=%d" % (
                    str(request.httprequest.host_url), intern.id)
                mapschild['avatars'] = avatars
                mapschild['className'] = 'green'

                mapschild['pos'] = {'x': intern.province.x_point, 'y': intern.province.y_point}

                mapschild['col'] = intern.province.column
                mapschild['sort'] = intern.province.sort

                maps[intern.province.id_map] = mapschild
                # for key, value in enumerate(maps.iteritems()):
                listPro.append(mapschild)

            def getKey(item):
                return item['sort']

            listPro.sort(key=getKey)

            maps_return = {}
            maps_return['title'] = invoice.name_of_guild
            maps_return['data'] = listPro

            return json.dumps(maps_return, ensure_ascii=False)

    @http.route('/odoo/get_avatar', type='http',
                auth='public', methods=['GET'])
    def get_avatar(self, **kwargs):
        intern_id = kwargs.get('intern', False)
        intern = request.env['intern.intern'].sudo().browse(int(intern_id))
        streamAvatar = BytesIO()
        if intern.avatar is not None:
            streamAvatar = BytesIO(intern.avatar.decode("base64"))

        return request.make_response(streamAvatar,
                                     [('Content-Type', 'image/jpeg'),
                                      ('Content-Disposition', content_disposition('avatar.jpeg'))])
