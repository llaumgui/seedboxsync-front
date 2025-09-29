# -*- coding: utf-8 -*-
#
# Copyright (C) 2025 Guillaume Kulakowski <guillaume@kulakowski.fr>
#
# For the full copyright and license information, please view the LICENSE
# file that was distributed with this source code.
#
import uuid
from flask import Blueprint, jsonify, request, Response
from peewee import fn
from werkzeug.exceptions import HTTPException
from datetime import datetime
from seedboxsync.core.dao.torrent import Torrent
from seedboxsync.core.dao.download import Download

# Create a Blueprint named 'api'
bp = Blueprint('api', __name__, url_prefix='/api')


def __get_limit(default: int = 5, max_limit: int = 50) -> int:
    """
    Helper which get limit parameter from arg.
    :param default: default limit if not set or invalid (default: 5).
    :param max_limit: max limit accepted (default: 50).
    :return: integer, limit value.
    """
    try:
        limit = int(request.args.get('limit', default))
    except (TypeError, ValueError):
        limit = default
    if limit > max_limit or limit < 1:
        limit = default

    return limit


def api_error(e: Exception) -> tuple[Response, int | None]:
    """
    Global error handler.
    :param e: Exception
    :return: Rendered error template with status code
    """
    status_code = e.code if isinstance(e, HTTPException) else 500
    title = e.name if isinstance(e, HTTPException) else "Internal Server Error"
    detail = e.description if isinstance(e, HTTPException) else str(e)

    return jsonify({
        "type": "about:blank",
        "title": title,
        "status": status_code,
        "detail": detail,
        "timestamp": datetime.now().astimezone().isoformat(),
        "traceId": str(uuid.uuid4())
    }), status_code


@bp.route('/')
def root() -> Response:
    """
    Default API root.
    """
    return jsonify({})


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
        .limit(__get_limit())
        .order_by(Torrent.sent.desc()).dicts()
    ))


@bp.route('/downloaded', methods=['GET'])
def downloaded() -> Response:
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
        .limit(__get_limit())
        .order_by(Download.finished.desc()).dicts()
    ))


@bp.route('/progress', methods=['GET'])
def progress() -> Response:
    """
    Get files in progress.
    """
    return jsonify(list(
        Download.select(
            Download.id,
            Download.path,
            Download.finished,
            fn.sizeof(Download.local_size)
        )
        .where(Download.finished == 0)
        .limit(__get_limit())
        .order_by(Download.finished.desc()).dicts()
    ))
