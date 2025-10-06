DEFAULT = 5


def test_404(client):
    response = client.get('/api/404')
    assert response.status_code == 404
    assert response.json['title'] == 'Not Found'


def test_500(client):
    response = client.get('/api/downloads?limit=_ERROR_')
    assert response.status_code == 200
    assert len(response.json) == DEFAULT


def test_downloads(client):
    # Default
    response = client.get('/api/downloads')
    assert response.status_code == 200
    assert response.json[2]['finished'] == 'Tue, 20 May 2025 21:50:46 GMT'
    assert response.json[2]['id'] == 997
    assert response.json[2]['local_size'] == '3.6GiB'
    assert response.json[2]['path'] == 'FelisSedLacus.ppt'
    assert len(response.json) == DEFAULT
    # With param limit
    response = client.get('/api/downloads?limit=6')
    assert len(response.json) == 6
    # Out of the limit
    response = client.get('/api/downloads?limit=1001')
    assert len(response.json) == DEFAULT


def test_progress(client):
    # Default
    response = client.get('/api/progress')
    assert response.status_code == 200
    assert response.json[1]['finished'] == 0
    assert response.json[1]['id'] == 999
    assert response.json[1]['local_size'] == '958.1MiB'
    assert response.json[1]['path'] == 'ConvallisMorbi.doc'
    assert len(response.json) == 2
    # With param limit
    response = client.get('/api/progress?limit=1')
    assert len(response.json) == 1
    # Out of the limit
    response = client.get('/api/progress?limit=1001')
    assert len(response.json) == 2


def test_stats_by_month(client):
    response = client.get('/api/stats-by-month')
    assert response.status_code == 200
    assert response.json[89]['files'] == 14
    assert response.json[89]['month'] == '2025-02'
    assert response.json[89]['total_size'] == '37.1GiB'
    assert len(response.json) == 93


def test_stats_by_year(client):
    response = client.get('/api/stats-by-year')
    assert response.status_code == 200
    assert response.json[4]['files'] == 143
    assert response.json[4]['total_size'] == '308.3GiB'
    assert response.json[4]['year'] == '2021'
    assert len(response.json) == 9


def test_uploads(client):
    # Default
    response = client.get('/api/uploads')
    assert response.status_code == 200
    assert response.json[3]['id'] == 247
    assert response.json[3]['name'] == 'SuscipitLigulaIn.torrent'
    assert response.json[3]['sent'] == 'Mon, 16 Oct 2017 21:13:02 GMT'
    assert len(response.json) == DEFAULT
    # With param limit
    response = client.get('/api/uploads?limit=6')
    assert len(response.json) == 6
    # Out of the limit
    response = client.get('/api/uploads?limit=1001')
    assert len(response.json) == DEFAULT
