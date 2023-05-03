from typing import Dict
from typing import Tuple

import requests
from flask import jsonify
from flask import request
from flask import Response

import src.downloader as downloader
from . import routes
from src.tempfiles_manager import TempfilesManager


_YOUTUBE_URL_PARAM = "url"


@routes.route("/youtube", methods=["GET"])
def youtube() -> Response:
    params = request.args
    param_validation_result = _validate_param(**params)

    if not all(param_result[0] for param_result in param_validation_result.values()):
        return (
            jsonify(
                {
                    "success": False,
                    "errors": [
                        valres[1] for valres in param_validation_result.values()
                    ],
                }
            ),
            400,
        )

    download_result = downloader.download_youtube(params.get(_YOUTUBE_URL_PARAM))
    if not download_result:
        return (
            jsonify(
                {"success": False, "errors": ["Server Error: Unable to download video"]}
            ),
            505,
        )

    tmpfiles_manager = TempfilesManager.get_instance()
    tmpfiles_manager.add_file(download_result.file_id, download_result.file_path)

    return jsonify(
        {
            "download_file_id": download_result.file_id,
            **download_result.video_data.to_dict(),
        }
    )


def _validate_param(**params) -> Dict[str, Tuple[bool, str]]:
    result = {param: (True, "") for param in params}

    if _YOUTUBE_URL_PARAM not in params:
        result[_YOUTUBE_URL_PARAM] = (False, f"Missing {_YOUTUBE_URL_PARAM} param")

    for param, value in params.items():
        if param == _YOUTUBE_URL_PARAM and not _validate_youtube_url(value):
            result[_YOUTUBE_URL_PARAM] = (False, "Invalid Youtube video URL")

    return result


def _validate_youtube_url(url):
    return requests.get(f"https://www.youtube.com/oembed?url={url}").status_code == 200
