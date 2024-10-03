def get_patient_details(appointment_data):
    data = appointment_data.get("data", {})
    patient_profile = data.get('patient_profile', {})
    appointment_id = data.get('appointment_id')

    patient_details = {
        "externalOrderID": appointment_id,
        "pid": data.get('patient_id'),
        "dob": f"{patient_profile.get('dob')}T00:00:00Z" if patient_profile.get('dob') else None,
        "emailId": patient_profile.get('email_id'),
        "firstName": patient_profile.get('first_name'),
        "middleName": patient_profile.get('middle_name'),
        "age": patient_profile.get('age'),
        "lastName": patient_profile.get('last_name'),
        "genderName": patient_profile.get('gender'),  # TODO: map
        "contactNumber": patient_profile.get('mobile', '')[-10:],
        "salutationName": patient_profile.get('salutation')  # TODO: map
    }

    # Remove keys with None values
    patient_details = {k: v for k, v in patient_details.items() if v is not None}

    return patient_details, appointment_id

def get_visit_details(appointment_data, payment_data, appointment_id):
    data = appointment_data.get("data", {})
    amount = payment_data.get("amount", 0)

    visit_details = {
        "externalVid": appointment_id,
        "visitDate": data.get('visit_start'),
        "samplePickUpDateTime": data.get('visit_start'),
        "orgId": 361,
        "orgName": "Hitech-GKS TOWERS",
        "registeredVia": "HVT",
        "locationId": 4102,
        "locationIdName": "TIRUVOTTIYUR PSC",
        "clientCode": "CUS26358",
        "patientType": "Homevisit",
        "doctorID": "0035j000019najjAAA",
        "phleboID": 100612,
        "testDetails": {
            "test": [
                {
                    "baseMRP": amount,
                    "netAmount": amount,
                    "discountAmount": 0,
                    "testCode": "HV75",
                    "testType": "GBI"
                }
            ]
        },
        "paymentDetails": {
            "grossAmount": amount,
            "totalDiscountAmount": 0,
            "netAmount": amount,
            "amountReceived": amount,
            "billNumber": "",
            "billDate": "",
            "bankAccountNumber": "",
            "transactionDetails": [
                {
                    "paymentDate": payment_data.get("created_at"),
                    "amount": amount,
                    "transactionID": payment_data.get("rrn"),
                    "paymentGatewayName": payment_data.get("payment_gateway"),
                    "ezetapReferenceNumber": payment_data.get("transaction_id"),
                    "paymentTypeName": payment_data.get("payment_mode"),
                    "cardNo": "",
                    "chequeNo": "",
                    "chequeDate": "",
                    "chequeBank": "",
                    "MICRCode": "",
                    "cardHolderName": "",
                    "authCode": "",
                    "userName": "",
                    "userMobile": "",
                    "messageCode": "",
                    "message": ""
                }
            ]
        },
        "CreatedBy": "2403131744051"
    }

    if data.get('prescription_url'):
        visit_details["documentDetails"] = {
            "document": [
                {
                    "documentType": "TRF",
                    "documentLink": data.get('prescription_url'),
                    "documentExtension": ".pdf"
                }
            ]
        }

    return visit_details

def transform_appointment_data(appointment_data, payment_data):
    patient_details, appointment_id = get_patient_details(appointment_data)
    visit_details = get_visit_details(appointment_data, payment_data, appointment_id)

    patient_details["visitdetails"] = visit_details

    return {
        "patientDetails": patient_details,
        "totalrecords": 0,
        "offset": 0,
        "limit": 0,
        "action": "C",
    }