# -*- coding: utf-8 -*-
#
# Copyright (C) 2025 Guillaume Kulakowski <guillaume@kulakowski.fr>
#
# For the full copyright and license information, please view the LICENSE
# file that was distributed with this source code.
#
from flask import jsonify, Response
from seedboxsync.core.dao.torrent import Torrent
from . import bp
from ...utils import get_limit


@bp.route('/uploaded', methods=['GET'])
def uploaded() -> Response:
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
