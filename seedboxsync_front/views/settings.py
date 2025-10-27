# -*- coding: utf-8 -*-
#
# Copyright (C) 2025 Guillaume Kulakowski <guillaume@kulakowski.fr>
#
# For the full copyright and license information, please view the LICENSE
# file that was distributed with this source code.
#
import os
from flask import render_template, current_app
from seedboxsync_front.views import bp
from seedboxsync_front.utils import init_flash


@bp.route('/settings')
def settings() -> str:
    """
    Home page view.
    """
    init_flash()

    # Get YAML config
    yaml_config = current_app.config['CONFIG_YAML_PATH']
    readonly = True
    if os.path.exists(yaml_config) and os.access(yaml_config, os.R_OK):
        readonly = False
    seedbox = current_app.config.get('seedbox') or {}
    local = current_app.config.get('local') or {}
    healthchecks = current_app.config.get('healthchecks') or {}
    hc_sync_seedbox = healthchecks.get('sync_seedbox') or {}
    hc_sync_blackhole = healthchecks.get('sync_blackhole') or {}

    # Build form
    form = {
        'seedbox': {
            'host': seedbox.get('host') or 'my-seedbox.ltd',
            'port': seedbox.get('port') or '22',
            'login': seedbox.get('login') or 'me',
            'password': seedbox.get('password') or 'p4sw0rd',
            'timeout_enabled': seedbox.get('timeout') or False,
            'timeout': seedbox.get('timeout') or '30',
            'protocol': seedbox.get('protocol') or 'sftp',
            'chmod_enabled': seedbox.get('chmod') or False,
            'chmod': seedbox.get('chmod') or '0o644',
            'tmp_path': seedbox.get('tmp_path') or './tmp',
            'watch_path': seedbox.get('watch_path') or './watch',
            'finished_path': seedbox.get('finished_path') or './files',
            'prefixed_path': seedbox.get('prefixed_path') or './files',
            'part_suffix': seedbox.get('part_suffix') or '.part',
            'exclude_syncing': seedbox.get('exclude_syncing') or '',
        },
        'local': {
            'watch_path': local.get('watch_path') or '',
            'download_path': local.get('download_path') or '',
            'db_file': local.get('db_file') or '',
        },
        'healthchecks': {
            'sync_seedbox_enabled': hc_sync_seedbox.get('enabled') or False,
            'sync_seedbox_ping_url': hc_sync_seedbox.get('ping_url') or '',
            'sync_blackhole_enabled': hc_sync_blackhole.get('enabled') or False,
            'sync_blackhole_ping_url': hc_sync_blackhole.get('ping_url') or '',
        }
    }

    return render_template('settings.html', form=form, readonly=readonly)
