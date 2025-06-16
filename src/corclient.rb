require "socket"
sock = TCPSocket.open("127.0.0.1", 80)
sock.write("HELLO")
sock.close