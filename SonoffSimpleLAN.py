import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
import collections
import sonoffcrypto
import json
import traceback
from zeroconf import ServiceBrowser, ServiceListener, Zeroconf
import time

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
        total=8,
        backoff_factor=0.8,
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

    sonoffcrypto.format_encryption_msg(payload, api_key, params)

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

        if outlet == None:
            #no outlet so we not strip device
            response = send(http_session, get_update_payload(api_key, device_id, {"switch": on_request, "outlet": int(0)}), 'http://' + ip_address + ":8081/zeroconf/switch")
        else:
            params = {"switches": [{"switch": "x", "outlet": 0}]}
            params["switches"][0]["switch"] = on_request
            params["switches"][0]["outlet"] = int(outlet)
            response = send(http_session, get_update_payload(api_key, device_id, params), 'http://' + ip_address + ":8081/zeroconf/switches")
        
        response_json = json.loads(response.content.decode("utf-8"))

        if response_json["error"] != 0:
            strReturn = '%s Error returned by device'%response_json["error"]

        return strReturn

    except:
        return 'change_switch error setting device %s to state %s : %s'%(device_id, on_request, traceback.format_exc())


def BeginMonitoringSonoffDevices(callbackfunc, dictDevices):
    #import logging
    #logging.getLogger('zeroconf').setLevel(logging.DEBUG)
    while True:
        zeroconf = Zeroconf()
        listener = sonoffListener(callbackfunc, dictDevices)
        browser = ServiceBrowser(zeroconf, "_ewelink._tcp.local.", listener)
        time.sleep(60 * 30)
        browser.cancel()
        zeroconf.browsers.clear()
        zeroconf.close()
        
        
        

class sonoffListener(ServiceListener):
    import sonoffcrypto
    callbackfunc = None
    dictDevices = None
    
    def __init__(self, callbackfunc, dictDevices) -> None:
        super().__init__()
        self.callbackfunc = callbackfunc
        self.dictDevices = dictDevices

    def actionSonoffEvent(self, zc: Zeroconf, type_: str, name: str) -> None:
        info = zc.get_service_info(type_, name)
        device = info.properties[b"id"].decode("ascii")
        data = info.properties.get(b"data1")
        if info.properties.get(b"data2") is not None:
            data += info.properties.get(b"data2")
        if info.properties.get(b"data3") is not None:
            data += info.properties.get(b"data3")
        if info.properties.get(b"data4") is not None:
            data += info.properties.get(b"data4")
                                    
        iv = info.properties.get(b"iv")
        api_key = self.dictDevices[device][0]

        data = self.sonoffcrypto.decrypt(data, iv, api_key)
        data = json.loads(data.decode("ascii"))
        
        self.callbackfunc(device, data)
        
    def update_service(self, zc: Zeroconf, type_: str, name: str) -> None:
        self.actionSonoffEvent(zc, type_, name)

    def add_service(self, zc: Zeroconf, type_: str, name: str) -> None:
        self.actionSonoffEvent(zc, type_, name)

    def remove_service(self, zc: Zeroconf, type_: str, name: str) -> None:
        self.actionSonoffEvent(zc, type_, name)

'''
ip_address = '192.168.1.107'
api_key = '8cc35b2c-d8c9-4eae-817a-68096a3e3e70'
device_id = '100073bdf7' #not really required
outlet=None #or integer if is strip socket
err = change_switch(api_key, device_id, ip_address, outlet, str("ON").lower())


to monitor just call:
import sonoffsimpleLAN
dictNewSonoff = {}
dictNewSonoff[devID] = (apikey, deviceIPAddress, outlet)

try:
    sonoffsimpleLAN.BeginMonitoringSonoffDevices(SonoffCallback, dictNewSonoff)
except:
    pass
    
where SonoffCallback:

def SonoffCallback(device, data):
    try:
        print(device)
        print(data)
        if 'switches' in data:
            
            for sw in data['switches']:
                devstatus = 'ON' if sw['switch'] == 'on' else 'OFF'  
                #sw['outlet'] gives the outlet
                #do some stuff
                            
        else:
            devstatus = 'ON' if data['switch'] == 'on' else 'OFF'        
            strRSSI = 'rssi:%s'%data['rssi']
            #do some stuff

    except:
        pass #handle error

'''
