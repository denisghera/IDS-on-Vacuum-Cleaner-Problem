import random
from var import starting_position

class Environment:
    def __init__(self):
        self.generate_random_state()
        self.vacuum_location = starting_position

    def generate_random_state(self):
        self.locations = {
            'left': random.choice(['clean', 'dirty']),
            'middle': random.choice(['clean', 'dirty']),
            'right': random.choice(['clean', 'dirty'])
        }
        self.vacuum_location = starting_position

    def is_dirty(self):
        return self.locations[self.vacuum_location] == 'dirty'

    def clean(self):
        self.locations[self.vacuum_location] = 'clean'

    def move(self, direction):
        self.vacuum_location = direction

    def status(self):
        return self.locations.copy()