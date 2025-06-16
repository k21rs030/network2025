require "socket"
def server sock
  while buf = sock.gets()
    p buf
    sock.puts buf
  end
  sock.close()
end


s0 = TCPServer.open(80)
while true
  sock = s0.accept()
  Thread.new do
    server sock
  end
end
sock.close()
s0.close()