# Iterative Deepening Agent
class IDA:
    def __init__(self, environment):
        self.environment = environment
        self.action_log = []

    def dls(self, env, depth): # Depth limited search
        if all(status == 'clean' for status in env.status().values()):
            return True

        # No moves left, yet not all cells are clean
        if depth == 0:
            return False

        location = env.vacuum_location
        if env.is_dirty():
            env.clean()
            self.action_log.append(f"Clean {location}")
            if self.dls(env, depth - 1):
                return True
            env.locations[location] = 'dirty' # Undo clean
            self.action_log.pop()

        if location == 'left':
            # Only possible move is to middle
            env.move('middle')
            self.action_log.append("Move to middle")
            if self.dls(env, depth - 1):
                return True
            env.move('left')  # Undo movement
            self.action_log.pop()

        elif location == 'middle':
            # Move to left
            env.move('left')
            self.action_log.append("Move to left")
            if self.dls(env, depth - 1):
                return True
            env.move('middle')  # Undo movement
            self.action_log.pop()

            # Move to right
            env.move('right')
            self.action_log.append("Move to right")
            if self.dls(env, depth - 1):
                return True
            env.move('middle')  # Undo movement
            self.action_log.pop()

        elif location == 'right':
            # Only possible move is to middle
            env.move('middle')
            self.action_log.append("Move to middle")
            if self.dls(env, depth - 1):
                return True
            env.move('right')  # Undo movement
            self.action_log.pop()

        return False

    def iterative_deepening_search(self):
        depth = 0
        while True:
            if self.dls(self.environment, depth):
                return depth
            depth += 1