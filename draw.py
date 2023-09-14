from PIL import Image, ImageDraw
import random
import math

# Function to calculate distance from center
def distance_from_center(x, y, width, height):
    center_x, center_y = width // 2, height // 2
    return math.sqrt((x - center_x) ** 2 + (y - center_y) ** 2)

# Function to generate a pattern block
def draw_tile(draw, x, y, size, colors, bg_color, width, height, max_dist):
    dist = distance_from_center(x + size // 2, y + size // 2, width, height)
    
    edge_threshold = 75  # The width of the inner border in pixels where clustering will occur
    prob_bg = int(4 - (dist / max_dist) * 4)  # More shapes at center, fewer at edges

    # For the inner border
    if edge_threshold <= x <= width - edge_threshold - size and edge_threshold <= y <= height - edge_threshold - size:
        pass  # Do not change prob_bg
    else:
        prob_bg = min(prob_bg, 1)  # Force dense clustering in the inner border
    
    if random.randint(0, 4) > prob_bg:  # Reverse the logic
        draw.rectangle([x, y, x + size, y + size], bg_color)
        return

    color = random.choice(colors)
    draw.rectangle([x, y, x + size, y + size], color)

    inner_size = size // 4
    for i in range(4):
        for j in range(4):
            if random.randint(0, 2) == 0:
                draw.rectangle(
                    [x + i * inner_size, y + j * inner_size, x + (i + 1) * inner_size, y + (j + 1) * inner_size],
                    bg_color)
                continue

            color = random.choice(colors)
            if (i + j) % 2 == 0:
                draw.rectangle(
                    [x + i * inner_size, y + j * inner_size, x + (i + 1) * inner_size, y + (j + 1) * inner_size],
                    color)

# Function to generate the entire carpet
def draw_carpet(width, height):
    bg_color = '#' + random.choice(['8B', 'A0', 'B0']) + '0000'
    fg_colors = ['#000080', '#FFFFFF', '#006400', '#EEEED1', '#000000']

    img = Image.new('RGB', (width, height), bg_color)
    draw = ImageDraw.Draw(img)

    tile_size = 4

    # Calculate max_dist using a corner point for accurate scaling
    max_dist = distance_from_center(0, 0, width, height)

    for x in range(0, width // 2, tile_size):
        for y in range(0, height // 2, tile_size):
            draw_tile(draw, x, y, tile_size, fg_colors, bg_color, width, height, max_dist)

    top_half = img.crop((0, 0, width, height // 2))
    img.paste(top_half.transpose(Image.FLIP_TOP_BOTTOM), (0, height // 2))

    left_half = img.crop((0, 0, width // 2, height))
    img.paste(left_half.transpose(Image.FLIP_LEFT_RIGHT), (width // 2, 0))

    return img

carpet = draw_carpet(800, 400)
carpet.save("random_persian_carpet_v4.png")
