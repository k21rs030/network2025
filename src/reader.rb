# file = File.open("sample.txt","r")
# line =  file.read()
# puts line
# file.close

file=File.open("sample.txt","r")
while line  =  file.gets&.chomp
    pp line
end

file.close