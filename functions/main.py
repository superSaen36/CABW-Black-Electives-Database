from firebase_functions import https_fn
from firebase_functions.options import set_global_options
from firebase_admin import initialize_app

# Import your Flask app
from app import app

# For cost control, you can set the maximum number of containers that can be
# running at the same time. This helps mitigate the impact of unexpected
# traffic spikes by instead downgrading performance. This limit is a per-function
# limit. You can override the limit for each function using the max_instances
# parameter in the decorator, e.g. @https_fn.on_request(max_instances=5).
set_global_options(max_instances=10)

initialize_app()

@https_fn.on_request()
def app_function(req: https_fn.Request) -> https_fn.Response:
    """HTTP Cloud Function that serves the Flask app"""
    with app.request_context(req.environ):
        return app.full_dispatch_request()