from person import Person

class Employee(Person):
    def __init__(self, name, age, job_title):
        super().__init__(name, age)
        self.job_title = job_title

    def work(self):
        print(f'{self.name} is working as a {self.job_title}.')