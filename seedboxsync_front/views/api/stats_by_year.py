# -*- coding: utf-8 -*-
#
# Copyright (C) 2025 Guillaume Kulakowski <guillaume@kulakowski.fr>
#
# For the full copyright and license information, please view the LICENSE
# file that was distributed with this source code.
#
from flask import jsonify, Response
from seedboxsync_front.views.api import bp
from seedboxsync_front.utils import stats_by_period
from seedboxsync_front.cache import cache


@bp.route('/stats-by-year', methods=['GET'])
@cache.cached(timeout=3600)
def stats_by_year() -> Response:
    """
    Get Download statistics by year.
    """
    return jsonify(stats_by_period('year'))
