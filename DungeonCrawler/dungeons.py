
class dungeon:
    def __init__(self, name, description, enemies, rewards):
        self.name = name
        self.description = description
        self.enemies = enemies  # List of enemy objects
        self.rewards = rewards  # List of reward objects

    def enter(self):
        print(f"Entering the dungeon: {self.name}")
        print(self.description)
        # Logic for encountering enemies and collecting rewards would go here

    def exit(self):
        print(f"Exiting the dungeon: {self.name}")