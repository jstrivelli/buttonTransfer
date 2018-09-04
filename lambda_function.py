#this function is invoked via SNS when the CodePipeline manual approval action starts.
# It will take the details from this approval notification and sent an interactive message to Slack that allows users to approve or cancel the deployment.

import os
import json
import logging
import urllib.parse

from base64 import b64decode
from urllib.request import Request, urlopen
from urllib.error import URLError, HTTPError

# This is passed as a plain-text environment variable for ease of demonstration.
# Consider encrypting the value with KMS or use an encrypted parameter in Parameter Store for production deployments.
SLACK_WEBHOOK_URL = "https://hooks.slack.com/services/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"
SLACK_CHANNEL = "#general"

logger = logging.getLogger()
logger.setLevel(logging.INFO)

def lambda_handler(event, context):
    #print("Received event: " + json.dumps(event, indent=2))
    #message = event["Records"][0]["Sns"]["Message"]
    
    #data = json.loads(message) 
    #token = data["approval"]["token"]
    #codepipeline_name = data["approval"]["pipelineName"]
    
    
    slack_message = {
        "channel": SLACK_CHANNEL,
        "text": "Would you like to promote the build to production?",
        "attachments": [
            {
                "text": "Yes to deploy your build to production",
                "fallback": "You are unable to promote a build",
                "callback_id": "wopr_game",
                "color": "#3AA3E3",
                "attachment_type": "default",
                "actions": [
                    {
                        "name": "deployment",
                        "text": "Yes",
                        "style": "danger",
                        "type": "button",
                        "confirm": {
                            "title": "Are you sure?",
                            "text": "This will deploy the build to production",
                            "ok_text": "Yes",
                            "dismiss_text": "No"
                        }
                    },
                    {
                        "name": "deployment",
                        "text": "No",
                        "type": "button"
                    }  
                ]
            }
        ]
    }

    print("BEFORE I HIT REQUEST")
    req = Request(SLACK_WEBHOOK_URL, json.dumps(slack_message).encode('utf-8'))
    try:
       response = urlopen(req)
       response.read()
       logger.info("Message posted to %s", slack_message['channel'])
    except HTTPError as e:
        logger.error("Request failed: %d %s", e.code, e.reason)
    except URLError as e:
        logger.error("Server connection failed: %s", e.reason)
 
