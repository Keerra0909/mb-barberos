from PIL import Image

# Open image
img = Image.open('logo.png').convert('RGB')
w, h = img.size

# Find bounding box of non-background pixels
min_x, min_y, max_x, max_y = w, h, 0, 0
bg_thresh = 15  # Pixels brighter than 15 in any channel are "content"

for y in range(h):
    for x in range(w):
        r, g, b = img.getpixel((x, y))
        if r > bg_thresh or g > bg_thresh or b > bg_thresh:
            if x < min_x: min_x = x
            if x > max_x: max_x = x
            if y < min_y: min_y = y
            if y > max_y: max_y = y

print(f"Content bounding box: ({min_x}, {min_y}) to ({max_x}, {max_y})")

# Calculate how off-center it is
content_w = max_x - min_x
content_center = min_x + content_w / 2
image_center = w / 2

print(f"Content center: {content_center}, Image center: {image_center}")

# Let's crop it symmetrically so the center of the content becomes the center of the image
# Actually, just cropping it to exactly the bounding box is perfect!
# Then the CSS `object-contain` will naturally center the cropped image.
cropped = img.crop((min_x, min_y, max_x + 1, max_y + 1))
cropped.save('logo_cropped.png')
print("Saved logo_cropped.png")
