import json
import smtplib
import time
from email.message import EmailMessage

_FROM_FIELD = "From"
_TO_FIELD = "To"
_MESSAGE_FIELD = "Message"

_SMTP_SERVER_FIELD = "Server"
_SMTP_USER_FIELD = "Username"
_SMTP_PASSWORD_FIELD = "Password"


class MailSender:
    def __init__(self, app, flask_request):
        self.app = app
        self.request = flask_request

    def send(self):
        if self.request.is_json:
            payload = json.loads(self.request.data)
            self.verify_fields(payload)

            return self.send_mail(payload)
        else:
            raise Exception("Payload must be JSON")

    def send_mail(self, payload):
        email = EmailMessage()

        email['Subject'] = "NetSuite Project Code Push Report <%s>" % time.strftime("%d-%m-%Y", time.gmtime())
        email['To'] = payload[_TO_FIELD]
        email['From'] = payload[_FROM_FIELD]
        email.set_content(payload[_MESSAGE_FIELD])

        self.app.logger.info("%s %s" % (payload[_SMTP_USER_FIELD], payload[_SMTP_PASSWORD_FIELD]))

        # Get Mail server related configurations and authenticate
        mail_server = smtplib.SMTP(payload[_SMTP_SERVER_FIELD], 25)
        mail_server.login(payload[_SMTP_USER_FIELD], payload[_SMTP_PASSWORD_FIELD])

        mail_server.send_message(email)
        mail_server.quit()

        self.app.logger.info("Email sent. From : %s To : %s" % (payload["From"], payload["To"]))

        return "Email sent"

    @staticmethod
    def verify_fields(payload):
        if _FROM_FIELD not in payload:
            raise Exception("Sender email not provided")

        if _TO_FIELD not in payload:
            raise Exception("Receiver email not provided")

        if _MESSAGE_FIELD not in payload:
            raise Exception("Message not provided")

        if _SMTP_SERVER_FIELD not in payload:
            raise Exception("SMTP Server is not provided")

        if _SMTP_USER_FIELD not in payload:
            raise Exception("SMTP Server's authentication user missing")

        if _SMTP_PASSWORD_FIELD not in payload:
            raise Exception("SMTP Server's authentication password missing")
