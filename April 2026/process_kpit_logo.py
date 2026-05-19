from PIL import Image

# Open the source image
img = Image.open('logo_kpit.jpg')

# Create a new image with RGBA mode (transparent support)
background = Image.new('RGBA', img.size, (255, 255, 255, 255))

# If image has transparency, paste it properly
if img.mode == 'RGBA':
    background.paste(img, (0, 0), img)
else:
    background.paste(img, (0, 0))

# Get image dimensions
width, height = background.size

# Find the content bounds by scanning for non-white pixels
# White is (255, 255, 255) - we'll find the bounding box of content
pixels = background.load()
rmin, rmax = height, 0
cmin, cmax = width, 0

# Scan all pixels to find non-white content
for y in range(height):
    for x in range(width):
        r, g, b, a = pixels[x, y]
        # Check if pixel is not white (allowing some tolerance)
        if not (r > 250 and g > 250 and b > 250):
            if y < rmin: rmin = y
            if y > rmax: rmax = y
            if x < cmin: cmin = x
            if x > cmax: cmax = x

# Add padding
padding = 5
rmin = max(0, rmin - padding)
rmax = min(height, rmax + padding)
cmin = max(0, cmin - padding)
cmax = min(width, cmax + padding)

# Crop to content + padding
cropped = background.crop((cmin, rmin, cmax, rmax))

# Get the content size
content_width, content_height = cropped.size

print(f"Content bounds: {cmin}, {rmin} to {cmax}, {rmax}")
print(f"Content size: {content_width}x{content_height}")

# Create the final logo with appropriate size
# Target height of 60px to match other logos (which are h-6 = 24px * 2.5 = ~60px scaled)
target_height = 60
aspect_ratio = content_width / content_height
target_width = int(target_height * aspect_ratio)

# Resize the cropped image
resized = cropped.resize((target_width, target_height), Image.LANCZOS)

# Create the final image with transparent background
final_img = Image.new('RGBA', (target_width, target_height), (0, 0, 0, 0))
final_img.paste(resized, (0, 0))

# Save as PNG with transparency
final_img.save('logo_kpit_uniform.png', 'PNG')

print(f"Created logo_kpit_uniform.png: {final_img.size} pixels")
