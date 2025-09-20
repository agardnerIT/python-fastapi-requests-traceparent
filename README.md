# python-fastapi-requests-traceparent


```
python -m venv .
source bin/activate
pip install -r requirements.txt

########################
# Terminal 1: app1
python app1.py

########################
# Terminal 2: app2
python app2.py

########################
# Terminal 3: Jaeger
# Start Jaeger all-in-one
# Using docker instructions here
# https://www.jaegertracing.io/docs/2.10/getting-started/#all-in-one

########################
# Send a request to app1
curl http://localhost:8080
```
