# -*- coding: utf-8 -*-
#
# Copyright (C) 2025 Guillaume Kulakowski <guillaume@kulakowski.fr>
#
# For the full copyright and license information, please view the LICENSE
# file that was distributed with this source code.
#
from flask_restx import fields, inputs, Namespace, reqparse
from peewee import fn
from typing import Any
from seedboxsync_front.cache import cache
from seedboxsync.core.dao import Download
from seedboxsync_front.apis import DateTimeOrZero, Resource
from seedboxsync_front.utils import byte_to_gi

api = Namespace('downloads', description='Operations related to download management')


# ==========================
# Models
# ==========================
download_model = api.model('Download', {
    'id': fields.Integer(required=True, description="Unique identifier of the download record"),
    'path': fields.String(required=True, description="Local path of the downloaded file"),
    'started': fields.DateTime(dt_format='iso8601', required=True, description="Download start timestamp"),
    'finished': DateTimeOrZero(dt_format='iso8601', required=False, description="Download completion timestamp"),
    'local_size': fields.String(required=True, description="File size on local storage"),
    'seedbox_size': fields.String(required=True, description="File size on seedbox storage"),
})
download_list_envelope = Resource.build_envelope_model(api, 'Downloads', download_model)
download_envelope = Resource.build_envelope_model(api, 'Download', download_model)

stats_month_model = api.model('StatsMonth', {
    'files': fields.Integer(required=True, description="Number of files downloaded in the month"),
    'month': fields.String(
        required=True,
        description="Year and month of the statistics (format: yyyy-mm)",
        pattern=r'^\d{4}-(0[1-9]|1[0-2])$'
    ),
    'total_size': fields.String(required=True, description="Total size of files downloaded"),
})
stats_month_envelope = Resource.build_envelope_model(api, 'StatsMonth', stats_month_model)

stats_year_model = api.model('StatsYear', {
    'files': fields.Integer(required=True, description="Number of files downloaded in the year"),
    'year': fields.String(
        required=True,
        description="Year of the statistics (format: yyyy)",
        pattern=r'^\d{4}$'
    ),
    'total_size': fields.String(required=True, description="Total size of files downloaded"),
})
stats_year_envelope = Resource.build_envelope_model(api, 'StatsYear', stats_year_model)


# ==========================
# Request parser
# ==========================
parser = reqparse.RequestParser()
parser.add_argument(
    'limit',
    type=int,
    required=False,
    default=50,
    help='Maximum number of items to return (min=5, max=1000)',
    location='args'
)
parser.add_argument(
    'finished',
    type=inputs.boolean,
    required=False,
    default=None,
    help='Filter only completed downloads (true) or in-progress downloads (false)',
    location='args'
)


# ==========================
# Endpoints
# ==========================
@api.route('')
class DownloadsList(Resource):
    """
    Endpoint for managing downloads list.

    Provides a list of downloads with optional filtering for in-progress or completed files.
    """

    @api.doc('list_downloads')  # type: ignore[misc]
    @api.expect(parser)  # type: ignore[misc]
    @api.marshal_with(download_list_envelope, code=200, description="List of downloads")  # type: ignore[misc]
    def get(self) -> dict[str, Any]:
        """
        Retrieve a list of recent downloads.

        Query Parameters:
        - limit: Maximum number of downloads to return (default=50)
        - progress: Filter downloads by status (true=in-progress, false=finished)
        """
        args = parser.parse_args()
        limit = self.set_limit(args.get('limit'))
        finished = args.get('finished')

        query = Download.select(
            Download.id,
            Download.path,
            Download.started,
            Download.finished,
            fn.sizeof(Download.local_size),
            fn.sizeof(Download.seedbox_size)
        ).limit(limit).order_by(Download.finished.desc())

        if finished is not None:
            # Filter downloads by completion status
            if finished:
                query = query.where(Download.finished != 0)
            else:
                query = query.where(Download.finished == 0)

        return self.build_envelope(list(query.dicts()), 'Download', 200)


@api.route('/<int:id>')
@api.response(404, 'Download not found')
@api.param('id', 'The download identifier')
class Downloads(Resource):
    """
    Endpoint for managing downloads.

    Provides downloads operations.
    """

    @api.doc('get_download')  # type: ignore[misc]
    @api.marshal_with(download_envelope, code=200, description="Download element")  # type: ignore[misc]
    def get(self, id: int) -> dict[str, Any]:
        """
        Retrieve a download.
        """
        try:
            result = Download.select(
                Download.id,
                Download.path,
                Download.started,
                Download.finished,
                fn.sizeof(Download.local_size),
                fn.sizeof(Download.seedbox_size)
            ).where(Download.id == id).dicts().get()
        except Download.DoesNotExist:
            api.abort(404, "Download {} doesn't exist".format(id))

        return self.build_envelope(result, 'Download', 200)


@api.route('/stats/month')
class DownloadsStatsByMonth(Resource):
    """
    Endpoint to retrieve monthly download statistics.
    """

    @cache.cached(timeout=3600)
    @api.doc('stats_downloads_by_month')  # type: ignore[misc]
    @api.marshal_with(stats_month_envelope, code=200, description="Download statistics aggregated by month")  # type: ignore[misc]
    def get(self) -> dict[str, Any]:
        """
        Return download statistics grouped by month.

        Returns the number of files downloaded and total size per month.
        """
        return self.build_envelope(stats_by_period('month'), 'StatsMonth', 200)


@api.route('/stats/year')
class DownloadsStatsByYear(Resource):
    """
    Endpoint to retrieve yearly download statistics.
    """

    @cache.cached(timeout=3600)
    @api.doc('stats_downloads_by_year')  # type: ignore[misc]
    @api.marshal_with(stats_year_envelope, code=200, description="Download statistics aggregated by year")  # type: ignore[misc]
    def get(self) -> dict[str, Any]:
        """
        Return download statistics grouped by year.

        Returns the number of files downloaded and total size per year.
        """
        return self.build_envelope(stats_by_period('year'), 'StatsYear', 200)


# ==========================
# Utility functions
# ==========================
def stats_by_period(period: str) -> list[dict[str, str | float]]:
    """
    Compute aggregated download statistics by period (month or year).

    Args:
        period (str): Aggregation period, either 'month' or 'year'.

    Returns:
        list[dict[str, str | float]]: List of statistics including period, number of files,
                                      and total size.
    """
    strftime_format = "%Y-%m" if period == "month" else "%Y"

    data = Download.select(
        Download.id,
        Download.finished,
        fn.strftime(strftime_format, Download.finished).alias(period),
        Download.seedbox_size,
    ).where(Download.finished != 0).order_by(Download.finished.desc()).dicts()

    tmp = {}
    for download in data:
        key = download[period]
        size = download['seedbox_size']
        if not key or not size:
            continue
        if key not in tmp:
            tmp[key] = {"files": 0, "total_size": 0.0}
        tmp[key]["files"] += 1
        tmp[key]["total_size"] += size

    return [
        {
            period: key,
            "files": tmp[key]["files"],
            "total_size": byte_to_gi(tmp[key]["total_size"]),
        }
        for key in sorted(tmp)
    ]
