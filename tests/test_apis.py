from seedboxsync_front.__version__ import __api_path_version__ as api_path_version

DEFAULT = 50
API_PATH = f'/api/{api_path_version}'


def test_404(client):
    response = client.get(f'{API_PATH}/404')
    assert response.status_code == 404
    assert response.json['title'] == 'Not Found'


def test_400(client):
    response = client.get(f'{API_PATH}/downloads?limit=_ERROR_')
    assert response.status_code == 400
    assert response.json['title'] == 'Input payload validation failed'
    assert 'limit' in response.json['message']
    response = client.get(f'{API_PATH}/downloads?limit=5&finished=_ERROR_')
    assert response.status_code == 400
    assert response.json['title'] == 'Input payload validation failed'
    assert 'finished' in response.json['message']


def test_swagger(client):
    response = client.get(f'{API_PATH}/')
    assert response.status_code == 200
    assert b'<title>SeedboxSync API</title>' in response.data  # Is HTML


def test_downloads_list(client):
    # Default
    response = client.get(f'{API_PATH}/downloads')
    assert response.status_code == 200
    assert response.json['data'][2]['finished'] == '2025-05-20T21:50:46'
    assert response.json['data'][2]['id'] == 997
    assert response.json['data'][2]['local_size'] == '3.6GiB'
    assert response.json['data'][2]['path'] == 'FelisSedLacus.ppt'
    assert len(response.json['data']) == DEFAULT
    # With param limit
    response = client.get(f'{API_PATH}/downloads?limit=6')
    assert len(response.json['data']) == 6
    # Out of the limit
    response = client.get(f'{API_PATH}/downloads?limit=1001')
    assert len(response.json['data']) == 1000


def test_downloads(client):
    # Default
    response = client.get(f'{API_PATH}/downloads/1000')
    assert response.status_code == 200
    assert response.json['data']['finished'] == '2025-05-30T01:47:04'
    assert response.json['data']['id'] == 1000
    assert response.json['data']['local_size'] == '3.3GiB'
    assert response.json['data']['path'] == 'Quis.mpeg'


def test_downloads_404(client):
    # Default
    response = client.get(f'{API_PATH}/downloads/9999999')
    assert response.status_code == 404
    assert response.json['title'] == 'Download 9999999 doesn\'t exist'


def test_downloads_list_progress(client):
    # Default
    response = client.get(f'{API_PATH}/downloads?finished=false')
    assert response.status_code == 200
    assert response.json['data'][1]['finished'] == 0
    assert response.json['data'][1]['id'] == 999
    assert response.json['data'][1]['local_size'] == '958.1MiB'
    assert response.json['data'][1]['path'] == 'ConvallisMorbi.doc'
    assert len(response.json['data']) == 2


def test_downloads_stats_by_month(client):
    response = client.get(f'{API_PATH}/downloads/stats/month')
    assert response.status_code == 200
    assert response.json['data'][89]['files'] == 14
    assert response.json['data'][89]['month'] == '2025-02'
    assert response.json['data'][89]['total_size'] == '37.1GiB'
    assert len(response.json['data']) == 93


def test_downloads_stats_by_year(client):
    response = client.get(f'{API_PATH}/downloads/stats/year')
    assert response.status_code == 200
    assert response.json['data'][4]['files'] == 143
    assert response.json['data'][4]['total_size'] == '308.3GiB'
    assert response.json['data'][4]['year'] == '2021'
    assert len(response.json['data']) == 9


def test_uploads_list(client):
    # Default
    response = client.get(f'{API_PATH}/uploads')
    assert response.status_code == 200
    assert response.json['data'][3]['id'] == 247
    assert response.json['data'][3]['name'] == 'SuscipitLigulaIn.torrent'
    assert response.json['data'][3]['sent'] == '2017-10-16T21:13:02.851925'
    assert len(response.json['data']) == DEFAULT
    # With param limit
    response = client.get(f'{API_PATH}/uploads?limit=6')
    assert len(response.json['data']) == 6
    # Out of the limit
    response = client.get(f'{API_PATH}/uploads?limit=1001')
    assert len(response.json['data']) == 250


def test_uploads(client):
    # Default
    response = client.get(f'{API_PATH}/uploads/100')
    assert response.status_code == 200
    assert response.json['data']['sent'] == '2017-09-10T19:52:03.455537'
    assert response.json['data']['id'] == 100
    assert response.json['data']['name'] == 'Justo.torrent'


def test_uploads_404(client):
    # Default
    response = client.get(f'{API_PATH}/uploads/9999999')
    assert response.status_code == 404
    assert response.json['title'] == 'Upload 9999999 doesn\'t exist'


def test_locks_list(client):
    # Default
    response = client.get(f'{API_PATH}/locks')
    assert response.status_code == 200
    assert response.json['data'][0]['key'] == 'sync_blackhole'
    assert response.json['data'][0]['pid'] == 0
    assert response.json['data'][0]['locked'] is False
    assert response.json['data'][0]['locked_at'] == '2025-10-13T15:37:46.747181'
    assert response.json['data'][0]['unlocked_at'] == '2025-10-13T15:37:46.752033'
    assert len(response.json['data']) == 2


def test_locks(client):
    # Default
    response = client.get(f'{API_PATH}/locks/sync_seedbox')
    assert response.status_code == 200
    assert response.json['data']['key'] == 'sync_seedbox'
    assert response.json['data']['pid'] == 84074
    assert response.json['data']['locked'] is True
    assert response.json['data']['locked_at'] == '2025-10-13T15:38:29.652233'
    assert response.json['data']['unlocked_at'] is None


def test_locks_404(client):
    # Default
    response = client.get(f'{API_PATH}/locks/test')
    assert response.status_code == 404
    assert response.json['title'] == 'Lock test doesn\'t exist'
