import asyncio
from rover_common import aiolcm
from rover_msgs import GPS
from rover_common.aiohelper import run_coroutines

def testCallback(channel, msg):
    print("called back")
    print(channel, GPS.decode(msg).quality)

def init():
    lcm = aiolcm.AsyncLCM()
    lcm.subscribe("/gps", testCallback)
    return lcm

async def run():
    while True:
        print("running loop")
        await asyncio.sleep(1) 

def main():
    lcm = init()
    run_coroutines(lcm.loop(), run())

if __name__ == "__main__":
    main()