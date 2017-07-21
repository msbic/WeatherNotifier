from requests import Request, Session

from twilio.http import HttpClient, get_cert_file
from twilio.http.response import Response
from twilio.rest import Client

class ProxiedTwilioHttpClient(HttpClient):
    """
    General purpose HTTP Client for interacting with the Twilio API
    """
    def request(self, method, url, params=None, data=None, headers=None, auth=None, timeout=None,
                allow_redirects=False):

        session = Session()
        session.verify = get_cert_file()
        session.proxies = {
                              "https" : "http://10.94.134.70:8080"
                          }

        request = Request(method.upper(), url, params=params, data=data, headers=headers, auth=auth)

        prepped_request = session.prepare_request(request)
        response = session.send(
            prepped_request,
            allow_redirects=allow_redirects,
            timeout=timeout,
        )

        return Response(int(response.status_code), response.content.decode('utf-8'))



if __name__ == "__main__":
	accountSID = ""
	autToken = ""
	client = Client("", "", http_client=ProxiedTwilioHttpClient())
	client.messages.create(to="", from_="", body="Spam Span Spam!")