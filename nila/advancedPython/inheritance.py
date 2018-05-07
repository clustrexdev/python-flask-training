#!/usr/bin/python

class Parent:        # define parent class
   def myMethod(self):
      print 'Calling parent method'
   def myMethod1(self):
      print 'Calling parent method1'

class Child(Parent): # define child class
   def myMethod(self):
      print 'Calling child method'

c = Child()          # instance of child
c.myMethod1()         # child calls overridden method