#from requests import Request, Session

from twilio.http import HttpClient, get_cert_file
from twilio.http.response import Response
from twilio.rest import Client
import xml.etree.ElementTree as etree
from ApixuClient import ApixuClient
import json

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
    
def readCredentials(fileName):
    try:
        twillioSID = ""
        twillioToken = ""
        fromNumber = ""
        apixuKey = ""
        tree = etree.parse(fileName)
        root = tree.getroot()
        for n in root:
            if n.tag == "twlSID":
                twillioSID = n.attrib["value"]
            elif n.tag == "twlAuthToken":
                twillioToken = n.attrib["value"]
            elif n.tag == "fromNumber":
                fromNumber = n.attrib["value"]
            elif n.tag == "apixuKey":
                apixuKey = n.attrib["value"]
                return (twillioSID, twillioToken, fromNumber, apixuKey)
    except xml.etree.ElementTree.ParseError as e:
        #var/log/
        print("Failed to parse sms credentials file " + e)
        return ()

def readWeatherInfo(myKey):
    try:
        weatherClient = ApixuClient(myKey)
        weather = json.loads ( str(weatherClient.getCurrentWeather(q="L6A3Y1&temp_c&feelslike_c&precip_mm")).replace("\"", "'") )
        print(weather["current"]["temp_c"])
    except Exception as e:
        print("Failed to get weather forecast: " + e)


if __name__ == "__main__":
    params = readCredentials("config.xml")
    if len(params) >= 4: 
        readWeatherInfo(params[3])       
    	#client = Client(params[0], params[1])
    	#client.messages.create(to="+16474053246", from_=params[2], body="Spam Span Spam!")
