import json


class DummyAPI:

    def __init__(self):
        self.CACHE = []
        self.id = 0

    def handle_post(self, flask_request):
        json_data = json.loads(flask_request.data)

        json_data["ref-id"] = self.id
        self.id += 1

        self.CACHE.append(json_data)

        # bad_resp = json.dumps({
        #     "status": "fail",
        #     "error-code": "Payment gateway is not responding"
        # })

        return json.dumps({
            "status": "ok",
            "ref-id": json_data["ref-id"]
        })

    # return bad_resp;

    def handle_get(self):
        response = {"bookings": []}

        for item in self.CACHE:
            response["bookings"].append(item)

        return json.dumps(response)
