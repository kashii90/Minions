import pygame
import math

def draw_minion(surface, width, height):
    """
    Draw a more detailed minion on the given surface
    """
    # Colors
    MINION_YELLOW = (255, 224, 47)
    MINION_BLUE = (29, 172, 214)
    GOGGLE_GRAY = (150, 150, 150)
    BLACK = (0, 0, 0)
    WHITE = (255, 255, 255)
    BROWN = (139, 69, 19)
    
    # Clear the surface
    surface.fill((0, 0, 0, 0))
    
    # Body proportions
    body_width = width * 0.8
    body_height = height * 0.7
    body_top = height * 0.2
    
    # Draw the minion body (yellow)
    pygame.draw.ellipse(surface, MINION_YELLOW, 
                       (width * 0.1, body_top, body_width, body_height))
    
    # Draw the minion overalls (blue)
    overall_top = height * 0.5
    overall_height = height * 0.4
    pygame.draw.rect(surface, MINION_BLUE, 
                    (width * 0.2, overall_top, width * 0.6, overall_height))
    
    # Draw the overall pocket
    pocket_width = width * 0.2
    pocket_height = height * 0.15
    pocket_left = width * 0.4
    pocket_top = overall_top + height * 0.05
    pygame.draw.rect(surface, MINION_BLUE, 
                    (pocket_left, pocket_top, pocket_width, pocket_height))
    
    # Draw the overall straps
    strap_width = width * 0.1
    pygame.draw.rect(surface, MINION_BLUE, 
                    (width * 0.3, body_top + height * 0.1, strap_width, height * 0.3))
    pygame.draw.rect(surface, MINION_BLUE, 
                    (width * 0.6, body_top + height * 0.1, strap_width, height * 0.3))
    
    # Draw the goggle strap
    goggle_strap_height = height * 0.08
    goggle_strap_top = body_top + height * 0.15
    pygame.draw.rect(surface, GOGGLE_GRAY, 
                    (width * 0.1, goggle_strap_top, width * 0.8, goggle_strap_height))
    
    # Draw the goggle
    goggle_width = width * 0.5
    goggle_height = height * 0.2
    goggle_left = width * 0.25
    goggle_top = body_top + height * 0.1
    pygame.draw.ellipse(surface, GOGGLE_GRAY, 
                       (goggle_left, goggle_top, goggle_width, goggle_height))
    
    # Draw the eye (white background)
    eye_size = width * 0.2
    eye_center_x = width * 0.5
    eye_center_y = goggle_top + goggle_height * 0.5
    pygame.draw.circle(surface, WHITE, (eye_center_x, eye_center_y), eye_size)
    
    # Draw the pupil (brown)
    pupil_size = eye_size * 0.6
    pygame.draw.circle(surface, BROWN, (eye_center_x, eye_center_y), pupil_size)
    
    # Draw the iris (black)
    iris_size = pupil_size * 0.5
    pygame.draw.circle(surface, BLACK, (eye_center_x, eye_center_y), iris_size)
    
    # Draw the mouth - a happy upward curved smile
    mouth_width = width * 0.4
    mouth_height = height * 0.15
    mouth_left = width * 0.3
    mouth_top = body_top + height * 0.4
    
    # Draw a simple curved line for the smile (upward curve for happiness)
    # Using an arc from pi to 2*pi makes it curve upward
    pygame.draw.arc(surface, BLACK, 
                   (mouth_left, mouth_top - mouth_height * 0.5, mouth_width, mouth_height), 
                   math.pi, 2 * math.pi, 4)
    
    # Draw hair (a few strands)
    hair_top = body_top - height * 0.05
    for i in range(5):
        hair_x = width * (0.3 + i * 0.1)
        pygame.draw.line(surface, BLACK, 
                        (hair_x, hair_top), 
                        (hair_x, hair_top - height * 0.1), 2)
    
    # Draw arms
    arm_width = width * 0.1
    arm_height = height * 0.3
    # Left arm
    pygame.draw.ellipse(surface, MINION_YELLOW, 
                       (width * 0.05, height * 0.4, arm_width, arm_height))
    # Right arm
    pygame.draw.ellipse(surface, MINION_YELLOW, 
                       (width * 0.85, height * 0.4, arm_width, arm_height))
    
    # Draw hands (small circles at the end of arms)
    hand_size = width * 0.08
    pygame.draw.circle(surface, MINION_YELLOW, 
                      (width * 0.1, height * 0.65), hand_size)
    pygame.draw.circle(surface, MINION_YELLOW, 
                      (width * 0.9, height * 0.65), hand_size)
    
    # Draw feet
    foot_width = width * 0.2
    foot_height = height * 0.1
    pygame.draw.ellipse(surface, BLACK, 
                       (width * 0.25, height * 0.9, foot_width, foot_height))
    pygame.draw.ellipse(surface, BLACK, 
                       (width * 0.55, height * 0.9, foot_width, foot_height))
    
    return surface

def draw_banana(surface, width, height):
    """
    Draw a Cavendish banana on the given surface
    """
    # Colors
    BANANA_YELLOW = (255, 225, 53)
    BANANA_SHADOW = (227, 207, 87)
    BANANA_STEM = (165, 124, 27)
    
    # Clear the surface
    surface.fill((0, 0, 0, 0))
    
    # Banana body - curved shape
    banana_points = [
        (width * 0.5, height * 0.1),  # Top middle
        (width * 0.8, height * 0.3),  # Upper right
        (width * 0.9, height * 0.6),  # Middle right
        (width * 0.7, height * 0.9),  # Lower right
        (width * 0.3, height * 0.9),  # Lower left
        (width * 0.1, height * 0.6),  # Middle left
        (width * 0.2, height * 0.3),  # Upper left
    ]
    
    # Draw the main banana shape
    pygame.draw.polygon(surface, BANANA_YELLOW, banana_points)
    
    # Draw the banana stem
    stem_points = [
        (width * 0.5, height * 0.1),  # Top of banana
        (width * 0.45, height * 0.05),  # Left of stem
        (width * 0.55, height * 0.05),  # Right of stem
    ]
    pygame.draw.polygon(surface, BANANA_STEM, stem_points)
    
    # Draw a shadow/highlight to give the banana some depth
    shadow_points = [
        (width * 0.7, height * 0.3),  # Upper middle
        (width * 0.8, height * 0.6),  # Middle
        (width * 0.6, height * 0.8),  # Lower middle
        (width * 0.4, height * 0.8),  # Lower middle left
        (width * 0.3, height * 0.6),  # Middle left
        (width * 0.4, height * 0.4),  # Upper middle left
    ]
    pygame.draw.polygon(surface, BANANA_SHADOW, shadow_points)
    
    return surface
