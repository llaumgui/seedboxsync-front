# -*- coding: utf-8 -*-
#
# Copyright (C) 2025 Guillaume Kulakowski <guillaume@kulakowski.fr>
#
# For the full copyright and license information, please view the LICENSE
# file that was distributed with this source code.
#
from flask import jsonify, Response
from peewee import fn
from seedboxsync.core.dao import Download
from seedboxsync_front.views.api import bp
from seedboxsync_front.utils import get_limit


@bp.route('/downloads', methods=['GET'])
def downloads() -> Response:
    """
    Get last downloaded files.
    """
    return jsonify(list(
        Download.select(
            Download.id,
            Download.path,
            Download.finished,
            fn.sizeof(Download.local_size)
        )
        .where(Download.finished != 0)
        .limit(get_limit())
        .order_by(Download.finished.desc()).dicts()
    ))
