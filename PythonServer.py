import flask
from flask import Flask, request

from src.DummyAPI import DummyAPI

app = Flask(__name__)
app.logger.setLevel('INFO')

DUMMY_HANDLER = DummyAPI()


@app.route('/bookings/bookings', methods=['GET', 'POST'])
def dummy_api():
    if request.method == 'GET':
        resp_val = DUMMY_HANDLER.handle_get()
    else:
        resp_val = DUMMY_HANDLER.handle_post(request)

    response = flask.Response(resp_val)
    response.headers["Content-Type"] = "application/json"

    return response

# @app.route('/services/<path:path>', methods=['POST'])
# def ns_support_services(path):
#     try:
#         if path == "oauth1" or path == "oauth1/":
#             return OAuth1(app, request).process()
#         elif path == "mail" or path == "mail/":
#             return MailSender(app, request).send()
#         else:
#             raise Exception("Invalid service request : %s" % path)
#     except Exception:
#         ex_type, ex_value, ex_traceback = sys.exc_info()
#
#         app.logger.error("%s %s" % (ex_type.__name__, ex_value))
#
#         # Print the stack trace to stderr
#         traceback.print_tb(ex_traceback)
#
#         return "Something went wrong : %s" % ex_value
