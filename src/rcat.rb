#/usr/local/bin/ruby


ARGV.each do |i|
    File.open(i,"r") do |file|
        while line = file.gets&.chomp
            puts (line)
        end
    end
end