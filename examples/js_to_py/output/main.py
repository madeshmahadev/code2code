from person import Person
from employee import Employee

person = Person('Alice', 30)
person.greet()

employee = Employee('Bob', 40, 'Software Engineer')
employee.greet()
employee.work()