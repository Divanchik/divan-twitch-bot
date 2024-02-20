import requests
from json import dumps
import webbrowser
import json

def validate_token(token):
    resp = requests.get(
        "https://id.twitch.tv/oauth2/validate",
        headers={"Authorization": f"OAuth {token}"}
    )
    return resp.status_code == 200


def get_access_token(client_id, client_secret, auth_code):
    resp = requests.post(
        "https://id.twitch.tv/oauth2/token",
        headers={"Content-Type": "application/x-www-form-urlencoded"},
        data={
            "client_id": client_id,
            "client_secret": client_secret,
            "code": auth_code,
            "grant_type": "authorization_code",
            "redirect_uri": "http://localhost:3000"
        }
    )
    return resp.json()


def refresh_token(client_id, client_secret, refresh_token):
    resp = requests.post(
        "https://id.twitch.tv/oauth2/token",
        headers={"Content-Type": "application/x-www-form-urlencoded"},
        data={
            "client_id": client_id,
            "client_secret": client_secret,
            "grant_type": "refresh_token",
            "refresh_token": refresh_token
        }
    )
    return resp.json()


if __name__ == "__main__":
    with open("config.json") as f:
        conf = json.load(f)

    url = "https://id.twitch.tv/oauth2/authorize?response_type=code"
    url += "&client_id=" + conf['client_id']
    url += "&redirect_uri=http://localhost:5000"
    url += "&scope=chat%3Aread+channel%3Aread%3Aredemptions"
    webbrowser.open(url, 2)