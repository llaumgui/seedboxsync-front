# -*- coding: utf-8 -*-
#
# Copyright (C) 2025 Guillaume Kulakowski <guillaume@kulakowski.fr>
#
# For the full copyright and license information, please view the LICENSE
# file that was distributed with this source code.
#
import os
from flask import current_app, flash, render_template, request
from seedboxsync_front.views import bp
from seedboxsync_front.utils import init_flash


@bp.route('/settings', methods=('GET', 'POST'))
def settings() -> str:
    """
    Home page view.
    """
    init_flash()

    # List of required form fields
    required_fields = [
        'seedbox_host', 'seedbox_port', 'seedbox_login',
        'seedbox_password'
    ]

    if request.method == 'POST':
        # Check for missing required fields
        missing = [f for f in required_fields if not request.form.get(f)]
        if missing:
            flash(f"Missing required fields: {', '.join(missing)}")
        else:
            flash('OK')
            # redirect(url_for('blog.index'))  # Enable later if needed

    # Get YAML config
    yaml_config = current_app.config['CONFIG_YAML_PATH']
    readonly = True
    if os.path.exists(yaml_config) and os.access(yaml_config, os.R_OK):
        readonly = False
    seedbox = current_app.config.get('seedbox', {})
    local = current_app.config.get('local', {})
    healthchecks = current_app.config.get('healthchecks', {})
    hc_sync_seedbox = healthchecks.get('sync_seedbox', {})
    hc_sync_blackhole = healthchecks.get('sync_blackhole', {})

    # Build form
    def with_default(d, key, default):
        """Return a value from a dict or a default value if key is missing."""
        return d.get(key, default)
    form = {
        'seedbox': {
            'host': with_default(seedbox, 'host', 'my-seedbox.ltd'),
            'port': with_default(seedbox, 'port', '22'),
            'login': with_default(seedbox, 'login', 'me'),
            'password': with_default(seedbox, 'password', 'p4sw0rd'),
            'timeout_enabled': with_default(seedbox, 'timeout', False),
            'timeout': with_default(seedbox, 'timeout', '30'),
            'protocol': with_default(seedbox, 'protocol', 'sftp'),
            'chmod_enabled': with_default(seedbox, 'chmod', False),
            'chmod': with_default(seedbox, 'chmod', '0o644'),
            'tmp_path': with_default(seedbox, 'tmp_path', './tmp'),
            'watch_path': with_default(seedbox, 'watch_path', './watch'),
            'finished_path': with_default(seedbox, 'finished_path', './files'),
            'prefixed_path': with_default(seedbox, 'prefixed_path', './files'),
            'part_suffix': with_default(seedbox, 'part_suffix', '.part'),
            'exclude_syncing': with_default(seedbox, 'exclude_syncing', ''),
        },
        'local': {
            'watch_path': with_default(local, 'watch_path', ''),
            'download_path': with_default(local, 'download_path', ''),
            'db_file': with_default(local, 'db_file', ''),
        },
        'healthchecks': {
            'sync_seedbox_enabled': with_default(hc_sync_seedbox, 'enabled', False),
            'sync_seedbox_ping_url': with_default(hc_sync_seedbox, 'ping_url', ''),
            'sync_blackhole_enabled': with_default(hc_sync_blackhole, 'enabled', False),
            'sync_blackhole_ping_url': with_default(hc_sync_blackhole, 'ping_url', ''),
        }
    }

    return render_template('settings.html', form=form, readonly=readonly)
