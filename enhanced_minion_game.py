import pygame
import sys
import random
import os
import base64
from assets.images.minion import draw_minion, draw_banana
from assets.images.background import create_brick_background

# Initialize pygame
pygame.init()
pygame.mixer.init()  # Initialize sound mixer

# Constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
TITLE = "Minion Banana Catcher"
FPS = 60

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
YELLOW = (255, 255, 0)
BLUE = (0, 0, 255)

# Set up the display
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption(TITLE)
clock = pygame.time.Clock()

# Load fonts
font_large = pygame.font.SysFont('Arial', 48)
font_medium = pygame.font.SysFont('Arial', 36)
font_small = pygame.font.SysFont('Arial', 24)

# Create background
background = create_brick_background(SCREEN_WIDTH, SCREEN_HEIGHT)

# Create a sound file for the "banana" sound
def create_banana_sound():
    # Path to save the sound file
    sound_path = os.path.join('assets', 'sounds', 'banana.wav')
    
    # Check if the sound file already exists
    if os.path.exists(sound_path):
        return sound_path
    
    # Create a directory for sounds if it doesn't exist
    os.makedirs(os.path.dirname(sound_path), exist_ok=True)
    
    # Create a simple sound file (this will be a placeholder)
    try:
        # Create a simple sound buffer (silence)
        buffer = bytearray([128] * 8000)  # 8000 samples of silence
        
        # Save the buffer as a WAV file
        with open(sound_path, 'wb') as f:
            # Write a minimal WAV header
            f.write(b'RIFF')
            f.write((36 + len(buffer)).to_bytes(4, 'little'))  # File size
            f.write(b'WAVE')
            f.write(b'fmt ')
            f.write((16).to_bytes(4, 'little'))  # Format chunk size
            f.write((1).to_bytes(2, 'little'))  # Format (1 = PCM)
            f.write((1).to_bytes(2, 'little'))  # Channels (1 = mono)
            f.write((8000).to_bytes(4, 'little'))  # Sample rate
            f.write((8000).to_bytes(4, 'little'))  # Byte rate
            f.write((1).to_bytes(2, 'little'))  # Block align
            f.write((8).to_bytes(2, 'little'))  # Bits per sample
            f.write(b'data')
            f.write(len(buffer).to_bytes(4, 'little'))  # Data chunk size
            f.write(buffer)  # Audio data
        
        return sound_path
    except:
        return None

# Try to create and load the banana sound
banana_sound_path = create_banana_sound()
try:
    if banana_sound_path and os.path.exists(banana_sound_path):
        banana_sound = pygame.mixer.Sound(banana_sound_path)
        banana_sound.set_volume(0.7)
    else:
        # Create a dummy sound
        buffer = bytearray([128] * 4000)
        banana_sound = pygame.mixer.Sound(buffer=buffer)
        banana_sound.set_volume(0.5)
except:
    # If creating a sound fails, create a dummy sound class
    class DummySound:
        def play(self):
            pass
    banana_sound = DummySound()

class Minion(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        # Start with a simple rectangle for the minion
        self.width = 80
        self.height = 100
        self.image = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
        self.image = draw_minion(self.image, self.width, self.height)
        self.rect = self.image.get_rect()
        self.rect.midbottom = (SCREEN_WIDTH // 2, SCREEN_HEIGHT - 20)
        self.speed = 8
        self.growth_factor = 1.0
    
    def update(self):
        # Get keyboard input
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.rect.x -= self.speed
        if keys[pygame.K_RIGHT]:
            self.rect.x += self.speed
        
        # Keep minion on screen
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > SCREEN_WIDTH:
            self.rect.right = SCREEN_WIDTH
    
    def grow(self):
        # Increase size when eating a banana
        self.growth_factor += 0.05
        self.width = int(80 * self.growth_factor)
        self.height = int(100 * self.growth_factor)
        
        # Create new image with new size
        old_center = self.rect.center
        self.image = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
        self.image = draw_minion(self.image, self.width, self.height)
        self.rect = self.image.get_rect()
        self.rect.center = old_center
        
        # Make sure minion stays above ground
        self.rect.bottom = SCREEN_HEIGHT - 20

class Banana(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.width = 40
        self.height = 60
        self.image = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
        self.image = draw_banana(self.image, self.width, self.height)
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(0, SCREEN_WIDTH - self.rect.width)
        self.rect.y = random.randint(-100, -40)
        self.speed = random.randint(3, 7)
    
    def update(self):
        self.rect.y += self.speed
        
        # If banana goes off screen, it's missed
        if self.rect.top > SCREEN_HEIGHT:
            self.kill()
            return True  # Banana was missed
        return False

class Game:
    def __init__(self):
        self.running = True
        self.game_over = False
        self.score = 0
        self.missed_bananas = 0
        self.max_missed = 6
        
        # Create sprite groups
        self.all_sprites = pygame.sprite.Group()
        self.bananas = pygame.sprite.Group()
        
        # Create minion
        self.minion = Minion()
        self.all_sprites.add(self.minion)
        
        # Timing for banana spawning
        self.last_banana_time = pygame.time.get_ticks()
        self.banana_spawn_delay = 1500  # milliseconds
    
    def spawn_banana(self):
        current_time = pygame.time.get_ticks()
        if current_time - self.last_banana_time > self.banana_spawn_delay:
            banana = Banana()
            self.all_sprites.add(banana)
            self.bananas.add(banana)
            self.last_banana_time = current_time
            
            # Make bananas spawn faster as the game progresses
            self.banana_spawn_delay = max(500, self.banana_spawn_delay - 10)
    
    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.running = False
                if self.game_over and event.key == pygame.K_RETURN:
                    self.__init__()  # Reset the game
    
    def update(self):
        if not self.game_over:
            self.spawn_banana()
            self.all_sprites.update()
            
            # Check for collisions between minion and bananas
            hits = pygame.sprite.spritecollide(self.minion, self.bananas, True)
            for hit in hits:
                self.score += 1
                self.minion.grow()
                # Play banana sound
                banana_sound.play()
            
            # Check for missed bananas
            for banana in list(self.bananas):
                if banana.update():  # If banana was missed
                    self.missed_bananas += 1
            
            # Check for game over
            if self.missed_bananas >= self.max_missed:
                self.game_over = True
    
    def draw(self):
        # Draw background
        screen.blit(background, (0, 0))
        
        # Draw all sprites
        self.all_sprites.draw(screen)
        
        # Draw score
        score_text = font_small.render(f"Score: {self.score}", True, WHITE)
        screen.blit(score_text, (10, 10))
        
        # Draw missed bananas
        missed_text = font_small.render(f"Missed: {self.missed_bananas}/{self.max_missed}", True, WHITE)
        screen.blit(missed_text, (10, 40))
        
        # Draw game over screen
        if self.game_over:
            # Semi-transparent overlay
            overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, 128))
            screen.blit(overlay, (0, 0))
            
            # Game over text
            game_over_text = font_large.render("GAME OVER", True, WHITE)
            screen.blit(game_over_text, 
                       (SCREEN_WIDTH // 2 - game_over_text.get_width() // 2, 
                        SCREEN_HEIGHT // 2 - 50))
            
            # Final score
            final_score_text = font_medium.render(f"Final Score: {self.score}", True, WHITE)
            screen.blit(final_score_text, 
                       (SCREEN_WIDTH // 2 - final_score_text.get_width() // 2, 
                        SCREEN_HEIGHT // 2 + 20))
            
            # Restart prompt
            restart_text = font_small.render("Press ENTER to play again or ESC to quit", True, WHITE)
            screen.blit(restart_text, 
                       (SCREEN_WIDTH // 2 - restart_text.get_width() // 2, 
                        SCREEN_HEIGHT // 2 + 80))
        
        pygame.display.flip()
    
    def run(self):
        while self.running:
            clock.tick(FPS)
            self.handle_events()
            self.update()
            self.draw()

# Main function
def main():
    game = Game()
    game.run()
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
