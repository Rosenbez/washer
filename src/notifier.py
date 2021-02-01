import yagmail


class EmailNotifier():

    def __init__(self, notify_email):
        self._yag = yagmail.SMTP(
            "my.washer.project@gmail.com", oauth2_file="oauth2_creds_yag.json"
        )
        self._notify_email = notify_email
        self._notify_message = "Your laundry is finished!"

    def laundry_finished(self):
        self._yag.send(
            to=self._notify_email, contents=self._notify_message
        )

