from flask import Blueprint, jsonify, request
from peewee import fn
from seedboxsync.core.dao.torrent import Torrent
from seedboxsync.core.dao.download import Download

# Create a Blueprint named 'root'
bp = Blueprint('api', __name__, url_prefix='/api')


@bp.route('/')
def root():
    """
    Default API root.
    """
    return {}


@bp.route('/uploaded', methods=['GET'])
def uploaded():
    """
    Get last uploaded torrents.
    """
    return jsonify(list(
        Torrent.select(
            Torrent.id,
            Torrent.name,
            Torrent.sent
        )
        .limit(get_limit())
        .order_by(Torrent.sent.desc()).dicts()
    ))


@bp.route('/downloaded', methods=['GET'])
def downloaded():
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
        .limit(get_limit())
        .order_by(Download.finished.desc()).dicts()
    ))


@bp.route('/progress', methods=['GET'])
def progress():
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
        .limit(get_limit())
        .order_by(Download.finished.desc()).dicts()
    ))


def get_limit(default=5, max_limit=50):
    """
    Helper which get limit parameter from arg.
    """
    try:
        limit = int(request.args.get('limit', default))
    except (TypeError, ValueError):
        limit = default
    if limit > max_limit or limit < 1:
        limit = default
    return limit
