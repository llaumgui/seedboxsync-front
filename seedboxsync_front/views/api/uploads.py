# -*- coding: utf-8 -*-
#
# Copyright (C) 2025 Guillaume Kulakowski <guillaume@kulakowski.fr>
#
# For the full copyright and license information, please view the LICENSE
# file that was distributed with this source code.
#
from flask import jsonify, Response
from seedboxsync.core.dao import Torrent
from seedboxsync_front.views.api import bp
from seedboxsync_front.utils import get_limit


@bp.route('/uploads', methods=['GET'])
def uploads() -> Response:
    """
    Get last uploaded torrents.
    """
    return jsonify(list(
        Torrent.select(
            Torrent.id,
            Torrent.name,
            Torrent.sent
        )
        .limit(get_limit())
        .order_by(Torrent.sent.desc()).dicts()
    ))
