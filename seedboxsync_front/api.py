from flask import Blueprint, jsonify
from seedboxsync.core.dao.torrent import Torrent
from seedboxsync.core.dao.download import Download
from playhouse.shortcuts import model_to_dict

# Create a Blueprint named 'root'
bp = Blueprint('api', __name__, url_prefix='/api')

@bp.route('/')
def root():
    return {}

@bp.route('/downloaded', methods=['GET'])
def downloaded():
    # DB query
    data = Torrent.select(Torrent.id,
                          Torrent.name,
                          Torrent.sent).limit(10).order_by(Torrent.sent.desc()).dicts()
    return jsonify(list(data))
