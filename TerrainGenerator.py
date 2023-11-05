import tkinter as tk
from perlin_noise import generate_perlin_noise
import pygame
import random
from collections import Counter
import numpy as np 


# Rules for better land formation
RULES_LAND_AND_WATER = {
    0: [1, 2, 3, 4, 5, 6, 7, 8],
    1: [1, 2, 3, 6],  # Green
    2: [1, 2],  # Dark Green
    3: [1, 3, 4],  # Yellow
    4: [3, 4, 5],  # Blue
    5: [4, 5],  # Deep Blue
    6: [6, 7, 1],  # rocky island bottom
    7: [6, 7, 8],  # rocky island
    8: [7, 8],  # rocky island peek,
    "tiles_collection": {0: ["black", (0, 0, 0)], 1: ["green", (0, 255, 0)],
                         2: ["dark green", (0, 125, 0)], 3: ["yellow", (255, 255, 0)],
                         4: ["blue", (0, 25, 255)], 5: ["deep blue", (0, 0, 100)], 6: ["rocky island bottom", (65, 65, 100)],
                         7: ["rocky island", (35, 35, 60)], 8: ["rocky island peek", (255, 255, 255)]
                         }}

# Rules for better Island formation and water bodies
RULES_ISLANDS = {
    0: [1, 2, 3, 4, 5, 6, 7, 8],
    1: [1, 2],  # Green
    2: [1, 2],  # Dark Green
    3: [3, 4],  # Yellow
    4: [4, 5],  # Blue
    5: [4, 5],  # Deep Blue
    6: [6, 7],  # rocky island bottom
    7: [6, 7, 8],  # rocky island
    8: [7, 8],  # rocky island peek,
    "tiles_collection": {0: ["black", (0, 0, 0)], 1: ["green", (0, 255, 0)],
                         2: ["dark green", (0, 125, 0)], 3: ["yellow", (255, 255, 0)],
                         4: ["blue", (0, 25, 255)], 5: ["deep blue", (0, 0, 100)], 6: ["rocky island bottom", (65, 65, 100)],
                         7: ["rocky island", (35, 35, 60)], 8: ["rocky island peek", (255, 255, 255)]
                         }}

# Rules for better Island formation and water bodies with NO PERLIN
RULES_NO_PERLIN = {
    0: [1, 2, 3, 4, 5, 6, 7, 8],
    1: [1, 2, 3, 6],  # Green
    2: [1, 2],  # Dark Green
    3: [1, 3, 4],  # Yellow
    4: [3, 4, 5],  # Blue
    5: [4, 5],  # Deep Blue
    6: [6, 7, 1],  # rocky island bottom
    7: [6, 7, 8],  # rocky island
    8: [7, 8],  # rocky island peek,
    "tiles_collection": {0: ["black", (0, 0, 0)], 1: ["green", (0, 255, 0)],
                         2: ["dark green", (0, 125, 0)], 3: ["yellow", (255, 255, 0)],
                         4: ["blue", (0, 25, 255)], 5: ["deep blue", (0, 0, 100)], 6: ["rocky island bottom", (65, 65, 100)],
                         7: ["rocky island", (35, 35, 60)], 8: ["rocky island peek", (255, 255, 255)]
                         }}
# Rules for Land Only
RULES_LAND_ONLY = {
    0: [1, 2, 3, 4, 5],
    1: [1, 2, 3, 6],  # Green
    2: [1, 2],  # Dark Green
    3: [6, 7, 1],  # rocky island bottom
    4: [6, 7, 8],  # rocky island
    5: [7, 8],  # rocky island peek,
    "tiles_collection": {0: ["black", (0, 0, 0)], 1: ["green", (0, 255, 0)],
                         2: ["dark green", (0, 125, 0)], 3: ["rocky island bottom", (65, 65, 100)],
                         4: ["rocky island", (35, 35, 60)], 5: ["rocky island peek", (255, 255, 255)]
                         }}


def neighbor_rules_subset(x, y, img_array, RULES):
    rules_list = [
        RULES[img_array[x][y + 1]],
        RULES[img_array[x][y - 1]],
        RULES[img_array[x + 1][y]],
        RULES[img_array[x - 1][y]],
        RULES[img_array[x + 1][y + 1]],
        RULES[img_array[x + 1][y - 1]],
        RULES[img_array[x - 1][y + 1]],
        RULES[img_array[x - 1][y - 1]],
    ]

    # Calculate the intersection of rules using Counter
    intersection = Counter(rules_list[0])
    for i in range(1, len(rules_list)):
        intersection &= Counter(rules_list[i])

    # Convert the intersection back to a list of rules
    intersection_list = list(intersection.elements())

    return intersection_list

def apply_rules(random_array, rules):
    for i in range(len(random_array)):
        for j in range(len(random_array[i])):
            try:
                random_array[i][j] = random.choice(neighbor_rules_subset(i, j, random_array, rules))
            except:
                pass
    return random_array

def generate_terrain():
    # Get parameters from the GUI
    scale = int(scale_entry.get())
    octaves = int(octaves_entry.get())
    persistence = float(persistence_entry.get())
    rule_set = rule_set_var.get()
    cell_size = int(cell_size_entry.get())
    rows = int(rows_entry.get())
    cols = int(cols_entry.get())
    width = cols
    height = rows



    # Pick the selected rule set
    if rule_set == "Land and Water":
        picked_rules = RULES_LAND_AND_WATER
    elif rule_set == "Islands":
        picked_rules = RULES_ISLANDS
    elif rule_set == "No Perlin":
        picked_rules = RULES_NO_PERLIN
    elif rule_set == "Land Only":
        picked_rules = RULES_LAND_ONLY

    collection_size = len(picked_rules["tiles_collection"])
    tiles = picked_rules["tiles_collection"]
    


    if (rule_set != "No Perlin"):
        # Generate Perlin noise
        perlin_noise = generate_perlin_noise(width, height, scale, octaves, persistence)

        # Normalize the Perlin noise to the range [0, 1] and map it to the values 0-8
        min_value = min(map(min, perlin_noise))
        max_value = max(map(max, perlin_noise))

        normalized_perlin_noise = [
            [int((collection_size - 1) * (value - min_value) / (max_value - min_value)) for value in row]
            for row in perlin_noise]

        random_array = normalized_perlin_noise
    else:
        random_array = np.zeros((rows, cols))

    random_array = apply_rules(random_array, picked_rules)

    # Create a list of color values based on the values in random_array
    #color_values = [[tiles[value][1] for value in row] for row in random_array]
    # Create color_values with the correct dimensions
    color_values = [[(0, 0, 0) for _ in range(cols)] for _ in range(rows)]
    

    # Update color_values using the values from random_array and the tiles dictionary
    for row in range(rows):
        for col in range(cols):
            value = random_array[row][col]
            if value in tiles:
                color_values[row][col] = tiles[value][1]
            else:
                # Handle the case when the value is not in the tiles dictionary
                color_values[row][col] = (0, 0, 0)  # You can set a default color or handle it differently


    # Define the dimensions
    screen_width = cell_size * cols
    screen_height = cell_size * rows

    # Create a Pygame window
    screen = pygame.display.set_mode((screen_width, screen_height))

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        for row in range(rows):
            for col in range(cols):
                cell_color = color_values[row][col]
                pygame.draw.rect(
                    screen,
                    cell_color,
                    (col * cell_size, row * cell_size, cell_size, cell_size)
                )

        pygame.display.flip()

# Create the main tkinter window
root = tk.Tk()
root.title("Terrain Generator")

# Create GUI elements
scale_label = tk.Label(root, text="Scale:")
scale_label.pack()
scale_entry = tk.Entry(root)
scale_entry.pack()

octaves_label = tk.Label(root, text="Octaves:")
octaves_label.pack()
octaves_entry = tk.Entry(root)
octaves_entry.pack()

persistence_label = tk.Label(root, text="Persistence:")
persistence_label.pack()
persistence_entry = tk.Entry(root)
persistence_entry.pack()

rule_set_label = tk.Label(root, text="Rule Set:")
rule_set_label.pack()

rule_set_var = tk.StringVar()
rule_set_var.set("Islands")
rule_set_options = ["Land and Water", "Islands", "No Perlin", "Land Only"]
rule_set_menu = tk.OptionMenu(root, rule_set_var, *rule_set_options)
rule_set_menu.pack()

cell_size_label = tk.Label(root, text="Cell Size:")
cell_size_label.pack()
cell_size_entry = tk.Entry(root)
cell_size_entry.pack()

rows_label = tk.Label(root, text="Rows:")
rows_label.pack()
rows_entry = tk.Entry(root)
rows_entry.pack()

cols_label = tk.Label(root, text="Columns:")
cols_label.pack()
cols_entry = tk.Entry(root)
cols_entry.pack()

generate_button = tk.Button(root, text="Generate Terrain", command=generate_terrain)
generate_button.pack()

root.mainloop()
