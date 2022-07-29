from slack import WebClient
from slack.errors import SlackApiError
from dotenv import load_dotenv
import os
import json

load_dotenv()
BOT_OAUTH_TOKEN = os.environ.get('BOT_USER_OAUTH_TOKEN')

# Client Set Up
slack_client = WebClient(token=str(BOT_OAUTH_TOKEN))

def sendMessage(user_id):
    try:
        slack_client.chat_postMessage(channel="#bday-bot-tests", text=f"Hey @<{user_id}>! Happy Birthday!!")
    except SlackApiError as e:
        print(f'ApiExceptionOccured: {e["message"]}')
        return False
    except Exception as e:
        print(f'Unknown Exception Occured: {e["message"]}')
    return True
    



