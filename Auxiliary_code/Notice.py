import requests
import json


def send_notice(event_name="Notice_SuperIdiot", key="ookE4B-wCVZLbcGmiWwS3rC_Iqpxn0wH7oDusbnFC65", text="123"):

    url = f"https://maker.ifttt.com/trigger/{event_name}/with/key/{key}"
    payload = {"value": text}
    headers = {"Content-type": "application/json"}
    response = requests.request("Post", url, data=json.dumps(payload), headers=headers)
    print(response.text)


