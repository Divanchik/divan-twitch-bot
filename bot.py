import asyncio
import websockets
import json
from tokenfunc import *


async def handle_message(wsock, message):
    print("Raw message:", message)


async def listener(wsock):
    async for raw in wsock:
        messages = raw.split('\n')
        for message in messages:
            await handle_message(wsock, message)


async def main(conf: dict):
    uri = "ws://irc-ws.chat.twitch.tv:80"
    async with websockets.connect(uri) as wsock:
        await wsock.send("CAP REQ :twitch.tv/commands twitch.tv/tags")
        await wsock.send(f"PASS oauth:{conf['access_token']}")
        await wsock.send(f"NICK {conf['nick']}")
        resp = await wsock.recv()
        print(json.dumps(resp, indent=4, ensure_ascii=False))

        await wsock.send(f"JOIN #{conf['channel']}")
        resp = await wsock.recv()
        print(json.dumps(resp, indent=4, ensure_ascii=False))

        await listener(wsock)


if __name__ == "__main__":
    with open("config.json") as f:
        conf = json.load(f)

    if not validate_token(conf['access_token']):
        print("Refreshing...")
        r = refresh_token(conf['client_id'], conf['client_secret'], conf['refresh_token'])
        print(json.dumps(r, indent=2, ensure_ascii=False))
        conf['access_token'] = r['access_token']
        conf['refresh_token'] = r['refresh_token']
        with open("config.json", "w") as f:
            json.dump(conf, f)
    else:
        print("Connecting...")
        try:
            asyncio.run(main(conf))
        except KeyboardInterrupt:
            print("Shutting down...")