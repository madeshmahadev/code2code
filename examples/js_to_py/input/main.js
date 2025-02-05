const Person = require('./person');
const Employee = require('./employee');

const person = new Person('Alice', 30);
person.greet();

const employee = new Employee('Bob', 40, 'Software Engineer');
employee.greet();
employee.work();