import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
import collections
import pysonofflanr3
import json
import traceback


def create_http_session():

    # create an http session so we can use http keep-alives
    http_session = requests.Session()

    # add the http headers
    # note the commented out ones are copies from the sniffed ones
    headers = collections.OrderedDict(
        {
            "Content-Type": "application/json;charset=UTF-8",
            # "Connection": "keep-alive",
            "Accept": "application/json",
            "Accept-Language": "en-gb",
            # "Content-Length": "0",
            # "Accept-Encoding": "gzip, deflate",
            # "Cache-Control": "no-store",
        }
    )

    # needed to keep headers in same order
    http_session.headers = headers

    return http_session

def set_retries(http_session):

    # no retries at moment, control in sonoffdevice
    retries = Retry(
        total=5,
        backoff_factor=0.5,
        method_whitelist=["POST"],
        status_forcelist=None,
    )

    http_session.mount("http://", HTTPAdapter(max_retries=retries))

    return http_session

def get_update_payload(api_key, device_id: str, params: dict):
    import time

    payload = {
        "sequence": str(
            int(time.time() * 1000)
        ),  # otherwise buffer overflow type issue caused in the device
        "deviceid": device_id,
    }

    pysonofflanr3.sonoffcrypto.format_encryption_msg(payload, api_key, params)

    return payload

def send(http_session, request, thefullurl):

    data = json.dumps(request, separators=(",", ":"))
    response = http_session.post(thefullurl, data=data)

    return response

def change_switch(api_key, device_id, ip_address, outlet, on_request):
    strReturn = 'OK'
    try:

        http_session = create_http_session()
        http_session = set_retries(http_session)
        response = send(http_session, get_update_payload(api_key, device_id, {"switch": on_request, "outlet": int(outlet)}), 'http://' + ip_address + ":8081/zeroconf/switch")
        
        response_json = json.loads(response.content.decode("utf-8"))

        if response_json["error"] != 0:
            strReturn = '%s Error returned by device'%response_json["error"]

        return strReturn

    except:
        return traceback.format_exc()


'''
ip_address = '192.168.x.x'
api_key = 'xxxxxx'
device_id = '' #not really required so you don't need to supply it
outlet=0 #for things like multi channel wall switches
err = change_switch(api_key, device_id, ip_address, outlet, str("ON").lower())
'''
