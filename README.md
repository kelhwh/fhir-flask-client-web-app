# FHIR Patient Portal
This is a FHIR client web app built with Flask, a plug-and-play web app set to connect to [Epic on FHIR](https://fhir.epic.com/) testing environment and [SMART App Launcher](https://launch.smarthealthit.org/)
open endpoint to render appointment history and perform data exchange. Demo can be seen here https://fhir-patient-portal.herokuapp.com/.

Login credentials for EPIC on FHIR are provided in the page before initiating the OAuth. Credentials for SMART App Launcher are prefilled.

If you want to deploy the app locally, you'll have to register an account in EPIC on FHIR and get your own app id.

## Initiation
```
python app.py
```
Go to http://127.0.0.1:5000/ and register a user with prefilled values and then login.
