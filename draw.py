from PIL import Image, ImageDraw
import random

# Function to generate a pattern block
def draw_tile(draw, x, y, size, colors, bg_color):
    # Increase the chance of negative space
    if random.randint(0, 2) == 0:  # Adjust this probability to make the background more prevalent
        draw.rectangle([x, y, x+size, y+size], bg_color)
        return

    color = random.choice(colors)
    draw.rectangle([x, y, x+size, y+size], color)

    inner_size = size // 4
    for i in range(4):
        for j in range(4):
            if random.randint(0, 3) == 0:  # Increase this probability as well
                draw.rectangle(
                    [x + i * inner_size, y + j * inner_size, x + (i+1) * inner_size, y + (j+1) * inner_size], 
                    bg_color)
                continue
                
            color = random.choice(colors)
            if (i+j) % 2 == 0:
                draw.rectangle(
                    [x + i * inner_size, y + j * inner_size, x + (i+1) * inner_size, y + (j+1) * inner_size], 
                    color)

# Function to generate the entire carpet
def draw_carpet(width, height):
    # Randomly pick a shade of dark red for the background
    bg_color = '#' + random.choice(['8B', 'A0', 'B0']) + '0000'
    
    # Foreground colors (dark blue, white, dark green, pale yellow, black)
    fg_colors = ['#000080', '#FFFFFF', '#006400', '#EEEED1', '#000000']

    img = Image.new('RGB', (width, height), bg_color)
    draw = ImageDraw.Draw(img)

    tile_size = 8

    for x in range(0, width // 2, tile_size):
        for y in range(0, height // 2, tile_size):
            draw_tile(draw, x, y, tile_size, fg_colors, bg_color)

    top_half = img.crop((0, 0, width, height // 2))
    img.paste(top_half.transpose(Image.FLIP_TOP_BOTTOM), (0, height // 2))

    left_half = img.crop((0, 0, width // 2, height))
    img.paste(left_half.transpose(Image.FLIP_LEFT_RIGHT), (width // 2, 0))
    
    return img

carpet = draw_carpet(800, 400)
carpet.save("random_persian_carpet.png")
