# -*- coding: utf-8 -*-
#
# Copyright (C) 2025 Guillaume Kulakowski <guillaume@kulakowski.fr>
#
# For the full copyright and license information, please view the LICENSE
# file that was distributed with this source code.
#
from flask import current_app, flash, request
from seedboxsync.core.dao.download import Download
from peewee import fn


def init_flash() -> None:
    """
    Initialize flash messages.
    """
    if current_app.config.get('INIT_ERROR'):
        flash(current_app.config['INIT_ERROR'], 'error')


def get_limit(default: int = 5, max_limit: int = 1000) -> int:
    """
    Helper which get limit parameter from arg.

    Args:
        default (int): Default limit if not set or invalid (default: 5).
        max_limit (int): Max limit accepted (default: 1000).

    Returns:
        int: limit value.
    """
    try:
        limit = int(request.args.get('limit', default))
    except (TypeError, ValueError):
        limit = default
    if limit > max_limit or limit < 1:
        limit = default

    return limit


def sizeof(num: float, suffix: str = 'B') -> str:
    """
    Convert in human readable units.
    From: https://stackoverflow.com/a/1094933

    Args:
        num (int): Value not human readable.
        suffix (str): Suffix for value given to (default: B).

    Returns:
        str: Human readable value.
    """
    for unit in ("", "Ki", "Mi", "Gi", "Ti", "Pi", "Ei", "Zi"):
        if abs(num) < 1024.0:
            return f"{num:3.1f}{unit}{suffix}"
        num /= 1024.0
    return f"{num:.1f}Yi{suffix}"


def byte_to_gi(bytes_value: float, suffix: str = 'B') -> str:
    """
    Convert in human readable units.

    Args:
        bytes_value (integer): Value not human readable.
        suffix (str): Suffix for value given to (default: B).

    Returns:
        str: human readable value in Gi.
    """
    gib = bytes_value / (1024**3)
    return f"{gib:.1f}Gi{suffix}"


def stats_by_period(period: str) -> list[dict[str, str | float]]:
    """
    Generic stats by period (month or year).

    Args:
        period (str): 'month' or 'year'.

    Returns:
        dict: List of dict with period, files count and total size in GiB.
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


def get_locale() -> str | None:
    """
    Get locale from browser.

    Returns:
        str: The local.
    """
    return request.accept_languages.best_match(['fr', 'en'])
