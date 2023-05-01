from . import routes


@routes.route("/", methods=["GET"])
def index():
    return "Hello from GrabIt"
