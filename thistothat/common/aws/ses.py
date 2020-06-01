
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
import os

from thistothat.common.aws import get_boto_client


def send_email(sender: str, recipients: list, subject: str, text: str=None, html: str=None, attachments: list=None):

    message = _create_multipart_message(sender, recipients, subject, text, html, attachments)
    
    ses_client = get_boto_client('ses')
    return ses_client.send_raw_email(
        Source=sender,
        Destinations=recipients,
        RawMessage={'Data': message.as_string()}
    )

def _create_multipart_message(sender: str, recipients: list, title: str, text: str=None, html: str=None, attachments: list=None):

    multipart_content_subtype = 'alternative' if text and html else 'mixed'
    msg = MIMEMultipart(multipart_content_subtype)
    msg['Subject'] = title
    msg['From'] = sender
    msg['To'] = ', '.join(recipients)

    if text:
        part = MIMEText(text, 'plain')
        msg.attach(part)
    if html:
        part = MIMEText(html, 'html')
        msg.attach(part)

    for attachment in attachments or []:
        with open(attachment, 'rb') as f:
            part = MIMEApplication(f.read())
            part.add_header('Content-Disposition', 'attachment', filename=os.path.basename(attachment))
            msg.attach(part)

    return msg