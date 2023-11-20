import asyncio
from AddQual.ur_cobot import URCobot
from AddQual.robotiq_gripper import RobotiqGripper
from AddQual.addqual_queue import AddQualQueue
import logging
import pyfiglet
from AddQual import addqual_global

logging.basicConfig(filename='cobot.log', filemode='w',
                    level=logging.DEBUG,
                    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")


async def main():
    if addqual_global.is_dev_mode:
        title = pyfiglet.figlet_format("AddQual Cobot IOT App", width=200)
        mode = pyfiglet.figlet_format("Development Mode", width=200)
        logging.info("\n{title}\n{mode}".format(title=title, mode=mode))
    else:
        title = pyfiglet.figlet_format("AddQual Cobot IOT App", width=200)
        mode = pyfiglet.figlet_format("Production Mode", width=200)
        logging.info("\n{title}\n{mode}".format(title=title, mode=mode))
    try:
        queue = asyncio.Queue()
        addqual_queue = AddQualQueue()
        ur_cobot = URCobot()
        robotiq_gripper = RobotiqGripper()
        await asyncio.gather(addqual_queue.listen(queue),
                             ur_cobot.connect_azure_iot(queue),
                             robotiq_gripper.connect_azure_iot(queue))
    except asyncio.exceptions.CancelledError:
        logging.error("The execution of the thread was manually stopped due to a KeyboardInterrupt signal.")
    except SystemExit:
        logging.error("AddQual Cobot IOT App was stopped.")


if __name__ == '__main__':
    asyncio.run(main())
