import sendgrid
import functools
import json

from urllib import request
from flask import url_for as flask_url_for

from pepites_webapp import conf

sendgrid_client = sendgrid.SendGridAPIClient(apikey=conf.SENDGRID_API_KEY)

url_for = functools.partial(flask_url_for, _scheme=conf.REDIRECT_SCHEME, _external=True)


def send_mail(template_name, recipient, **kwargs):
    '''Format and send email template with Sendgrid API
    Args:
        * template_name: str, name of sendgrid template name,
        * recipient: str, email address that will receive the mail
        * kwargs: all keyword arguments will be used to format the template
    '''
    data = {
        'personalizations': [
            {
                'to': [
                    {
                        'email': recipient,
                    }
                ],
                'substitutions': {
                    '{%s}' % k: v for k, v in kwargs.items()
                },
            },
        ],
        'from': {
            'email': conf.SENDGRID_EMAIL_FROM
        },
        'template_id': conf.SENDGRID_TEMPLATES[template_name]
    }
    try:
        response = sendgrid_client.client.mail.send.post(request_body=data)
        if response.status_code < 200 or response.status_code >= 300:
            raise Warning(
                f'Unable to send mail, '
                f'received status code {response.status_code}'
            )
    except Exception as exc:
        raise exc


def trigger_slack_alerts(msg):
    slack_data = {
        'channel': conf.SLACK_CHANNEL,
        'text': f' {msg}'
    }

    req = request.Request(
        conf.SLACK_URL,
        data=json.dumps(slack_data).encode(),
        headers={'Content-Type': 'application/json'}
    )
    response = request.urlopen(req)

    if response.status != 200:
        raise ValueError(
            'Request to slack returned an error %s, the response is:\n%s'
            % (response, response.read().decode())
        )
