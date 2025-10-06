def test_404(client):
    response = client.get('/404')
    assert response.status_code == 404


def test_dashboard(client):
    response = client.get('/')
    assert response.status_code == 200


def test_stats(client):
    response = client.get('/stats')
    assert response.status_code == 200


def test_downloads(client):
    response = client.get('/downloaded')
    assert response.status_code == 200


def test_uploads(client):
    response = client.get('/uploaded')
    assert response.status_code == 200


def test_translation(client, client_translated):
    response = client.get('/')
    assert b'<h1 class="title is-invisible">Dashboard</h1>' in response.data
    response = client_translated.get('/')
    assert b'<h1 class="title is-invisible">Tableau de bord</h1>' in response.data
