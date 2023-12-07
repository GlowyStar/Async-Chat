import asyncio
from collections import namedtuple, OrderedDict



Message = namedtuple('Message', ['nickname', 'message', 'id_message']) # to keep nicknames and messages in chronological order.

clients = {}
messages = OrderedDict()


def forward(sender_nickname: str, message: Message) -> None:
    '''Shows a new member all messages in the chat room.
        :param sender_nickname (str): The alias of the sender of the message.
        :param message (Message): A forwarding message containing the alias, message text and message ID.
        :return None'''
    for nickname, writer in clients.items():
        if nickname != sender_nickname:
            writer.write(f"{sender_nickname}: {message.message}\n".encode())


async def set_nickname(reader: asyncio.StreamReader, writer: asyncio.StreamWriter) -> str:
    '''Sets the aliases for new participants.
        :param reader (asyncio.StreamReader): The stream to read the data from.
        :param writer (asyncio.StreamWriter): A stream for writing data.
        :return str: The selected alias.'''
    writer.write("Please choose a nickname: ".encode())
    await writer.drain()
    nickname = (await reader.read(1000)).decode().strip()

    writer.write("____________________________________________________________________________________________\n".encode())
    await writer.drain()
    return nickname



async def handle(reader: asyncio.StreamReader, writer: asyncio.StreamWriter) -> None:
    '''
    Handles the connection of a new client.
    :param reader (asyncio.StreamReader): Stream to read the data.
    :param writer (asyncio.StreamWriter): A stream for writing data.
    :return: None
    '''
    nickname = await set_nickname(reader, writer)
    clients[nickname] = writer

    addr = writer.get_extra_info('peername')
    message = Message(nickname, "joined the chat", len(messages) + 1)
    messages[message.id_message] = message
    print(f"{addr!r} ({nickname}) {message.message}") # log

    for mes_id, mes in messages.items(): # send message from user to another users
        if mes_id != message.id_message:
            writer.write(f"{mes.nickname}: {mes.message}\n".encode())
            await writer.drain()
    forward(nickname, message)

    try:
        while True:
            data = await reader.read(100)
            if not data:
                break

            message_content = data.decode()
            message = Message(nickname, message_content, len(messages) + 1)
            messages[message.id_message] = message # saving all messages to our collection

            forward(nickname, message)
            print(f"{nickname}: {message.message}") # log

            await writer.drain()

    finally:
        del clients[nickname]
        forward(nickname, Message(nickname, "left the chat", len(messages) + 1))
        writer.close()
        await writer.wait_closed() # close connection with client


async def main() -> None:
    '''
    starts the sever
    :return: None
    '''
    server = await asyncio.start_server(handle, '127.0.0.1', 8888)
    addr = server.sockets[0].getsockname()

    print(f'Serving on {addr}') # log

    async with server:
        await server.serve_forever()


if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Server is shutting down...")

