class VacuumCleaner:
    def clean(self):
        print("Starting cleaning...")

class Robot:
    def move(self):
        print("Moving in the room on wheels.")

class Roomba(Robot, VacuumCleaner):
    def auto_mode(self):
        print("Auto Mode is activated")
        self.move()
        self.clean()

my_roomba = Roomba()

my_roomba.move()
my_roomba.clean()
my_roomba.auto_mode()