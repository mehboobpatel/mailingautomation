# Azure-Sendgrid-with-Python-and-AZ-Functions
How to run automated mailing in Azure - few end to end examples using Azure Functions, Python and Sendgrid. 
  
---
  
### SCENARIOS
All of the AZ functions in this repo are based on the same real project requirement I've worked with: using on some kind of trigger generate email with (or without) specified attachment coming from blob storage. All of them are using combination of Python and Sendgrid and are a complete working samples that can be used for your reference.

  
**SCENARIO 1: Simple Blob Trigger**  
Whenever a new blob appears in the storage send an email using a blob as attachment. Email details defined directly in the function content, without additional configuration. As simple as it can be.

**SCENARIO 2: Blob Trigger with Additional Configuration**  
This scenario has the same trigger and functionality as <simple-blob-trigger> however it itroduce additional configuration options.  
Let's say that you have 3 different alerts to run, for 3 different data providers - each with separate folder in blob storage. For each one of them you want to have different email (receipent, subject, content etc.). This function is an example of how we can store email details in json config file and load it based on the blob folder path.  

**SCENARIO 3: Http trigger**  
Email details are defined in the http request - this includes information if there is an attachment and if yes then what is the path. Most versatile approach where function can ex. chained with another function or called from ADF as part of the existing pipeline.   
with request in following format:  
```python
json_request = {
    'with_attachment': 'yes',
    'blob_name' : 'attachment_name.csv',
    'container_name' : 'samplecontainer',
    'sender_address' : "sender.adress@goeshere.com",
    'receipent_address' : 'receipent.adress@goeshere.com',
    'email_subject' : 'your subject',
    'email_content' : 'your content'}
```  
  
---
  
#### PREREQUISITES & LINKS
- SendGrid account for SendGrid API key and authenticated sender email account: [link - setup Azure Sengrid](https://docs.sendgrid.com/for-developers/partners/microsoft-azure-2021) 
- Connection Strings, secrets and config parameters in AZ Functions are [managed in Application settings](https://docs.microsoft.com/en-us/azure/azure-functions/functions-reference-python?tabs=asgi%2Cazurecli-linux%2Capplication-level#environment-variables) for Azure deployment or from `local.settings.json` for local development
