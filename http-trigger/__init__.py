import logging
import os
import azure.functions as func

import base64
import sendgrid
from sendgrid.helpers.mail import Mail, Email, To, Content, Attachment, FileContent, FileName, FileType, Disposition, ContentId

from io import BytesIO
from azure.storage.blob import BlobServiceClient


def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Mailing Function received new request')

    connection_string = os.environ["STORAGE_CONNECTION_STRING"]
    sendgrid_api_key = os.environ["SENDGRID_API_KEY"]

    # define email details from received request
    try:
        email_det = req.get_json()
        sender_email = email_det['sender_address']
        receipent_email = email_det['receipent_address']
        email_subject = email_det['email_subject']
        email_content = email_det['email_content']
        attachment_present = email_det['with_attachment']

    except:
        logging.error('unable to read request parameters')

    # create email object  
    mail = Mail(
        from_email=Email(sender_email),
        to_emails=To(receipent_email),
        subject=email_subject,
        plain_text_content=email_content)

    # if indicated in request - create attachment obect from streamed blob
    if attachment_present == 'yes':
        try:
            attachment_blob_name = email_det['blob_name']
            attachment_container = email_det['container_name']

            blob_service_client = BlobServiceClient.from_connection_string(connection_string)
            blob_client = blob_service_client.get_blob_client(attachment_container, attachment_blob_name)
            stream_object_from_blob = blob_client.download_blob()
            stream = BytesIO()
            stream_object_from_blob.download_to_stream(stream)

            encoded = base64.b64encode(stream.getvalue()).decode()
            attachment = Attachment()
            attachment.file_content = FileContent(encoded)
            attachment.file_name = FileName(attachment_blob_name)
            attachment.disposition = Disposition('attachment')
            attachment.content_id = ContentId('Example Content ID')
            mail.attachment = attachment

        except Exception as e:
            logging.error(f'failed to create attachment. error message: {str(e)}')

    # send email
    try:
        sg = sendgrid.SendGridAPIClient(api_key=sendgrid_api_key)
        response = sg.client.mail.send.post(request_body=mail.get())
        
        return func.HttpResponse(f"mail to {receipent_email} sent successfully.")

    except Exception as e:
        logging.error(f'failed to call sendgrid api - response: {response.status_code} - message: {str(e)}')

    