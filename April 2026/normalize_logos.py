#!/usr/bin/env python3
"""
Normalize logos to uniform dimensions with padding.
Creates centered logos in a consistent bounding box.
"""

from PIL import Image
import os

# Target uniform size for all logos
TARGET_WIDTH = 160
TARGET_HEIGHT = 80

# Background color (white) for padding
BG_COLOR = (255, 255, 255)

# Logos to process
LOGOS = [
    'logo_ffly4u.png',
    'logo_mobirider.png',
    'logo_intel.png',
    'logo_viettel.png',
    'logo_noema.png',
    'logo_freescale.png',
    'logo_motorola.png',
    'logo_nttdocomo.png',
]

def normalize_logo(input_path, output_path, target_w, target_h):
    """Load logo, center it in a uniform box with padding, save."""
    img = Image.open(input_path).convert('RGBA')
    
    # Calculate scaling to fit within target while preserving aspect ratio
    img_w, img_h = img.size
    scale = min(target_w / img_w, target_h / img_h)
    new_w = int(img_w * scale)
    new_h = int(img_h * scale)
    
    # Resize with high-quality resampling
    resized = img.resize((new_w, new_h), Image.Resampling.LANCZOS)
    
    # Create uniform canvas with white background
    canvas = Image.new('RGBA', (target_w, target_h), BG_COLOR)
    
    # Calculate centering offset
    offset_x = (target_w - new_w) // 2
    offset_y = (target_h - new_h) // 2
    
    # Paste resized logo onto canvas
    canvas.paste(resized, (offset_x, offset_y), resized)
    
    # Save as PNG
    canvas.save(output_path, 'PNG')
    print(f'Created {output_path} ({new_w}x{new_h} scaled, centered in {target_w}x{target_h})')

def main():
    for logo in LOGOS:
        if not os.path.exists(logo):
            print(f'WARNING: {logo} not found, skipping')
            continue
        
        # Output filename with _uniform suffix
        name, ext = os.path.splitext(logo)
        output_path = f'{name}_uniform.png'
        
        normalize_logo(logo, output_path, TARGET_WIDTH, TARGET_HEIGHT)

if __name__ == '__main__':
    main()
