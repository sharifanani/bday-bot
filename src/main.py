import os
import json
import sched
import time

from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError
from datetime import datetime


def main():

    while True:
        json_path = "conf.json"
        scheduler = sched.scheduler(time.time, time.sleep)
        full_config = dict()
        with open(json_path, mode='r') as file:
            full_config = json.loads(file.read())

        bday_conf = full_config.get("config")
        # interpret all the attached bdays
        send_hour = bday_conf.get("send_hour", 8)
        send_minute = bday_conf.get("send_minute", 0)
        channel_name = bday_conf.get("channel_name", None)
        client_token = bday_conf.get("client_token", None)
        if client_token is None:
            raise AssertionError("Invalid key")
        slack_client = WebClient(token=client_token)
        bday_list = full_config.get("bdays", [])
        for bday in bday_list:
            dt = datetime.strptime(bday['date'], "%m/%d").replace(year=datetime.now().year, hour=send_hour,
                                                                  minute=send_minute)
            if dt.timestamp() < datetime.now().timestamp():
                dt = dt.replace(year=datetime.now().year+1)
            print(f"scheduled msg for {bday['name']} on {dt} ({dt.timestamp()})")
            scheduler.enterabs(
                dt.timestamp(),
                1,
                slack_client.chat_postMessage,
                kwargs={
                    "channel": channel_name,
                    "text": f"Hey <@{bday['uid']}>! Happy Birthday!!",
                },
            )
        scheduler.run(blocking=True)


if __name__ == "__main__":
    main()
#
#
# try:
#     response = client.chat_postMessage(channel='#bday-bot-tests', text="Hello world!")
#     assert response["message"]["text"] == "Hello world!"
# except SlackApiError as e:
#     # You will get a SlackApiError if "ok" is False
#     assert e.response["ok"] is False
#     assert e.response["error"]  # str like 'invalid_auth', 'channel_not_found'
#     print(f"Got an error: {e.response['error']}")
