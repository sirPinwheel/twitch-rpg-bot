import socket
from threading import Thread, Lock
from typing import Callable, List, Any

class IrcClient():
    def __init__(self) -> None:
        self._host: str
        self._port: int
        self._user: str
        self._oauth: str
        self._channel: str

        self._connection: Any = None

        self._connection_lock = Lock()
        self._send_lock = Lock()
        self._message_handlers_lock = Lock()

        self._message_handlers: List[Callable[[str], None]] = []

    def __del__(self) -> None:
        if self._connection is not None:
            self.disconnect()
    
    def connect(self, host: str, port: int, user: str, oauth: str, channel: str) -> None:
        self._connection_lock.acquire()
        
        try:
            if self._connection is None:
                self._connection = socket.socket()

                try:
                    self._connection.connect((host, port))
                except socket.gaierror:
                    raise RuntimeError("Connection attempt failed")

                self._connection.send(f'PASS {oauth}\r\n'.encode('utf-8'))
                self._connection.send(f'NICK {user}\r\n'.encode('utf-8'))
                self._connection.send(f'USER {user} {host} : {user}\r\n'.encode('utf-8'))
                self._connection.send(f'JOIN {channel}\r\n'.encode('utf-8'))

                self._host = host
                self._port = port
                self._user = user
                self._oauth = oauth
                self._channel = channel

                self._message_thread = Thread(target=self._message_loop)
                self._message_thread.start()

            else:
                raise RuntimeError('The client is already connected')
        finally:
            self._connection_lock.release()

    def disconnect(self) -> None:
        self._connection_lock.acquire()

        connection = self._connection
        self._connection = None

        self._connection_lock.release()

        if connection is not None:
            connection.send(f'PART {self._channel}\r\n'.encode('utf-8'))
            connection.close()
        else:
            raise RuntimeError('The client is not connected')

        if self._message_thread is not None:
            self._message_thread.join()
        else:
            raise RuntimeError('The message thread is not running')
    
    def is_connected(self) -> bool:
        if self._connection is None:
            return False
        else:
            return True
    
    def _send_data(self, data) -> None:
        self._send_lock.acquire()

        try:
            data_sent = 0
            while data_sent < len(data):
                data_sent += self._connection.send(data[data_sent:])
        finally:
            self._send_lock.release()

    def _message_loop(self) -> None:
        buffer = ""
        while self._connection is not None:
            message_end = buffer.find('\r\n')
            if message_end == -1:
                buffer += self._connection.recv(1024).decode('utf-8')
            else:
                message = buffer[:message_end]
                buffer = buffer[message_end + 2:]
                self._process_message(message)

    def send_message(self, message: str) -> None:
        if self._connection is None:
            raise RuntimeError('The client is not connected')

        self._send_data(f'PRIVMSG {self._channel} :{message}\r\n'.encode('utf-8'))

    def _process_message(self, message) -> None:
        if message[:4] == "PING":
            self._send_data(f'PONG {message[4:]}\r\n'.encode('utf-8'))
            return

        self._message_handlers_lock.acquire()
        try:
            for message_handler in self._message_handlers:
                message_handler(message)
        finally:
            self._message_handlers_lock.release()

    def register_message_handler(self, message_handler: Callable[[str], None]) -> None:
        self._message_handlers_lock.acquire()
        try:
            self._message_handlers.append(message_handler)
        finally:
            self._message_handlers_lock.release()

    def unregister_message_handler(self, message_handler: Callable[[str], None]) -> None:
        self._message_handlers_lock.acquire()
        try:
            self._message_handlers.remove(message_handler)
        finally:
            self._message_handlers_lock.release()
