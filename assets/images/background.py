import pygame

def create_brick_background(width, height):
    """
    Create a grey brick background surface
    """
    # Colors
    BRICK_COLOR = (120, 120, 120)  # Grey
    MORTAR_COLOR = (180, 180, 180)  # Light grey
    
    # Brick dimensions
    brick_width = 60
    brick_height = 30
    mortar_thickness = 5
    
    # Create surface
    background = pygame.Surface((width, height))
    background.fill(MORTAR_COLOR)
    
    # Draw bricks in alternating pattern
    for y in range(0, height, brick_height + mortar_thickness):
        offset = 0
        # Offset every other row for a more realistic brick pattern
        if (y // (brick_height + mortar_thickness)) % 2 == 1:
            offset = brick_width // 2
            
        for x in range(-offset, width, brick_width + mortar_thickness):
            pygame.draw.rect(background, BRICK_COLOR, 
                            (x, y, brick_width, brick_height))
    
    return background
