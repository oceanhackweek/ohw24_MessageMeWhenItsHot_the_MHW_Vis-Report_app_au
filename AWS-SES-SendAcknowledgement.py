# %% import packages

import boto3
from botocore.exceptions import ClientError
import pickle as pkl

# %% Load email list

# file = 'pickle_file_containing_a_list_of_emails.pkl'

# with open(file, 'rb') as f:
#     email_list = pkl.load(f)

# temporary variable for testing
email_list = ["mphemming@live.co.uk"]
# email_list = stored_email


def create_email_content(location):
    subject = "MMWIH: Congratulations, you are on the hotlist"
    body = (
        f"Hello,\n\n"
        f"You want us to message you when it is hot at " + location + ".\n\n"
        f"This is a notification that your email has been added to our records, and you will receive an email when it is hot.\n\n"
        f"The MMWIH team\n\n"
    )
    return subject, body


location = "Maria Island"

subject, body = create_email_content(location)


def send_email():
    # Create an SES client
    ses_client = boto3.client(
        "ses", region_name="ap-southeast-2"
    )  # Change the region if needed

    # Email settings
    SENDER = "messagemewhenitshot@gmail.com"
    RECIPIENT = "mphemming@live.co.uk"
    SUBJECT = subject
    BODY_TEXT = body
    CHARSET = "UTF-8"

    # Try to send the email.
    try:
        response = ses_client.send_email(
            Destination={
                "ToAddresses": [
                    RECIPIENT,
                ],
            },
            Message={
                "Body": {
                    "Text": {
                        "Charset": CHARSET,
                        "Data": BODY_TEXT,
                    },
                },
                "Subject": {
                    "Charset": CHARSET,
                    "Data": SUBJECT,
                },
            },
            Source=SENDER,
        )
    except ClientError as e:
        print(e.response["Error"]["Message"])
    else:
        print("Email sent! Message ID:"),
        print(response["MessageId"])


# Call the function to send an email
send_email()
