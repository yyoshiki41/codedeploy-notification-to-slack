import json
import logging
import os
from base64 import b64decode
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

import boto3

# The base-64 encoded, encrypted key (CiphertextBlob) stored in the kmsEncryptedHookUrl environment variable
ENCRYPTED_HOOK_URL = os.environ['kmsEncryptedHookUrl']
# The Slack channel to send a message to stored in the slackChannel environment variable
SLACK_CHANNEL = os.environ['slackChannel']

HOOK_URL = "https://" + boto3.client('kms').decrypt(CiphertextBlob=b64decode(ENCRYPTED_HOOK_URL))['Plaintext'].decode('utf-8')


logger = logging.getLogger()
logger.setLevel(logging.INFO)


def lambda_handler(event, context):
    print("Received event: " + json.dumps(event, indent=2))
    message = event['Records'][0]['Sns']['Message']
    print("From SNS: " + message)

    subject = event['Records'][0]['Sns']['Subject']
    messageDict = json.loads(message)
    applicationName = messageDict['applicationName']
    deploymentId = messageDict['deploymentId']
    deploymentGroupName = messageDict['deploymentGroupName']
    createTime = messageDict['createTime']
    completeTime = messageDict['completeTime']
    status = messageDict['status']

    if status == 'FAILED':
        slackColor = 'danger'
        slackValue = messageDict['errorInformation']
    else:
        slackColor = 'good'
        slackValue = messageDict['status']

    slack_message = {
        'channel': SLACK_CHANNEL,
        'attachments': [
            {
                'fallback': 'Required plain-text summary of the attachment.',
                'color': slackColor,
                'title': subject,
                'fields': [
                    {
                        'title': 'status',
                        'value': status,
                        'short': True
                    },
                    {
                        'title': 'deploymentId',
                        'value': deploymentId,
                        'short': True
                    },
                    {
                        'title': 'applicationName',
                        'value': applicationName,
                        'short': True
                    },
                    {
                        'title': 'deploymentGroupName',
                        'value': deploymentGroupName,
                        'short': True
                    }
                ]
            }
        ]
    }

    req = Request(HOOK_URL, json.dumps(slack_message).encode('utf-8'))
    try:
        response = urlopen(req)
        response.read()
        logger.info("Message posted to %s", slack_message['channel'])
    except HTTPError as e:
        logger.error("Request failed: %d %s", e.code, e.reason)
    except URLError as e:
        logger.error("Server connection failed: %s", e.reason)
