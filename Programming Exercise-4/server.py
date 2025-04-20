# Server Side Application
from flask import Flask,jsonify,request
import rsa
import ntplib
import requests
from datetime import datetime, timezone
server_app=Flask(__name__)
(public_key,private_key)=rsa.newkeys(2048)
def get_timeapi_time():
    resp=""
    try:
        response=requests.get("https://timeapi.io/api/Time/current/zone?timeZone=UTC")
        if response.status_code==200:
            timeapi_time=response.json()
            # print(timeapi_time)
            return f"{timeapi_time['dateTime']}"
    except Exception as e:
        print("Can't fetch timeapi.io time")
        resp=e
    return resp
# get_timeapi_time()
def get_ntp_time():
    resp=""
    try:
        ntp_time=datetime.fromtimestamp(ntplib.NTPClient().request('time.nist.gov').tx_time,tz=timezone.utc)
        # print(ntp_time)
        return ntp_time
    except Exception as e:
        print("Can't fetch NTP time")
        resp=e
    return resp
# get_ntp_time()

@server_app.route("/timestamp",methods=["POST"])
def timestamp():
    data=request.get_json()
    pdf_hash=data.get("hash")
    if pdf_hash is None:
        return jsonify({"error":"Hash not received by Server"})
    timeapi_time=get_timeapi_time()
    ntp_time=get_ntp_time()
    combined_time=f"|| timeapi:{timeapi_time} || ntp:{ntp_time} ||"
    to_sign=f"{pdf_hash}|{combined_time}".encode('utf-8')
    signature=rsa.sign(to_sign,private_key, 'SHA-256')
    response={"timestamp":combined_time,"signature":signature.hex(),"public_key":public_key.save_pkcs1().decode('utf-8')}
    return jsonify(response)
server_app.run(ssl_context=('cert.pem','key.pem'))
