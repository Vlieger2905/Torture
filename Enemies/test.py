import pygame

def line_collides_with_obstacle(line, obstacle_rect):
    # Use clipline to check for collision
    clipped_line = obstacle_rect.clipline(line)

    if clipped_line:
        # If clipped_line is not an empty tuple, then the line collides/overlaps with the rect
        start, end = clipped_line
        return start  # Return the endpoint where the line intersects with the rect
    else:
        return None  # Return None if no collision is detected

# Example usage:
line = ((10, 10), (200, 200))  # Example line
obstacle_rect = pygame.Rect(100, 100, 200, 200)  # Example obstacle rectangle

end_point = line_collides_with_obstacle(line, obstacle_rect)
print(end_point)
if end_point:
    print("Collision detected with obstacle sprite at point:", end_point)
else:
    print("No collision detected with obstacle sprite")