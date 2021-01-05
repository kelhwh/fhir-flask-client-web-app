# FHIR Patient Portal
This is a FHIR client web app built with Flask, a flexible web app connecting to
[FHIR](http://www.hl7.org/implement/standards/fhir/) servers. The app verifies registration with Patient resources on the FHIR server and renders patient information fetched from the server.

By default, the app connects to the [(HAPI FHIR Reference server (STU3)](http://hapi.fhir.org/baseDstu3/). You may change the server it connects to, but the prefilled registration will fail because the registration must match a patient resource to pass the verification.

## Initiation
```
python app.py
```
Go to http://127.0.0.1:5000/ and register a user with prefilled values and then login.
