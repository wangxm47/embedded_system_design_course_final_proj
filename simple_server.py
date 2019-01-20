import time
from http.server import BaseHTTPRequestHandler, HTTPServer

import logging
import threading
import socket

# 
HOST_NAME = '0.0.0.0'
PORT_NUMBER = 9000

# REMOTE WIFI MODULE
# todo 
REMOTE_HOST = '192.168.199.228'
REMOTE_HOST_PORT = 8080


# STATE STRING 
STATE_PASSWORD_RETTING_SUCCESSFULLY = "密码重置成功"
STATE_PASSWORD_VALID = "密码正确，大门打开"
STATE_PASSWORD_INVALID = "密码错误"
STATE_WAITING_INPUT = '等待大门密码输入。。。'

PASSWORD = "123456"
connection = None

# sock = None

TIMEOUT = 0.5
# share variable, will be altered by the receiver thread.
state = STATE_WAITING_INPUT

WATING_FOR_CONNECT = False

class MyHandler(BaseHTTPRequestHandler):
    def do_HEAD(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()

    def do_GET(self):
        if(self.path == "/"):
            try:
                content = open("./front_end/index.html", "r").read()
                response = self.handle_http(200, content)
            except FileNotFoundError:
                content = "file not found"
            self.wfile.write(response)
        elif(self.path == "/poll"):
            # polling the lcok state
            # write password file
            self.wfile.write(self.handle_http(200, state))
        elif(self.path == "/bulma.css"):
            # write password file
            content = open("./front_end/bulma.css", "r").read()        
            self.wfile.write(self.handle_http(200, content, "text/css"))

    def do_POST(self):
        # 
        content_len = int(self.headers.get('content-length', 0))
        pw = self.rfile.read(content_len)
        print("post data : ", pw)
        # todo:should retrun a result to broswer
        # 把远程开锁的结果发送给wifi模块，wifi模块控制单片机开门, 同时把结果放回给浏览器显示密码的正确情况 
        # Data to wifi module  
        # data_2_wifi = None
        # # data 
        # data_2_browser = None
        data = None
        if pw.decode == PASSWORD: 
            data = b't'
        elif pw.decode != PASSWORD:
            data = b'f'
        else:
            pass
        
        
        
    def handle_http(self, status_code, content, type = 'text/html'):
        self.send_response(status_code)
        self.send_header('Content-type', type)
        self.end_headers()
        return bytes(content, 'UTF-8')


class sendDataToWifiModule(threading.Thread):
    '''
        send data the remote wifi module, data is required to be 
    '''
    def __init__(self, host_name, port_num, data):
        threading.Thread.__init__(self)
        self.host_name = host_name
        self.port_num = port_num
        self.data = data
    def run(self):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        conn = sock.connect((self.host_name, self.port_num))
        conn.send(self.data)        
    

# another handle the input from wifi module
def receiver():
    global connection
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind(('0.0.0.0',8080))
    sock.listen(5)
    while True:
        connection = None
        print("wating connection from wifi module:")
        connection, address = sock.accept()
        print("connect to wifi module with address: " + address)
        buf = connection.recv(1024)            
        input_pw = buf.decode()
        print("from wifi module:", input_pw)
        if(input_pw == PASSWORD):
            connection.send(b"t")
        else:
            connection.send(b"f")

# 如果收到信息，则打印
thread_recv = threading.Thread(target=receiver)
thread_recv.setDaemon(True)
thread_recv.start()


if __name__ == '__main__':
    server_class = HTTPServer
    httpd = server_class((HOST_NAME, PORT_NUMBER), MyHandler)
    print(time.asctime(), 'Server Starts - %s:%s' % (HOST_NAME, PORT_NUMBER))
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        pass
    httpd.server_close()
    print(time.asctime(), 'Server Stops - %s:%s' % (HOST_NAME, PORT_NUMBER))
