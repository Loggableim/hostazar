#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script to generate the hero image for the Redis Cache article.
Creates a 1200x630 PNG with:
- Dark violet background gradient
- Orange hex grid overlay
- Glowing data cable lines
- Terminal glow particles
- Gaussian blur + contrast for atmosphere
"""
import os
import random
from PIL import Image, ImageDraw, ImageFilter, ImageOps

# Constants
WIDTH, HEIGHT = 1200, 630
BACKGROUND_COLOR_START = (20, 0, 30)      # dark violet
BACKGROUND_COLOR_END = (30, 5, 50)        # slightly lighter violet
HEX_COLOR = (255, 152, 0)                 # orange
OUTPUT_PATH = "../images/redis-cache-vps-einrichten-2026.png"

def create_hex_grid(img, radius=10, spacing=20, offset_x=0, offset_y=0):
    """Draw an orange hex grid on the image."""
    draw = ImageDraw.Draw(img)
    for y in range(-HEIGHT, HEIGHT, spacing):
        for x in range(-WIDTH, WIDTH, spacing):
            cx = x + offset_x
            cy = y + offset_y
            # Generate hexagon points
            hex_points = []
            for i in range(6):
                angle = i * 60 * (3.14159 / 180)
                px = cx + radius * (2 * i / 6 - 1/3)
                py = cy + radius * (2 * i / 6) * (3**0.5)
                hex_points.append((px, py))
            draw.polygon(hex_points, outline=HEX_COLOR, width=1)
    return img

def add_glowing_cables(draw, img_width, img_height):
    """Add glowing data cable lines with multiple overlapping strokes to simulate glow."""
    num_cables = random.randint(3, 5)
    for _ in range(num_cables):
        start_x = random.randint(0, img_width)
        start_y = random.randint(0, img_height)
        end_x = random.randint(0, img_width)
        end_y = random.randint(0, img_height)
        # Draw multiple strokes with decreasing opacity to create glow effect
        for i in range(4):
            alpha = 0.8 - (i * 0.2)
            width = 6 - i * 1.2
            draw.line(
                (start_x, start_y, end_x, end_y),
                fill=(*HEX_COLOR, int(255 * alpha)),
                width=int(width)
            )

def add_terminal_particles(draw, img_width, img_height, num_particles=150):
    """Add small glowing particles reminiscent of terminal output."""
    for _ in range(num_particles):
        x = random.randint(0, img_width)
        y = random.randint(0, img_height)
        radius = random.randint(1, 3)
        r = random.randint(180, 255)
        g = random.randint(180, 255)
        b = random.randint(220, 255)
        color = (r, g, b)
        draw.ellipse(
            (x - radius, y - radius, x + radius, y + radius),
            fill=color + (int(255 * random.uniform(0.5, 0.9)),)
        )

def main():
    # Ensure output directory exists
    os.makedirs(os.path.dirname(OUTPUT_PATH), exist_ok=True)

    # Create base image with gradient background
    img = Image.new('RGBA', (WIDTH, HEIGHT), BACKGROUND_COLOR_START)
    # Create gradient overlay
    gradient = Image.new('RGBA', (WIDTH, HEIGHT))
    draw_gradient = ImageDraw.Draw(gradient)
    for i in range(WIDTH):
        ratio = i / WIDTH
        r = int(
            BACKGROUND_COLOR_START[0]
            + (BACKGROUND_COLOR_END[0] - BACKGROUND_COLOR_START[0]) * ratio
        )
        g = int(
            BACKGROUND_COLOR_START[1]
            + (BACKGROUND_COLOR_END[1] - BACKGROUND_COLOR_START[1]) * ratio
        )
        b = int(
            BACKGROUND_COLOR_START[2]
            + (BACKGROUND_COLOR_END[2] - BACKGROUND_COLOR_START[2]) * ratio
        )
        draw_gradient.line(
            [(i, 0), (i, HEIGHT)], fill=(r, g, b, 255)
        )
    img = Image.alpha_composite(img, gradient)

    # Create draw object for overlay
    draw = ImageDraw.Draw(img)

    # Add hex grid
    create_hex_grid(img)

    # Add glowing data cables
    add_glowing_cables(draw, WIDTH, HEIGHT)
    add_terminal_particles(draw, WIDTH, HEIGHT)

    # Apply Gaussian blur for atmospheric glow
    img = img.filter(ImageFilter.GaussianBlur(radius=1.5))

    # Convert to RGB (required for autocontrast)
    img = img.convert('RGB')
    img = ImageOps.autocontrast(img)

    # Save final image
    img.save(OUTPUT_PATH, format='PNG')
    print(f'Hero image saved to {OUTPUT_PATH}')

if __name__ == '__main__':
    main()