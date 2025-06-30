#! /usr/bin/ruby
require "socket"

def server client
  fl = true
  loop do
    b = client.gets&.chomp
    # retrieved entire text 
    pp b
    if fl == true
      path = b.split(" ")[1]
      client.puts "HTTP/1.0 200 OK"
      client.puts
      if path == "/hello"
        client.puts("hello world")
      else
        client.puts(path)
      end
      

      fl=false
    end

    if b.empty?()
      client.close()
      sleep 60
    end
  end
end


a = TCPServer.open(80)
client = a.accept()
loop do
  Thread.new do
    server(client)
  end
  client = a.accept()

end

