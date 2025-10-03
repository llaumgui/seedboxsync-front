# -*- coding: utf-8 -*-
#
# Copyright (C) 2025 Guillaume Kulakowski <guillaume@kulakowski.fr>
#
# For the full copyright and license information, please view the LICENSE
# file that was distributed with this source code.
#
from flask import render_template
from . import bp
from ..cache import cache
from ..utils import init_flash


@bp.route('/uploaded')
@cache.cached(timeout=300)
def uploaded() -> str:
    """
    Uploaded list controller.
    """
    init_flash()

    return render_template('uploaded.html')
