File.open("reader.rb","r") do |file|
    while line = file.gets&.chomp
        # puts a.to_s + ": " +  line
        # a+=1
        puts (line)
    end
end