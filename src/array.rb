#!/usr/local/bin/ruby
a=[16,253,326,13]
# for i in a
#   puts i
# end


if a[0]%2==0
  a.delete_at 0
end

a.each do |i|
  puts i+1
end