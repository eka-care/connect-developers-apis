from django.http import JsonResponse, HttpResponse, HttpResponseNotAllowed
from django.views.decorators.csrf import csrf_exempt
import logging
import json
import http

from .rni import send_data
from .appointments import fetch_appointment_data
from .transform import transform_appointment_data
from .payment_details import fetch_payment_details

log = logging.getLogger(__name__)


def get_json_body(request):
    try:
        return json.loads(request.body)
    except json.JSONDecodeError:
        log.error("Could not parse request body")
        return None

def validate_event(data):
    if data.get("scope") != "appointment":
        return False, "Uninterested event", http.HTTPStatus.OK
    if not data.get("data", {}).get("appointment_id"):
        return False, "appointment_id not found", http.HTTPStatus.BAD_REQUEST
    return True, None, None

def fetch_and_validate_appointment(appointment_id):
    try:
        appointment_data = fetch_appointment_data(appointment_id)
        receipts = appointment_data.get("data", {}).get("receipts", [])
        payment_id = None
        for receipt in receipts:
            if receipt.get("payment_id"):
                payment_id = receipt.get("payment_id")
                break
        if not payment_id:
            return None, None, "Appointment with no payment info!", http.HTTPStatus.OK
        return appointment_data, payment_id,  None, None
    except Exception as e:
        log.error(f"Error fetching appointment data: {e}")
        return None, str(e), http.HTTPStatus.INTERNAL_SERVER_ERROR

def fetch_and_validate_payment(payment_id):
    try:
        payment_data = fetch_payment_details(payment_id)
        if payment_data.get("payment_status") != "PAYMENT_SUCCESS":
            return None, "Appointment with payment not success!", http.HTTPStatus.OK
        return payment_data, None, None
    except Exception as e:
        log.error(f"Error fetching payment data: {e}")
        return None, str(e), http.HTTPStatus.INTERNAL_SERVER_ERROR

@csrf_exempt
def receive_event(request):
    if request.method != http.HTTPMethod.POST:
        return HttpResponseNotAllowed([http.HTTPMethod.POST])

    data = get_json_body(request)
    if not data:
        return JsonResponse({"error": "Invalid JSON body"}, status=http.HTTPStatus.BAD_REQUEST)

    is_valid, error_message, status_code = validate_event(data)
    if not is_valid:
        log.error(f"Invalid event data. error: {error_message}, data: {data}")
        return JsonResponse({"error": error_message}, status=status_code)

    appointment_id = data["data"]["appointment_id"]
    appointment_data, payment_id, error_message, status_code = fetch_and_validate_appointment(appointment_id)
    if not appointment_data:
        log.error(f"Invalid appointment data. error: {error_message}, appointment_id: {appointment_id}")
        return JsonResponse({"error": error_message}, status=status_code)

    payment_data, error_message, status_code = fetch_and_validate_payment(payment_id)
    if not payment_data:
        log.error(f"Invalid payment data. error: {error_message}, payment_id: {payment_id}")
        return JsonResponse({"error": error_message}, status=status_code)

    try:
        transformed_data = transform_appointment_data(appointment_data, payment_data)
        send_data(transformed_data)
    except Exception as e:
        log.error(f"Could not send data to metropolis: {e}, appointment_data: {transformed_data}")
        return JsonResponse(
            {"error": "Failed to send data to Metropolis API", "details": str(e)},
            status=http.HTTPStatus.INTERNAL_SERVER_ERROR)

    log.info(f"Successfully sent data to metropolis! appointment_id: {appointment_id}")
    return HttpResponse("Successfully sent data to metropolis!")