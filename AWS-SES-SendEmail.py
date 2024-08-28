import boto3
from botocore.exceptions import ClientError


def create_email_content(new_data_available, record_broken, temperature_value, summary, location, depth):
    subject = "New Data Update and Record Broken!"
    body = (
        f"Hello,\n\n"
        f"You told us to message you when it is hot. And it is!\n"
        f"We added new data to our website and it tells us a new record has been broken for {location} at {depth}m!\n"
        f"Temperature Record: {temperature_value}°C\n\n"
        f"Please read the summary below: {summary}. (In the future, we can add some images to it and increment the wording.)"
        f"Best regards,\nYour Message Me When It's Hot Team"
    )
    return subject, body

email_list = ["natalia.ribeirosantos@utas.edu.au", "ranisa.gupta@csiro.au","m.hemming@unsw.edu.au"]
temperature_value = "2"
location='Maria Island'
depth = '21'
summary = "A new heatwave has led to unprecedented temperatures."
subject, body = create_email_content(True, True, temperature_value, summary, location, depth)



def send_email():
    # Create an SES client
    ses_client = boto3.client('ses', region_name='ap-southeast-2')  # Change the region if needed

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
                'ToAddresses': [
                    RECIPIENT,
                ],
            },
            Message={
                'Body': {
                    'Text': {
                        'Charset': CHARSET,
                        'Data': BODY_TEXT,
                    },
                },
                'Subject': {
                    'Charset': CHARSET,
                    'Data': SUBJECT,
                },
            },
            Source=SENDER,
        )
    except ClientError as e:
        print(e.response['Error']['Message'])
    else:
        print("Email sent! Message ID:"),
        print(response['MessageId'])

# Call the function to send an email
send_email()
