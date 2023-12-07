import asyncio
from asyncio import StreamReader, Lock, StreamWriter
from typing import Any



async def read_messages(reader: StreamReader, task_group: Any, lock: Lock) -> None:
    '''
    Asynchronously reads messages from reader and displays them on the screen.
    :param reader (StreamReader): object for reading data.
    :param task_group (Any): a task group for managing asynchronous tasks.
    :param lock (Lock): lock object for synchronizing access to resources.
    :return: None
    '''
    try:
        while True:
            data = await reader.read(1000)
            if not data:
                break
            message = data.decode().strip()
            async with lock: # to display the chat normally on the screen
                print('\x1b[2K\r', end='') # clear the console line and move the cursor to the beginning of the line
                print(message, end='') # print the message on current line
                print('\nYou: ', end='', flush=True) # print 'You: ' on the next line and flush the output
    except asyncio.CancelledError:
        pass # not realised
    finally:
        await task_group.cancel_remaining()


async def send_messages(writer: StreamWriter, task_group: Any, lock: Lock) -> None:
    '''
    Asynchronously sends user-entered messages via writer.
    :param writer (StreamWriter): object for writing data.
    :param task_group (Any): a task group for managing asynchronous tasks.
    :param lock (Lock): lock object for synchronizing access to resources.
    :return: None
    '''
    try:
        while True:
            message = await asyncio.to_thread(input, "You: ") # to thread cuz input blocking function
            async with lock:
                writer.write(message.encode()) # send message
                await writer.drain()
            if message.lower() == 'exit':
                break
    except asyncio.CancelledError:
        pass # not realised
    finally:
        await task_group.cancel_remaining()

async def main() -> None:
    '''
    Basic asynchronous function for connection management and messaging.
    :return: None
    '''
    lock = asyncio.Lock()
    try:
        reader, writer = await asyncio.open_connection('127.0.0.1', 8888)

        async with asyncio.TaskGroup() as task_group: # to manage the tasks as a group (insteead using "gather")
            task_group.create_task(read_messages(reader, task_group, lock))
            task_group.create_task(send_messages(writer, task_group, lock))

    except (asyncio.CancelledError, KeyboardInterrupt):
        pass # not realised

    finally:
        if not writer.is_closing():
            writer.close()
            await writer.wait_closed()

if __name__ == "__main__":
    asyncio.run(main())
