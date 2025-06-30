#! /usr/bin/ruby
require "socket"
# ああああ
def server client
  fl = true
  loop do
    b = client.gets&.chomp
    # retrieved entire text 
    pp b
    if fl == true
      path = b.split(" ")[1]
      case path
      when "/hello"
        client.puts "HTTP/1.0 200 OK"
        client.puts
        client.puts("hello world")
      when "/93"
        client.puts "HTTP/1.1 301 Moved Permanently"
        client.puts "Location:  http://www.kyusan-u.ac.jp/"

        client.puts()
      else
        client.puts "HTTP/1.0 200 OK"
        client.puts("Content-Type: text/plain; charset=UTF-8")
        client.puts
        
        begin

          File.open("."+path,"r") do |file|
            while line = file.gets&.chomp
                client.puts (line)
            end
          end
          client.puts(path)
                  
        rescue 
          client.puts("File not found or cannot be opened.")
        end
        

      
      
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

