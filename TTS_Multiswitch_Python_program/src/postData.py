import requests
from base64 import b64encode


def sendData(payload, fPort, confirmedDownlink, priority, schedule, APIKey, applicationName, endDeviceName):

    if payload == "":                                                               # Check if the payload contains an empty string
        print("Nothing to send!")
        exit(0)                                                                     # If the string is empty, then exit the script
    else:
        print("Sending payload:", payload)


    # CayenneLPP hex -> base64
    payloadBase64 = b64encode(bytes.fromhex(payload)).decode()                      # Encoding the payload in base64 format


    # POST request
        # Construct the URL to which the POST request will be sent. The URL is composed of a string with the TTN server address, the application ID, the end device ID and the "push" or "replace" string.
    url = 'https://eu1.cloud.thethings.network/api/v3/as/applications/' + applicationName + '/devices/' + endDeviceName + '/down/'+ schedule
    
        # The header consists of authorization (using an API key), content type and user agent.
    header = {'Authorization': 'Bearer ' + APIKey, 
            'Content-Type': 'application/json',
            'User-Agent': 'my-integration/my-integration-version'
            }

        # Data that contains the encoded payload in base64, the fport number, information on whether we want to confirm the reception of the downlink and the priority with which the downlink should be sent
    data = {"downlinks":[{
        "frm_payload": payloadBase64,
        "f_port": fPort,
        "confirmed": confirmedDownlink,
        "priority": priority
        }]}

        # Send a POST request using the request.post() method and store the response in the response variable.
    response = requests.post(url, headers=header, json=data)

        # The result of the method that sent the POST request is a status code. For example, a 200 success status response code indicates that the request was successful.
    print("Status code", response.status_code)
    return  response.status_code
