# SeedboxSync frontend

[![Author][ico-bluesky]][link-bluesky]
[![Software License][ico-license]](LICENSE)
[![Build Status][ico-ghactions]][link-ghactions]
[![Latest Version][ico-pypi-version]][link-pypi]
[![Docker Pull][ico-docker]][link-docker]
[![Latest Version][ico-version]][link-docker]

[![Quality Gate Status][ico-sonarcloud-gate]][link-sonarcloud-gate]
[![Coverage][ico-sonarcloud-coverage]][link-sonarcloud-coverage]
[![Maintainability Rating][ico-sonarcloud-maintainability]][link-sonarcloud-maintainability]
[![Reliability Rating][ico-sonarcloud-reliability]][link-sonarcloud-reliability]
[![Security Rating][ico-sonarcloud-security]][link-sonarcloud-security]

## For users

ToDo

## For developers

### frontend development

Use [Bulma](https://bulma.io/) / [Vanilla](https://vanilla-js.com/) / [Alpine.js](https://alpinejs.dev/) / [Vite](https://vite.dev) / :

```bash
npm i
npm run dev
```

### Python development

```bash
python3 -m venv .venv
. .venv/bin/activate
pip install -e .
flask --app seedboxsync_front run --debug
```

## License

Released under the [GPL v2](http://opensource.org/licenses/GPL-2.0).

[ico-bluesky]: https://img.shields.io/static/v1?label=Author&message=llaumgui&color=208bfe&logo=bluesky&style=flat-square
[link-bluesky]: https://bsky.app/profile/llaumgui.kulakowski.fr
[ico-ghactions]: https://img.shields.io/github/actions/workflow/status/llaumgui/seedboxsync-front/devops.yml?branch=main&style=flat-square&logo=github&label=DevOps
[link-ghactions]: https://github.com/llaumgui/seedboxsync-front/actions
[ico-pypi-version]: https://img.shields.io/pypi/v/seedboxsync-front?include_prereleases&label=Package%20version&style=flat-square&logo=python
[link-pypi]:https://pypi.org/project/seedboxsync-front/
[ico-license]: https://img.shields.io/github/license/llaumgui/seedboxsync-front?style=flat-square
[ico-docker]: https://img.shields.io/docker/pulls/llaumgui/seedboxsync-front?color=%2496ed&logo=docker&style=flat-square
[link-docker]: https://hub.docker.com/r/llaumgui/seedboxsync-front
[ico-version]: https://img.shields.io/docker/v/llaumgui/seedboxsync-front?sort=semver&color=%2496ed&logo=docker&style=flat-square
[ico-sonarcloud-gate]: https://sonarcloud.io/api/project_badges/measure?branch=main&project=llaumgui_seedboxsync-front&metric=alert_status
[link-sonarcloud-gate]: https://sonarcloud.io/dashboard?id=llaumgui_seedboxsync-front&branch=main
[ico-sonarcloud-coverage]: https://sonarcloud.io/api/project_badges/measure?project=llaumgui_seedboxsync-front&metric=coverage
[link-sonarcloud-coverage]: https://sonarcloud.io/dashboard?id=llaumgui_seedboxsync-front
[ico-sonarcloud-maintainability]: https://sonarcloud.io/api/project_badges/measure?project=llaumgui_seedboxsync-front&metric=sqale_rating
[link-sonarcloud-maintainability]: https://sonarcloud.io/dashboard?id=llaumgui_seedboxsync-front
[ico-sonarcloud-reliability]: https://sonarcloud.io/api/project_badges/measure?project=llaumgui_seedboxsync-front&metric=reliability_rating
[link-sonarcloud-reliability]: https://sonarcloud.io/dashboard?id=llaumgui_seedboxsync-front
[ico-sonarcloud-security]: https://sonarcloud.io/api/project_badges/measure?project=llaumgui_seedboxsync-front&metric=security_rating
[link-sonarcloud-security]: https://sonarcloud.io/dashboard?id=llaumgui_seedboxsync-front

