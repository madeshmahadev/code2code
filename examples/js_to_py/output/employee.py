from person import Person
class Employee(Person):
    def __init__(self, name, age, job_title):
        super().__init__(name, age)
        self.job_title = job_title

    def work(self):
        print(f'{self.name} is working as a {self.job_title}.')

if __name__ == '__main__':
    import sys
    if sys.version_info.major < 3:
        raise TypeError('This module requires Python version >= 3')
    __package__ = 'employee'