# file = File.open("sample.txt","r")
# line =  file.read()
# puts line
# file.close

a = 1
File.open(ARGV[0],"r") do |file|
    while line = file.gets&.chomp
        # puts a.to_s + ": " +  line
        # a+=1
        puts ("#{a}: #{line}")
        a+=1
    end
end