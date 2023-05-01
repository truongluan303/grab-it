from flask import abort
from flask import after_this_request
from flask import send_file

from . import routes
from src.tempfiles_manager import TempfilesManager


@routes.route("/download/<string:file_id>", methods=["GET"])
def download(file_id: str):
    tempfile_manager = TempfilesManager.get_instance()

    if not tempfile_manager.contains(file_id):
        abort(404)

    # Downloading a big file may take a long time, so we must make sure the
    # file is not automatically deleted.
    tempfile_manager.prevent_expiration_removal(file_id)

    @after_this_request
    def _(response):
        tempfile_manager.remove_file(file_id)
        return response

    filepath = tempfile_manager.get_file(file_id)
    return send_file(
        filepath,
        download_name=filepath.split("/")[-1],
    )
