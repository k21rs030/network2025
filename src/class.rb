class Person
  attr_writer :age
  def initialize name, age
    @name = name
    @age = age
  end

  def info
    @name + ": "+ @age.to_s
  end
  def set_age age
    @age=age
  end
end

p=Person.new "aaaaa",7831
puts p.info
p.set_age 32423423
puts p.info
p.age=22342423
puts p.info