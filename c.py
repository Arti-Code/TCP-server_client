import asyncio
import random

async def tcp_echo_client(message):
    reader, writer = await asyncio.open_connection(
        '192.168.1.54', 9999) #somehow set the address for the writer permanently

    print(f'Send: {message!r}')
    writer.write(message.encode())

    data = await reader.read(100)
    print(f'Received: {data.decode()!r}')

    #print('Close the connection')
    writer.close()

async def main():
    while True:
        r = random.randint(0, 20)
        await tcp_echo_client(str(r))
        await asyncio.sleep(r)

asyncio.run(main())