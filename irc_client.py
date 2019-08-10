import socket
from threading import Thread, Lock
from typing import Callable, List, Any
import certifi
import ssl

class IrcClient():
    """
    Class for connecting to Twitch's IRC chat server. Uses socket with SSL functionality
    """

    _instance = None

    def __new__(self):
        if self._instance == None:
            self._instance = super(IrcClient, self).__new__(self)

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

        return self._instance

    def __del__(self):
        if self._connection is not None:
            self.disconnect()
    
    def connect(self, host: str, port: int, user: str, oauth: str, channel: str) -> None:
        """
        Connects to the IRC chat using socket, saves socket object to self._connection
        SSL certificated provided by certifi module
        """

        self._connection_lock.acquire()
        
        try:
            if self._connection is None:
                self._connection = socket.socket()
                self._connection = ssl.wrap_socket(self._connection,
                    ca_certs=certifi.where(),
                    server_side=False)

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

                self._message_thread = Thread(target=self._message_loop, name="IrcMessageThread")
                self._message_thread.start()

            else:
                raise RuntimeError('The client is already connected')
        finally:
            self._connection_lock.release()

    def disconnect(self) -> None:
        """
        Performs safe disconnect informing host about it
        _connection should be None after that
        """

        self._connection_lock.acquire()

        connection = self._connection
        self._connection = None

        self._connection_lock.release()

        if connection is not None:
            connection.send(f'PART {self._channel}\r\n'.encode('utf-8'))
            connection.shutdown(socket.SHUT_RDWR)
            connection.close()
        else:
            raise RuntimeError('The client is not connected')

        if self._message_thread is not None:
            self._message_thread.join()
        else:
            raise RuntimeError('The message thread is not running')
    
    def is_connected(self) -> bool:
        """
        Checks if connection is established, returns boolean
        """

        if self._connection is None:
            return False
        else:
            return True
    
    def _send_data(self, data) -> None:
        """
        Sends raw data taking into account connection/packet limitations
        """

        self._send_lock.acquire()

        try:
            data_sent = 0
            while data_sent < len(data):
                data_sent += self._connection.send(data[data_sent:])
        finally:
            self._send_lock.release()

    def _message_loop(self) -> None:
        """
        Waits for message data to be recieved, after that
        calls _process_message
        """

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
        """
        Wraps a string in IRC specific stuff, also encodes to UTF-8 to
        be sent using _send_raw
        """

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
        """
        Registers a callable function to be a message handler. Each handler can only
        take one string parameter and should return nothing
        """

        self._message_handlers_lock.acquire()
        try:
            if message_handler not in self._message_handlers:
                self._message_handlers.append(message_handler)
            else:
                raise RuntimeError("Tried to register the same handler twice")
        finally:
            self._message_handlers_lock.release()

    def unregister_message_handler(self, message_handler: Callable[[str], None]) -> None:
        """
        removes a message handler
        """
        
        self._message_handlers_lock.acquire()
        try:
            if message_handler in self._message_handlers:
                self._message_handlers.remove(message_handler)
            else:
                raise RuntimeError("Tried to remove non existant handler")
        finally:
            self._message_handlers_lock.release()
