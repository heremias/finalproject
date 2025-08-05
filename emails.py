#!/usr/bin/env python3

import email.message
import mimetypes
import os.path
import smtplib

def generate_email(sender, recipient, subject, body, attachment_path=None):
    """Creates an email with an optional attachment."""
    message = email.message.EmailMessage()
    message["From"] = sender
    message["To"] = recipient
    message["Subject"] = subject
    message.set_content(body)

    if attachment_path:
        attachment_filename = os.path.basename(attachment_path)
        mime_type, _ = mimetypes.guess_type(attachment_path)
        mime_type, mime_subtype = mime_type.split('/', 1)

        with open(attachment_path, 'rb') as ap:
            message.add_attachment(ap.read(),
                                   maintype=mime_type,
                                   subtype=mime_subtype,
                                   filename=attachment_filename)
    return message

def send_email(message):
    """Sends the given message through an SMTP server."""
    # TODO: Update with your SMTP server details
    mail_server = smtplib.SMTP('localhost')
    # If your server requires authentication:
    # mail_server.login(user, password)
    try:
        mail_server.send_message(message)
    finally:
        mail_server.quit()
