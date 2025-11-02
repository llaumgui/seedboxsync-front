# -*- coding: utf-8 -*-
#
# Copyright (C) 2025 Guillaume Kulakowski <guillaume@kulakowski.fr>
#
# For the full copyright and license information, please view the LICENSE
# file that was distributed with this source code.
#
import os
from typing import Any, Dict, Iterable
from ruamel.yaml import YAML
from ruamel.yaml.scalarstring import PlainScalarString
from flask import current_app, flash, render_template, request
from flask.wrappers import Request
from flask_babel import gettext
from seedboxsync_front.views import bp
from seedboxsync_front.utils import init_flash


@bp.route('/settings', methods=('GET', 'POST'))
def settings() -> str:
    """
    Manage settings: load YAML, display form, persist changes.
    """
    init_flash()
    saved = False

    yaml = _get_ruamel_yaml()  # <-- utilise l'instance avec representer
    yaml.preserve_quotes = False

    yaml_path = current_app.config.get('CONFIG_YAML_PATH')
    if not yaml_path:
        current_app.logger.error("No CONFIG_YAML_PATH found")
        flash(gettext("Configuration .yml not found."))
        return render_template('settings.html', form={}, readonly=True, saved=False)

    form = _load_yaml_into_form(yaml, yaml_path)

    readonly = not (os.path.exists(yaml_path) and os.access(yaml_path, os.R_OK | os.W_OK))

    if request.method == 'POST':
        missing = [f for f in _required_form_fields() if not request.form.get(f)]
        if readonly:
            flash(gettext('The configuration is read-only. Check the permissions.'), "error")
        elif missing:
            flash(gettext('Missing required fields: %(missing)s', missing=", ".join(missing)), "error")
        else:
            try:
                _save_form_to_yaml(yaml, yaml_path, request)
                form = _load_yaml_into_form(yaml, yaml_path)  # reload cleaned values
                saved = True
            except Exception as e:
                current_app.logger.exception("Failed to save YAML config", exc_info=e)
                flash(gettext("Failed to save configuration."), "error")

    return render_template('settings.html', form=form, readonly=readonly, saved=saved)


# -------------------------
# Helpers
# -------------------------
class OctalInt(int):
    """Class for octal integers in YAML representation."""
    pass


def _get_ruamel_yaml() -> YAML:
    """
    Create a ruamel.yaml YAML instance with custom representer for OctalInt.
    """
    yaml = YAML()

    def _represent_octal(dumper: Any, data: Any) -> Any:
        """Format en 0oNNN et tagger comme int YAML"""
        return dumper.represent_scalar('tag:yaml.org,2002:int', format(int(data), '#o'))
    yaml.representer.add_representer(OctalInt, _represent_octal)
    return yaml


def _required_form_fields() -> Iterable[str]:
    return [
        'seedbox_host', 'seedbox_port', 'seedbox_login',
        'seedbox_password', 'seedbox_protocol', 'seedbox_tmp_path',
        'seedbox_watch_path', 'seedbox_finished_path', 'seedbox_part_suffix'
    ]


def _load_yaml(yaml: YAML, path: str) -> Dict[str, Any]:
    if not os.path.exists(path):
        return {}
    with open(path, "r", encoding="utf-8") as f:
        return yaml.load(f) or {}


def _load_yaml_into_form(yaml: YAML, path: str) -> Dict[str, Dict[str, Any]]:
    data = _load_yaml(yaml, path)

    seedbox = data.get('seedbox', {})
    local = data.get('local', {})
    hc = data.get('healthchecks', {})
    hc_seedbox = hc.get('sync_seedbox', {})
    hc_blackhole = hc.get('sync_blackhole', {})

    # Présenter chmod sous forme '0oNNN' pour le formulaire
    chmod_raw = seedbox.get('chmod', '0o644')
    if isinstance(chmod_raw, int):
        chmod_display = PlainScalarString(format(chmod_raw, '#o'))
    else:
        # deja une chaine (ex: '0o777') ou autre -> forcer string
        chmod_display = PlainScalarString(str(chmod_raw))

    return {
        'seedbox': {
            'host': str(seedbox.get('host', 'my-seedbox.ltd')),
            'port': str(seedbox.get('port', '22')),
            'login': str(seedbox.get('login', 'me')),
            'password': str(seedbox.get('password', 'p4sw0rd')),
            'timeout_enabled': bool(seedbox.get('timeout', False)),
            'timeout': str(seedbox.get('timeout', '30')),
            'protocol': str(seedbox.get('protocol', 'sftp')),
            'chmod_enabled': bool(seedbox.get('chmod', False)),
            'chmod': chmod_display,
            'tmp_path': str(seedbox.get('tmp_path', './tmp')),
            'watch_path': str(seedbox.get('watch_path', './watch')),
            'finished_path': str(seedbox.get('finished_path', './files')),
            'prefixed_path': str(seedbox.get('prefixed_path', './files')),
            'part_suffix': str(seedbox.get('part_suffix', '.part')),
            'exclude_syncing': str(seedbox.get('exclude_syncing', '')),
        },
        'local': {
            'watch_path': str(local.get('watch_path', '')),
            'download_path': str(local.get('download_path', '')),
            'db_file': str(local.get('db_file', '')),
        },
        'healthchecks': {
            'sync_seedbox_enabled': bool(hc_seedbox.get('enabled', False)),
            'sync_seedbox_ping_url': str(hc_seedbox.get('ping_url', '')),
            'sync_blackhole_enabled': bool(hc_blackhole.get('enabled', False)),
            'sync_blackhole_ping_url': str(hc_blackhole.get('ping_url', '')),
        },
    }


def _save_form_to_yaml(yaml: YAML, path: str, req: Request) -> None:
    yaml_data = _load_yaml(yaml, path)

    # ensure sections exist
    yaml_data.setdefault('seedbox', {})
    yaml_data.setdefault('local', {})
    yaml_data.setdefault('healthchecks', {})
    yaml_data['healthchecks'].setdefault('sync_seedbox', {})
    yaml_data['healthchecks'].setdefault('sync_blackhole', {})

    # Flat mappings: section -> list of fields
    mappings = {
        'seedbox': [
            'host', 'port', 'login', 'password', 'protocol', 'tmp_path',
            'watch_path', 'finished_path', 'prefixed_path', 'part_suffix', 'exclude_syncing'
        ],
        'local': ['watch_path', 'download_path', 'db_file'],
    }

    # Update simple fields
    for section, fields in mappings.items():
        for field in fields:
            key = f"{section}_{field}"
            val = req.form.get(key)
            if val is not None:
                yaml_data[section][field] = val

    # Healthchecks nested
    for hc_name in ('sync_seedbox', 'sync_blackhole'):
        enabled = bool(req.form.get(f"healthchecks_{hc_name}_enabled") or req.form.get(f"{hc_name}_enabled"))
        ping_key = f"healthchecks_{hc_name}_ping_url"
        ping_val = req.form.get(ping_key) or req.form.get(f"{hc_name}_ping_url") or ""
        yaml_data['healthchecks'].setdefault(hc_name, {})
        yaml_data['healthchecks'][hc_name]['enabled'] = enabled
        yaml_data['healthchecks'][hc_name]['ping_url'] = ping_val

    # Special seedbox numeric fields (timeout) and chmod (octal)
    # timeout
    timeout_enabled = bool(req.form.get('seedbox_timeout_enabled'))
    timeout_val = req.form.get('seedbox_timeout')
    if timeout_enabled and timeout_val:
        try:
            yaml_data['seedbox']['timeout'] = int(timeout_val)
        except ValueError:
            raise ValueError("Invalid timeout value")
    else:
        yaml_data['seedbox']['timeout'] = False

    # chmod
    chmod_enabled = bool(req.form.get('seedbox_chmod_enabled'))
    chmod_val = req.form.get('seedbox_chmod')
    if chmod_enabled and chmod_val:
        s = str(chmod_val).strip()
        # accept formats like "0o644" or "644"
        if s.startswith('0o'):
            digits = s[2:]
        else:
            digits = s
        # validate octal digits
        if not digits or any(ch not in '01234567' for ch in digits):
            raise ValueError("Invalid chmod value")
        # store as OctalInt so ruamel writes: chmod: 0oNNN (unquoted)
        yaml_data['seedbox']['chmod'] = OctalInt(int(digits, 8))
    else:
        yaml_data['seedbox']['chmod'] = False

    # Persist file
    with open(path, "w", encoding="utf-8") as f:
        yaml.dump(yaml_data, f)
