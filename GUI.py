import pygame
import sys
from var import starting_position

WINDOW_WIDTH = 800
WINDOW_HEIGHT = 400

class GUI:
    def __init__(self, agent, initial_status):
        self.agent = agent
        self.initial_status = initial_status.copy()
        self.current_status = initial_status.copy()
        self.actions = agent.action_log
        self.action_index = 0
        self.cleaning_started = False
        self.animation_speed = 1000

        pygame.init()
        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption("Vacuum Cleaner Problem")
        
        self.WHITE = (255, 255, 255)
        self.GREEN = (0, 255, 0)
        self.RED = (255, 0, 0)
        self.BLUE = (0, 0, 255)
        self.BLACK = (0, 0, 0)

        self.CELL_SIZE = 150
        self.CELL_MARGIN = 10
        self.BUTTON_WIDTH = 150
        self.BUTTON_HEIGHT = 40

        self.font = pygame.font.Font(None, 36)
        self.clock = pygame.time.Clock()

        # Buttons
        self.rewind_button_rect = pygame.Rect(WINDOW_WIDTH - self.BUTTON_WIDTH - 10, 
                                              WINDOW_HEIGHT - self.BUTTON_HEIGHT - 10, 
                                              self.BUTTON_WIDTH, self.BUTTON_HEIGHT)
        self.regenerate_button_rect = pygame.Rect(10, WINDOW_HEIGHT - self.BUTTON_HEIGHT - 10, 
                                                  self.BUTTON_WIDTH, self.BUTTON_HEIGHT)
        self.start_button_rect = pygame.Rect((WINDOW_WIDTH // 2) - self.BUTTON_WIDTH // 2, 
                                             WINDOW_HEIGHT - self.BUTTON_HEIGHT - 10, 
                                             self.BUTTON_WIDTH, self.BUTTON_HEIGHT)

    def handle_events(self):
        """Handle user inputs like mouse clicks."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if self.rewind_button_rect.collidepoint(event.pos):
                    self.reset_animation()
                elif self.regenerate_button_rect.collidepoint(event.pos):
                    self.regenerate_environment()
                elif self.start_button_rect.collidepoint(event.pos):
                    self.start_cleaning()

    def reset_animation(self):
        """Reset the animation to the initial state."""
        self.action_index = 0
        self.current_status = self.initial_status.copy()
        self.agent.environment.vacuum_location = starting_position

    def regenerate_environment(self):
        """Regenerate the environment and reset the state."""
        self.agent.environment.generate_random_state()
        self.initial_status = self.agent.environment.status()
        self.current_status = self.initial_status.copy()
        self.action_index = 0
        self.agent.action_log.clear()
        self.agent.environment.vacuum_location = starting_position
        self.cleaning_started = False

    def start_cleaning(self):
        """Start the iterative deepening search and begin cleaning."""
        if not self.cleaning_started:
            self.agent.iterative_deepening_search()
            self.cleaning_started = True
            self.agent.environment.vacuum_location = starting_position

    def update_screen(self):
        """Update the Pygame screen with the latest state."""
        # Clear the screen
        self.screen.fill(self.WHITE)

        # Calculate the center alignment for cells
        total_width_of_cells = (3 * self.CELL_SIZE) + (2 * self.CELL_MARGIN)
        start_x = (WINDOW_WIDTH - total_width_of_cells) // 2

        # Draw the environment (the three cells)
        for index, (location, status) in enumerate(self.current_status.items()):
            x = start_x + index * (self.CELL_SIZE + self.CELL_MARGIN)
            y = (WINDOW_HEIGHT // 2) - (self.CELL_SIZE // 2) - 50
            color = self.GREEN if status == 'clean' else self.RED
            pygame.draw.rect(self.screen, color, (x, y, self.CELL_SIZE, self.CELL_SIZE))
            pygame.draw.rect(self.screen, self.BLACK, (x, y, self.CELL_SIZE, self.CELL_SIZE), 3)

        # Draw the vacuum cleaner in its current location
        vacuum_location = self.agent.environment.vacuum_location
        vacuum_index = list(self.current_status.keys()).index(vacuum_location)
        vacuum_x = start_x + vacuum_index * (self.CELL_SIZE + self.CELL_MARGIN) + (self.CELL_SIZE // 2)
        vacuum_y = (WINDOW_HEIGHT // 2) - (self.CELL_SIZE // 2) - 50 + (self.CELL_SIZE // 2)
        pygame.draw.circle(self.screen, self.BLUE, (vacuum_x, vacuum_y), 30)

        # Draw action text
        if self.cleaning_started and self.action_index < len(self.actions):
            action_text = self.actions[self.action_index]
            action_surface = self.font.render(action_text, True, self.BLACK)

            # Calculate the x-coordinate to center the action_surface
            action_surface_width = action_surface.get_width()
            x_position = (WINDOW_WIDTH - action_surface_width) // 2
            # Draw the action text centered horizontally
            self.screen.blit(action_surface, (x_position, WINDOW_HEIGHT - 150))
        
        elif len(self.actions) != 0 and self.action_index >= len(self.actions):
            done_text = "Cleaned in " + str(self.action_index) + " moves!"
            done_surface = self.font.render(done_text, True, self.BLACK)

            # Calculate the x-coordinate to center the done_surface
            done_surface_width = done_surface.get_width()
            x_position = (WINDOW_WIDTH - done_surface_width) // 2
            # Draw the finish text centered horizontally
            self.screen.blit(done_surface, (x_position, WINDOW_HEIGHT - 150))
        # Draw buttons
        self.draw_buttons()

        pygame.display.flip()
        self.clock.tick(60)

    def draw_buttons(self):
        """Draw the buttons on the screen."""
        # Draw the rewind button
        pygame.draw.rect(self.screen, self.BLACK, self.rewind_button_rect)
        button_text = self.font.render("Rewind", True, self.WHITE)
        self.screen.blit(button_text, (self.rewind_button_rect.x + 10, self.rewind_button_rect.y + 5))

        # Draw the regenerate button
        pygame.draw.rect(self.screen, self.BLACK, self.regenerate_button_rect)
        regenerate_text = self.font.render("Regenerate", True, self.WHITE)
        self.screen.blit(regenerate_text, (self.regenerate_button_rect.x + 10, self.regenerate_button_rect.y + 5))

        # Draw the start button
        pygame.draw.rect(self.screen, self.BLACK, self.start_button_rect)
        start_text = self.font.render("Clean", True, self.WHITE)
        self.screen.blit(start_text, (self.start_button_rect.x + 10, self.start_button_rect.y + 5))

    def perform_action(self):
        """Perform the next action in the action log."""
        if self.action_index < len(self.actions):
            action = self.actions[self.action_index]            
            if "Clean" in action:
                location = action.split()[-1]
                self.current_status[location] = 'clean'
                self.agent.environment.clean()

            elif "Move to" in action:
                location = action.split()[-1]
                self.agent.environment.move(location)

            self.action_index += 1
            pygame.time.delay(self.animation_speed)
    
    def run(self):
        """Run the main event loop for the GUI."""
        while True:
            self.handle_events()
            self.update_screen()

            # Perform actions based on the log if cleaning has started
            if self.cleaning_started and self.action_index < len(self.actions):
                self.perform_action()
