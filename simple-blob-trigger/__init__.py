import os
import logging
import base64

import azure.functions as func
from azure.storage.blob import BlobServiceClient, BlobClient
from io import BytesIO

import sendgrid
from sendgrid.helpers.mail import Mail, Email, To, Content, Attachment, FileContent, FileName, FileType, Disposition, ContentId



def main(myblob: func.InputStream):
    logging.info(f"trigger for new blob: {myblob.name} - starting mailing app")

    connection_string = os.environ["STORAGE_CONNECTION_STRING"]
    sendgrid_api_key = os.environ["SENDGRID_API_KEY"]

    # create email object with defined parameters
    sender_email = os.environ["SENDER_EMAIL"]
    receipent_email = os.environ["RECEIPENT_EMAIL"]
    email_subject = "Your email subject goes here"
    email_content = "And email content goes here"

    mail = Mail(
        from_email=Email(sender_email),
        to_emails=To(receipent_email),
        subject=email_subject,
        plain_text_content=email_content)

    # load blob as stream and create attachment object
    try:
        container_name, blob_name = myblob.name.split('/')

        blob_service_client = BlobServiceClient.from_connection_string(connection_string)
        blob_client = blob_service_client.get_blob_client(container_name, blob_name)
        stream_object_from_blob = blob_client.download_blob()
        stream = BytesIO()
        stream_object_from_blob.download_to_stream(stream)

        encoded = base64.b64encode(stream.getvalue()).decode()
        attachment = Attachment()
        attachment.file_content = FileContent(encoded)
        attachment.file_name = FileName(blob_name)
        attachment.disposition = Disposition('attachment')
        attachment.content_id = ContentId('Example Content ID')
        mail.attachment = attachment

        logging.info('attachment object created')
    
    except Exception as e:
        logging.error(f'failed to create attachment: check file type and storage connection. message: {str(e)}')

    # send email
    try:
        sg = sendgrid.SendGridAPIClient(api_key=sendgrid_api_key)
        response = sg.client.mail.send.post(request_body=mail.get())

    except Exception as e:
        logging.error(f'failed to call sendgrid api - response: {response.status_code} - message: {str(e)}')
