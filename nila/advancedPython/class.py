#!/usr/bin/python

class Employee:
   'Common base class for all employees'
   empCount = 0

   def __init__(self, name, salary, *vartuple, **checkAttr):
      self.name = name
      self.salary = salary
      Employee.empCount += 1
   
   def displayCount(self):
     print "Total Employee %d" % Employee.empCount

   def displayEmployee(self):
      print "Name : ", self.name,  ", Salary: ", self.salary
      
   # Function definition is here
   def printinfo( arg1, *vartuple, **checkAttr ):
     "This prints a variable passed arguments"
     print "Output is: "
     print arg1
     for var in vartuple:
        print var
     return

# Now you can call printinfo function
# printinfo( 10 )
# printinfo( 70, 60, 50 )

"This would create first object of Employee class"
emp1 = Employee("Zara", 2000)
"This would create second object of Employee class"
emp2 = Employee("Manni", 5000)
emp1.displayEmployee()
emp2.displayEmployee()
emp1.printinfo( 10 )
emp1.printinfo( 70, 60, 50 )
# print "Total Employee %d" % Employee.empCount