import asyncio

info = ""

class ClientServerProtocol(asyncio.Protocol):
    def connection_made(self, transport):
         self.transport = transport

    def data_received(self, data):
        global info
        resp = data.decode()
        data_answer = ""
        if not resp:
             return "error\nwrong command\n\n"
        data_temp = resp.replace("\n", "").split()
        if data_temp[0] == "put":
            if info.find(resp.replace("put ", "")) == -1:
                info  += resp.replace("put ", "")
            else:
                info = info.replace(resp.replace("put ", ""), "")
                info  += resp.replace("put ", "")
            data_answer = "ok\n\n"
        elif data_temp[0] == "get":
            data_answer = "ok\n"
            key = data_temp[1]
            metrics = info.split("\n")
            if key == "*":
                data_answer += info
            else:
                for metric in metrics:
                    if len(metric.split()) == 3 and metric.split()[0] == key:
                        data_answer+=metric + "\n"
            data_answer  += "\n"
        else:
            data_answer = "error\nwrong command\n\n"
        self.transport.write(data_answer.encode())

loop = asyncio.get_event_loop()
coro = loop.create_server(ClientServerProtocol,"127.0.0.1", 8888)
server = loop.run_until_complete(coro)
try:
     loop.run_forever()
except KeyboardInterrupt:
     pass
server.close()
loop.run_until_complete(server.wait_closed())
loop.close()
