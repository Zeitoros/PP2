class Person:
  def __init__(self, fname, lname):
    self.firstname = fname
    self.lastname = lname

  def printname(self):
    print(self.firstname, self.lastname)

x = Person("Han Sooyoung", "Oldest Dream")
x.printname()


class Student(Person):
    pass

y = Student("Kim Dokja", "Yoo Joong-Hyuk")
y.printname()