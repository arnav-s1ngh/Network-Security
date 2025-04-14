import rsa
from flask import Flask, request, jsonify
import ntplib
import requests
from datetime import datetime, timezone

app=Flask(__name__)
(public_key,private_key)=rsa.newkeys(2048)

def get_timeapi_time():
    try:
        response=requests.get("https://timeapi.io/api/Time/current/zone?timeZone=UTC")
        if response.status_code==200:
            data = response.json()
            return f"{data['date']} {data['time']}"
    except Exception as e:
        print("Error fetching timeapi.io time:", e)
    return "Unavailable"

def get_ntp_time():
    try:
        client= ntplib.NTPClient()
        response=client.request('time.nist.gov')
        ntp_time=datetime.fromtimestamp(response.tx_time, tz=timezone.utc)
        return ntp_time
    except Exception as e:
        print("Error fetching NTP time:", e)
    return "Unavailable"

@app.route("/timestamp", methods=["POST"])
def timestamp():
    data=request.get_json()
    doc_hash=data.get("hash")
    if not doc_hash:
        return jsonify({"error": "Missing 'hash' in request"}),400

    timeapi_time=get_timeapi_time()
    ntp_time=get_ntp_time()
    combined_time=f"timeapi: {timeapi_time}|ntp: {ntp_time}"

    to_sign=f"{doc_hash}|{combined_time}".encode('utf-8')
    signature=rsa.sign(to_sign, private_key, 'SHA-256')
    response = {"timestamp": combined_time,"signature": signature.hex(),"public_key": public_key.save_pkcs1().decode('utf-8')}
    return jsonify(response)

app.run()
