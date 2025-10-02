# -*- coding: utf-8 -*-
#
# Copyright (C) 2025 Guillaume Kulakowski <guillaume@kulakowski.fr>
#
# For the full copyright and license information, please view the LICENSE
# file that was distributed with this source code.
#
import uuid
from flask import jsonify, Response
from werkzeug.exceptions import HTTPException
from datetime import datetime


def error(e: Exception) -> tuple[Response, int | None]:
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
