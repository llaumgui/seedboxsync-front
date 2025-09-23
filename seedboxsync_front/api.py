from flask import Blueprint, jsonify, request
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

@bp.route('/downloaded', methods=['GET'])
def downloaded():
    """
    Get last downloaded torrents.
    """
    limit = get_limit()
    # DB query
    data = Torrent.select(Torrent.id,
                          Torrent.name,
                          Torrent.sent).limit(limit).order_by(Torrent.sent.desc()).dicts()
    return jsonify(list(data))

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
