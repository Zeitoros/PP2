class Dog:
    species = "Canis familiaris"
    total_dogs = 0

    def __init__(self, name):
        self.name = name
        Dog.total_dogs += 1
    
    def display_info(self):
        print(f"{self.name} is a {self.species}. Total dogs created: {Dog.total_dogs}")

d1 = Dog("Fido")
d2 = Dog("Buddy")

d1.display_info()
d2.display_info()

print(Dog.species)

Dog.species = "Canine"
d1.display_info()
