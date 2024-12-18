import time
import numpy as np
import pyglimshow

# Initialize a window
screen = pyglimshow.FullScreen()

# Get the screen size
width = screen.width
height = screen.height
shape = screen.shape  # (height, width, 3)

print(f"Screen size: {width}x{height}")

# Create an image
# red -> x, green -> y, blue -> constant
img_rgb = np.fromfunction(lambda y, x, c: 128 * (c == 2) + x / (width - 1) * 255 * (c == 0) + y / (height - 1) * 255 * (c == 1), (height, width, 3)).astype(np.uint8)

# Display the image
screen.imshow(img_rgb)

# Do some tasks here
time.sleep(3)
