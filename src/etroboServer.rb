require "socket"
require 'digest/sha2'

def intp(schrijf, nummer)
  puts(schrijf.to_s() + ": " + nummer.to_s())
end

puts("SERVER INITIALIZED.")
server = TCPServer.open(80)
server = server.accept()
puts("CONNECTION ESTABLISHED.")

puts("Waiting for the metadata...")
size = server.gets().to_i()
intp("Received filesize",size)
bs = server.gets().to_i()
intp("Received blocksize",bs)
last_bs = size%bs
hash = server.gets()
intp("Received hash",hash)
received_data = ""

loop_count = (size/bs).to_i()


begin
  loop_count.times do
    chunk=server.read(bs)
    #print(chunk)
    #exit()
    #print(chunk)
    print(chunk)
    received_data.concat(chunk)
  end



last_chunk = server.read(last_bs)
received_data+=last_chunk
puts(last_chunk)
rescue

end
calculated_hash = Digest::SHA256.hexdigest(received_data)
puts("Generated hash: ",calculated_hash)
puts("Accepted hash : ",hash)
status_code = 9
if calculated_hash.to_s().strip == hash.to_s().strip()
  puts("✅ Verified file integrity")
  status_code=1
else
  puts("❌ Hash verification failed")
  status_code=2
end

server.write(status_code)

feliz = File.open("aaa.zip","wb")
feliz.write(received_data)


server.close()