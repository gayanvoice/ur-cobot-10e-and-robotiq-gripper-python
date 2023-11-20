import asyncio
from AddQual import addqual_global


class AddQualQueue:
    @staticmethod
    def stdin_listener():
        while True:
            selection = input("Press Q to quit AddQual Cobot IoT App\n")
            if selection == "Q" or selection == "q":
                addqual_global.is_queue_running = False
                break

    async def listen(self, queue):
        loop = asyncio.get_running_loop()
        user_finished = loop.run_in_executor(None, self.stdin_listener)
        await user_finished
        await queue.put(None)
