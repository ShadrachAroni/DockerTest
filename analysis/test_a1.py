import asyncio
import aiohttp
from collections import Counter

url = "http://localhost:5000/home"
counter = Counter()

async def fetch(session, index):
    async with session.get(url) as response:
        json = await response.json()
        msg = json['message']
        server_id = msg.split(":")[1].strip()
        counter[server_id] += 1
        if index % 1000 == 0:
            print(f"Sent {index} requests...")

async def main():
    async with aiohttp.ClientSession() as session:
        tasks = [fetch(session, i) for i in range(100000)]
        await asyncio.gather(*tasks)

    for k, v in counter.items():
        print(f"{k}: {v} responses")

asyncio.run(main())
