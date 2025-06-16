require "socket"
def server sock
  while buf = sock.gets()
    p buf
  end
  sock.close()
end


s0 = TCPServer.open(80)
while true
  sock = s0.accept()
  server sock
end
sock.close()
s0.close()