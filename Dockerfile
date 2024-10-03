FROM vishal24tuniki/data-slinger-web:v0.0.9

COPY views_connect.py webapp/views_connect.py
COPY appointments.py webapp/appointments.py
COPY auth.py webapp/auth.py
COPY constants.py webapp/constants.py
COPY payment_details.py webapp/payment_details.py
COPY rni.py webapp/rni.py
COPY transform.py webapp/transform.py
