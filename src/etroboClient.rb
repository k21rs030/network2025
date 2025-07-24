require "socket"
require 'digest/sha2'
fp = "Documents.zip"
bs = 128
client = TCPSocket.open("localhost",80)
puts("CONNECTED TO THE SERVER.")
size = File.size(fp)
last_bs = size%bs
hash = Digest::SHA256.hexdigest(File.read(fp))


# sends file size 
puts("File size: " + size.to_s() + " bytes")
client.puts(size)
# sends block size
puts("Block size: " + bs.to_s() + " bytes")
client.puts(bs)
# sends hash
puts("Calculated hash: " + hash)
client.puts(hash)



data = File.read(fp)
seek = 0
loop_count = (size/bs).to_i()
loop_count.times do
  dtbs=data[seek..seek+bs-1]
  client.write(dtbs)
  print(dtbs)
  seek+=bs
end
client.write(data[seek..seek+last_bs])
print(data[seek..seek+last_bs])
puts()


status_code = client.read(1).to_i()
puts("Retrieved status code: ",status_code)
begin
  if status_code==1
    puts("✅ Data has been sent successfully")
  elsif status_code==2
    puts("❌ Data arrived but corrupted")
  else
    puts('🤷 Server claims an unknown error occurred')

  end
rescue
  puts('🤷 Server claims an unknown error occurred')

end
