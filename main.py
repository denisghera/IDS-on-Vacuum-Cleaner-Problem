from Environment import *
from IDA import *
from GUI import *

if __name__ == "__main__":
    environment = Environment()
    initial_status = environment.status()

    agent = IDA(environment)

    gui = GUI(agent, initial_status)
    gui.run()