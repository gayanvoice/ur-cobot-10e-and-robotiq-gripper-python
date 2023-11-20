import asyncio

from AddQual.ur_cobot import URCobot
from AddQual.robotiq_gripper import RobotiqGripper

host = '192.0.0.1'


async def main():
    try:
        queue = asyncio.Queue()
        ur_cobot = URCobot()
        robotiq_gripper = RobotiqGripper()
        await asyncio.gather(ur_cobot.connect_azure_iot(queue), robotiq_gripper.connect_azure_iot(queue))
    except asyncio.exceptions.CancelledError:
        print("main:The execution of the thread was manually stopped due to a KeyboardInterrupt signal.")
    except SystemExit:
        print("main:Cobot client was stopped.")


if __name__ == '__main__':
    asyncio.run(main())
