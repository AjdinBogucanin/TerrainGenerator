import math
import random

def fade(t):
    return t * t * t * (t * (t * 6 - 15) + 10)

def lerp(t, a, b):
    return a + t * (b - a)

def grad(hash, x, y):
    h = hash & 15
    u = x if h < 8 else y
    v = y if h < 8 else x
    if h & 1:
        u = -u
    if h & 2:
        v = -v
    return u + v

def perlin(x, y):
    X = int(x) & 255
    Y = int(y) & 255
    x -= int(x)
    y -= int(y)
    u = fade(x)
    v = fade(y)
    A = (p[X] + Y) & 255
    B = (p[X + 1] + Y) & 255

    return lerp(
        v,
        lerp(
            u,
            grad(p[A], x, y),
            grad(p[B], x - 1, y),
        ),
        lerp(
            u,
            grad(p[A + 1], x, y - 1),
            grad(p[B + 1], x - 1, y - 1),
        ),
    )

# Generate a random seed or set a fixed seed value
seed = random.randint(0, 1000)  # Generate a random seed
print("seed: "+ str(seed))
# seed = 42  # Use a fixed seed value

# Set the seed for the random number generator
random.seed(seed)

p = list(range(512))
random = random.Random()
random.shuffle(p)
p.extend(p)

def generate_perlin_noise(width, height, scale, octaves, persistence):
    noise_map = [[0.0 for _ in range(height)] for _ in range(width)]
    for i in range(width):
        for j in range(height):
            x = i / scale
            y = j / scale
            value = 0
            amplitude = 1
            frequency = 1
            for _ in range(octaves):
                value += perlin(x * frequency, y * frequency) * amplitude
                amplitude *= persistence
                frequency *= 2
            noise_map[i][j] = value
    return noise_map
