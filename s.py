import asyncio
import numpy as np
from time import perf_counter

most_recent_data = np.zeros(100)
CLIENT_A_PORT = 9999
CLIENT_B_PORT = 8888
sum_num = 0
timer = None
async def handle_echo(reader, writer):
    global timer
    global most_recent_data, sum_num
    data = await reader.read(100)
    message = data.decode()
    sum_num += int(message)
    addr = writer.get_extra_info('peername')

    print(f"Received {message!r} from {addr!r}")

    if addr == ('192.168.1.54', CLIENT_A_PORT):
        # received data from client, so store it
        most_recent_data = data
    elif addr == ('192.168.1.54', CLIENT_B_PORT):
        # data is requested
        writer.write(most_recent_data.flatten().tobytes())
    resp = f"SUM: {sum_num}"
    print(f"Send: {resp}")
    data = resp.encode()
    writer.write(data)
    await writer.drain()

    #print("Close the connection")
    writer.close()
    t = perf_counter()
    print(f"timer: {round(t, 2)} seconds")

async def main():
    global timer
    timer = perf_counter()
    server = await asyncio.start_server(handle_echo, '192.168.1.54', 9999)

    addr = server.sockets[0].getsockname()
    print(f'Serving on {addr}')

    async with server:
        await server.serve_forever()

asyncio.run(main())