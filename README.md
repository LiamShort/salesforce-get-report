# salesforce-get-report

This repo contains materials and resources that can be used to retrieve payment reports from Salesforce, returned in JSON formatting.

## Repo Contents

* `salesforce-report-tool`: Python script to retrieve a given report from
* `salesforce-creds`: Define Salesforce Credentials assumed by `salesforce-report-tool` to access Salesforce API
* `requirements.txt`: Pip requirements required by tool

## Pre-Requisites

### Language
Python 3.7.4.

### Packages
The packages listed below can be installed via the `requirements.txt` file.

* salesforce-reporting

## Using the Tool

### Salesforce Credentials File

The user must first insert the following Salesforce credentials within the `salesforce-creds.yaml` file to allow this application to query the Salesforce APIs:
* `username`: The email address used to login to Salesforce.
* `password`: The password used to login to Salesforce.
* `access_token`: To get a Access Token check out the following [Guide](https://onlinehelp.coveo.com/en/ces/7.0/administrator/getting_the_security_token_for_your_salesforce_account.htm).

This file should be included in the same directory as the `salesforce-report-tool.py` application.

### Getting the Report ID

An 18 character Report ID is required when running the application, this identifies which report will be ran. This value can be extracted from the URL when running the report from the browser, for example, a URL like the following will be displayed when running a report in the browser:

* **https://COMPANY.lightning.force.com/lightning/r/Report/`00O0J000007yNidUAE`/view**

The Report ID is the 18 character string highlighted above.

### Launching the Application

The application can be launched by running:
* `python3 salesforce-report-tool.py`

### Using the Application

After the application has been launched, the user will be presented with a GUI, displaying a text box and button. The Report ID should be inserted into the text box, then the button can be clicked to run the report.

**NOTE** After the button has been pressed, it may take some time for the report to run in Salesforce and the data returned - please be patient.

## Further Work

* Convert the Reports from JSON to XML - XML formatting is specific to Report Type.