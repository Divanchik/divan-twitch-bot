import asyncio
import websockets
import json
from tokenfunc import *


async def handle_message(wsock, raw):
    pass


async def listener(wsock):
    async for raw in wsock:
        await handle_message(wsock, raw)


async def main(conf: dict):
    uri = "ws://irc-ws.chat.twitch.tv:80"
    async with websockets.connect(uri) as wsock:
        await wsock.send("CAP REQ :twitch.tv/commands twitch.tv/tags")
        # PASS
        await wsock.send(f"NICK {conf['nick']}")
        resp = await wsock.recv()

        await wsock.send(f"JOIN #{conf['channel']}")
        resp = await wsock.recv()

        await listener(wsock)


if __name__ == "__main__":
    with open("config.json") as f:
        conf = json.load(f)

    if not validate_token(conf['access_token']):
        # refresh token
        with open("config.json", "w") as f:
            json.dump(conf, f)
        pass
    else:
        try:
            asyncio.run(main(conf))
        except KeyboardInterrupt:
            print("Shutting down...")