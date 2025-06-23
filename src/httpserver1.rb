#! /usr/bin/ruby
require "socket"

def server client
  loop do
    b = client.gets&.chomp
    pp b
    client.puts(b)
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

