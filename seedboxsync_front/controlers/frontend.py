# -*- coding: utf-8 -*-
#
# Copyright (C) 2025 Guillaume Kulakowski <guillaume@kulakowski.fr>
#
# For the full copyright and license information, please view the LICENSE
# file that was distributed with this source code.
#
from flask import current_app, Blueprint, render_template, flash
from peewee import fn
from werkzeug.exceptions import HTTPException
from seedboxsync.core.dao.download import Download
from ..db import sizeof, byte_to_gi
from .. import cache

# Create a Blueprint named 'frontend'
bp = Blueprint('frontend', __name__)


def __init_flash() -> None:
    """
    Initialize flash messages.
    """
    if current_app.config.get('INIT_ERROR'):
        flash(current_app.config['INIT_ERROR'], 'error')


def __stats_by_period(period: str) -> list[dict[str, str | float]]:
    """
    Generic stats by period (month or year).
    :param period: 'month' or 'year'.
    :return: list of dict with period, files count and total size in GiB.
    """
    strftime_format = "%Y-%m" if period == "month" else "%Y"

    data = Download.select(
        Download.id,
        Download.finished,
        fn.strftime(strftime_format, Download.finished).alias(period),
        Download.seedbox_size,
    ).where(Download.finished != 0).order_by(Download.finished.desc()).dicts()

    tmp = {}
    for download in data:
        key = download[period]
        size = download['seedbox_size']
        if not key or not size:
            continue
        if key not in tmp:
            tmp[key] = {"files": 0, "total_size": 0.0}
        tmp[key]["files"] += 1
        tmp[key]["total_size"] += size

    return [
        {
            period: key,
            "files": tmp[key]["files"],
            "total_size": byte_to_gi(tmp[key]["total_size"]),
        }
        for key in sorted(tmp)
    ]


def page_error(e: Exception) -> tuple[str, int | None]:
    """
    Global error handler.
    :param e: Exception
    :return: Rendered error template with status code
    """
    status_code = e.code if isinstance(e, HTTPException) else 500
    title = e.name if isinstance(e, HTTPException) else "Internal Server Error"
    detail = e.description if isinstance(e, HTTPException) else str(e)

    return render_template("error.html", title=title, detail=detail), status_code


@bp.route('/')
@cache.cache.cached(timeout=300)
def homepage() -> str:
    """
    Home page controller.
    """
    print("Home page accessed")
    __init_flash()

    return render_template('homepage.html')


@bp.route('/stats')
@cache.cache.cached(timeout=3600)
def stats() -> str:
    """
    Stats page controller.
    """
    print("Stats page accessed")
    __init_flash()

    query = Download.select().where(Download.finished != 0)
    total_files = query.count()
    total_size = sum([d.seedbox_size for d in query if d.seedbox_size])

    stats_total = {
        'files': total_files,
        'total_size': sizeof(total_size),
    }

    stats_month = __stats_by_period('month')
    stats_year = __stats_by_period('year')

    return render_template('stats.html', stats_total=stats_total, stats_month=stats_month, stats_year=stats_year)
