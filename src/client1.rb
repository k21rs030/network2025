#! /usr/local/bin/ruby
hostname=ARGV[0]
dir=ARGV[1]

require "socket"
# s=TCPSocket.open("www.is.kyusan-u.ac.jp",80)
s=TCPSocket.open(hostname,"http")
s.print("GET %s HTTP/1.1\r\n" %[dir])
s.print("Host: %s\r\n" %[hostname])
s.print("Connection: close\r\n")
s.print("\r\n")

while true
  p = s.gets()

  if p=="\r\n"
    break
  end
end

while true
  p = s.gets()
  if p==nil
    break
  end
  puts(p)
end