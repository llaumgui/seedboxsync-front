# -*- coding: utf-8 -*-
#
# Copyright (C) 2025 Guillaume Kulakowski <guillaume@kulakowski.fr>
#
# For the full copyright and license information, please view the LICENSE
# file that was distributed with this source code.
#
from flask import render_template
from seedboxsync.core.dao.download import Download
from . import bp
from ..cache import cache
from ..utils import init_flash, sizeof, stats_by_period


@bp.route('/stats')
@cache.cached(timeout=3600)
def stats() -> str:
    """
    Stats page controller.
    """
    init_flash()

    query = Download.select().where(Download.finished != 0)
    total_files = query.count()
    total_size = sum([d.seedbox_size for d in query if d.seedbox_size])

    stats_total = {
        'files': total_files,
        'total_size': sizeof(total_size),
    }

    stats_month = stats_by_period('month')
    stats_year = stats_by_period('year')

    return render_template('stats.html', stats_total=stats_total, stats_month=stats_month, stats_year=stats_year)
