from django.http import HttpResponse
import json
import requests

# from .auth import Auth


def receive_event(request):
    if request.method != "POST":
        return HttpResponse("Hello, world2!")

    data = json.loads(request.body)
    event_type = data.get("event_type")
    if event_type != "appointment":
        return HttpResponse("Hello, world2!")
    
    appointment_id = data.get("data", {}).get("appointment_id")
    if appointment_id is None:
        return HttpResponse("Hello, world2!")
    
    #access_token = Auth().login()
    access_token = ""

    url = "https://api.eka.care/dr/v1/business/appointments/{}".format(appointment_id)
    headers = {"auth": access_token}
    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        return HttpResponse("Failed appointment API!")
    
    appointment_data = response.json()
    url2 = "https://apirni.metropolisindia.com/rest/prshvtexternalapi/v1/HVT"
    data = {}
    response2 = requests.post(url2, json=data)
    if response2.status_code != 200:
        return HttpResponse("Failed Metropolis API!")

    return HttpResponse("Hello, world2!")
