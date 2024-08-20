import _thread
import socket

# 서버 IP와 포트 설정
ip = '0.0.0.0'
port = 8080

# 서버 소켓 생성
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server_socket.bind((ip, port))
server_socket.listen()

print('Server started, waiting for clients...')

# 서버 종료 플래그
server_running = True

def threaded(client_socket, addr):
    print('Connected by: ', addr[0], ':', addr[1])
    
    while True:
        try:
            data = client_socket.recv(1024)
            if not data:
                print('Disconnected by ' + addr[0], ':', addr[1])
                break
            
            print('Received from ' + addr[0], ':', addr[1], data.decode())
            client_socket.send(data)
            
        except ConnectionAbortedError as e:
            print('Disconnected by ' + addr[0], ':', addr[1])
            print(f'Error: {e}')
            break
    
    client_socket.close()

def stop_server():
    global server_running
    server_running = False
    server_socket.close()  # 서버 소켓을 닫아서 accept()에서 빠져나오게 함
    print('Server stopped.')

# 사용자 입력을 통해 종료 명령을 받는 함수
def monitor_commands():
    global server_running
    while server_running:
        command = input("Enter 'stop' to terminate the server: ")
        if command == 'stop':
            stop_server()

# 종료 명령을 모니터링하는 스레드 시작
_thread.start_new_thread(monitor_commands, ())

# 메인 서버 루프
while server_running:
    try:
        client_socket, addr = server_socket.accept()
        _thread.start_new_thread(threaded, (client_socket, addr))
    except OSError:
        break

print('Server has been terminated.')
