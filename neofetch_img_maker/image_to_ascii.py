import cv2
import numpy as np
from sklearn.cluster import KMeans
from sklearn.metrics import pairwise_distances_argmin_min

ansi_colors = ['#2e3436', '#cc0000', '#4e9a06', '#c4a000', '#3465a4', '#75507b', '#06989a', '#d3d7cf', '#555753', '#ef2929', '#8ae234', '#fce94f', '#729fcf', '#ad7fa8', '#34e2e2', '#eeeeec', '#000000', '#00005f', '#000087', '#0000af', '#0000d7', '#0000ff', '#005f00', '#005f5f', '#005f87', '#005faf', '#005fd7', '#005fff', '#008700', '#00875f', '#008787', '#0087af', '#0087d7', '#0087ff', '#00af00', '#00af5f', '#00af87', '#00afaf', '#00afd7', '#00afff', '#00d700', '#00d75f', '#00d787', '#00d7af', '#00d7d7', '#00d7ff', '#00ff00', '#00ff5f', '#00ff87', '#00ffaf', '#00ffd7', '#00ffff', '#5f0000', '#5f005f', '#5f0087', '#5f00af', '#5f00d7', '#5f00ff', '#5f5f00', '#5f5f5f', '#5f5f87', '#5f5faf', '#5f5fd7', '#5f5fff', '#5f8700', '#5f875f', '#5f8787', '#5f87af', '#5f87d7', '#5f87ff', '#5faf00', '#5faf5f', '#5faf87', '#5fafaf', '#5fafd7', '#5fafff', '#5fd700', '#5fd75f', '#5fd787', '#5fd7af', '#5fd7d7', '#5fd7ff', '#5fff00', '#5fff5f', '#5fff87', '#5fffaf', '#5fffd7', '#5fffff', '#870000', '#87005f', '#870087', '#8700af', '#8700d7', '#8700ff', '#875f00', '#875f5f', '#875f87', '#875faf', '#875fd7', '#875fff', '#878700', '#87875f', '#878787', '#8787af', '#8787d7', '#8787ff', '#87af00', '#87af5f', '#7dae87', '#87afaf', '#87afd7', '#87afff', '#87d700', '#87d75f', '#87d787', '#87d7af', '#87d7d7', '#87d7ff', '#87ff00', '#87ff5f', '#87ff87', '#87ffaf', '#87ffd7', '#87ffff', '#af0000', '#af005f', '#af0087', '#af00af', '#af00d7', '#af00ff', '#af5f00', '#af5f5f', '#af5f87', '#af5faf', '#af5fd7', '#af5fff', '#af8700', '#af875f', '#af8787', '#af87af', '#af87d7', '#af87ff', '#afaf00', '#afaf5f', '#afaf87', '#afafaf', '#afafd7', '#afafff', '#afd700', '#afd75f', '#afd787', '#afd7af', '#afd7d7', '#afd7ff', '#afff00', '#afff5f', '#afff87', '#afffaf', '#afffd7', '#afffff', '#d70000', '#d7005f', '#d70087', '#d700af', '#d700d7', '#d700ff', '#d75f00', '#d75f5f', '#d75f87', '#d75faf', '#d75fd7', '#d75fff', '#d78700', '#d7875f', '#d78787', '#d787af', '#d787d7', '#d787ff', '#d7af00', '#d7af5f', '#d7af87', '#d7afaf', '#d7afd7', '#d7afff', '#d7d700', '#d7d75f', '#d7d787', '#d7d7af', '#d7d7d7', '#d7d7ff', '#d7ff00', '#d7ff5f', '#d7ff87', '#d7ffaf', '#d7ffd7', '#d7ffff', '#ff0000', '#ff005f', '#ff0087', '#ff00af', '#ff00d7', '#ff00ff', '#ff5f00', '#ff5f5f', '#ff5f87', '#ff5faf', '#ff5fd7', '#ff5fff', '#ff8700', '#ff875f', '#ff8787', '#ff87af', '#ff87d7', '#ff87ff', '#ffaf00', '#ffaf5f', '#ffaf87', '#ffafaf', '#f4aed7', '#ffafff', '#ffd700', '#ffd156', '#ffd787', '#ffd7af', '#ffd7d7', '#ffd7ff', '#ffff00', '#ffff5f', '#ffff87', '#ffffaf', '#ffffd7', '#ffffff', '#080808', '#121212', '#1c1c1c', '#262626', '#303030', '#3a3a3a', '#444444', '#4e4e4e', '#585858', '#626262', '#6c6c6c', '#767676', '#808080', '#8a8a8a', '#949494', '#9e9e9e', '#a8a8a8', '#b2b2b2', '#bcbcbc', '#c6c6c6', '#d0d0d0', '#dadada', '#e4e4e4', '#eeeeee']

# Function to resize the image while keeping the aspect ratio
def resize_image(image, new_width):
    # Calculate the new height to keep the aspect ratio
    aspect_ratio = image.shape[1] / float(image.shape[0])
    new_height = int(new_width / aspect_ratio)

    # Account for character aspect ratio (characters are taller than wide)
    # 0.7 to 0.9 (https://www.google.com/search?client=opera-gx&q=character+size+aspect+ratio&sourceid=opera&ie=UTF-8&oe=UTF-8)
    new_height = int(new_height * 0.5)  # This scales the height to be the right ratio for ASCII
    
    resized_image = cv2.resize(image, (new_width, new_height))
    return resized_image

def rgb_to_hex(r, g, b):
    return f"#{r:02x}{g:02x}{b:02x}"

def hex_to_rgb(hex_color):
    hex_color = hex_color.lstrip('#')
    return np.array([int(hex_color[i:i+2], 16) for i in (0, 2, 4)])

# Function to find the closest color from a list of hex values
def closest_hex(input_hex, hex_list):
    # Convert input hex to RGB
    r, g, b = int(input_hex[1:3], 16), int(input_hex[3:5], 16), int(input_hex[5:7], 16)
    
    closest_distance = float('inf')
    closest_color = None

    # Iterate over hex_list to find the closest hex color
    for hex_val in hex_list:
        # Convert hex to RGB
        rr, gg, bb = int(hex_val[1:3], 16), int(hex_val[3:5], 16), int(hex_val[5:7], 16)
        
        # Calculate the Euclidean distance between the input RGB and current RGB color
        distance = (r - rr) ** 2 + (g - gg) ** 2 + (b - bb) ** 2
        if distance < closest_distance:
            closest_distance = distance
            closest_color = hex_val

    return closest_color

# Function to map pixel intensity to an ASCII character
def pixel_to_ascii(pixel, color=False, prevPixelColor=-1):
    ascii_chars = '@%#*+=-:. '
    
    # Calculate grayscale using a weighted average for better human perception
    grayscale_value = int(0.299 * pixel[0] + 0.587 * pixel[1] + 0.114 * pixel[2])
    ascii_char = ascii_chars[int(grayscale_value / 32)]  # Map intensity to character
    
    ascii_char = '█'
    
    r, g, b = pixel
    hex_color = rgb_to_hex(r, g, b)

    # If color is enabled, find the closest color from the color list
    if color:
        closest_color = closest_hex(hex_color, ansi_colors)
        indexOfClosest = ansi_colors.index(closest_color)
        
        colorPrefix = "${c" + str(indexOfClosest) + "}"
        if prevPixelColor == indexOfClosest:
            colorPrefix = "" # OPTIMIZATION BABY
        
        hex_color = ansi_colors[indexOfClosest]
        colorPrefix = f"[{hex_color}]"
        
        return f"{colorPrefix}{ascii_char}", indexOfClosest
    else:
        return ascii_char, -1

# Main function to convert the image to ASCII art with color
def image_to_ascii(image_path, new_width=60, color=True, quantization=6):
    # Load the image with OpenCV (BGR format)
    image = cv2.imread(image_path)
    
    # Resize the image
    resized_image = resize_image(image, new_width)
    
    # quantized_image
    resized_image, centroids = reduce_colors(resized_image, quantization)
    
    # Initialize the ASCII art result string
    ascii_art = ''
    
    prevPixelColor = -1
    
    # Iterate over each pixel in the resized image
    for y in range(resized_image.shape[0]):
        for x in range(resized_image.shape[1]):
            pixel = resized_image[y, x]
            # Convert the pixel to ASCII and add it to the output
            pixelAscii, prevPixelColor = pixel_to_ascii(pixel, color=color, prevPixelColor=prevPixelColor)
            ascii_art += pixelAscii
        ascii_art += '\n'  # Newline after each row
    
    return ascii_art

# Function to reduce the image to a palette of n_colors
def reduce_colors(image, n_colors=16):
    # Convert the entire ANSI color palette from hex to RGB
    rgb_palette = np.array([hex_to_rgb(hex_color) for hex_color in ansi_colors])
    
    # Use k-means to find the 'n_colors' best representative colors
    kmeans = KMeans(n_clusters=n_colors, random_state=0).fit(rgb_palette)
    best_colors = kmeans.cluster_centers_.astype(int)

    # Reshape the image to a 2D array of pixels
    pixels = image.reshape((-1, 3))
    
    # Find the closest color in the palette for each pixel using pairwise distance
    labels = pairwise_distances_argmin_min(pixels, best_colors)[0]
    
    # Create a new image by mapping each pixel to its closest color in the palette
    new_image = best_colors[labels].reshape(image.shape)

    return new_image, best_colors

# Save the ASCII art to a text file
def save_ascii_art(ascii_art, output_file):
    colorPrefix = ""
    for i in range(0, 256):
        if i != 0: colorPrefix += " "
        colorPrefix += str(i)
    
    with open(output_file, 'w') as file:
        #file.write(colorPrefix + "\n")
        file.write(ascii_art)

# Run the conversion
image_path = "C:\\Users\\Weaver\\Downloads\\emotional_creature.png"  # Replace with your image path
output_file = "C:\\Users\\Weaver\\Downloads\\ascii_art.txt"  # The output text file

# Convert image to ASCII art with color
ascii_art = image_to_ascii(image_path, new_width=60, color=True, quantization=6)

# Regex reduce ascii
hex_color_pattern = r'#[0-9A-Fa-f]{3,6}\b'
import re
foundHexColors = re.findall(hex_color_pattern, ascii_art)
replacedHexColors = []
header = ""
for hexColor in foundHexColors:
    if hexColor in replacedHexColors: continue
    
    ansiNumber = ansi_colors.index(hexColor)
    ascii_art = ascii_art.replace(f"[{hexColor}]", "${c"+ str(len(replacedHexColors)+1) +"}")
    
    replacedHexColors.append(hexColor)
    header += f"{ansiNumber} "

print(header)

# Save the ASCII art to a file
save_ascii_art(ascii_art, output_file)

print(f"ASCII art saved to {output_file}")
