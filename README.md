# GL imshow in Python

This repository provides programs to display images in Python via OpenGL. The main purpose is for structured light illumination, particularly for nearly synchronized image capturing in projector-camera or display-camera systems.

The core rendering program is borrowed from [kamino410/gl_imshow](https://github.com/kamino410/gl_imshow) developed by [Takumi Kaminokado](https://kamino410.github.io/). I have modified the original C++ code and bound it to Python using nanobind. I acknowledge and respect his pioneering work.

## Installation

You first need to clone this repository.

```shell
git clone --recursive-submodules https://github.com/elerac/pyglimshow.git
```

To build the C++ extension, you need to prepare the build environment of OpenGL through cmake. GLFW and GLEW are downloaded as submodules. As a Python environment, you need to prepare [nanobind](https://github.com/wjakob/nanobind).

This repository includes a script to build the C++ code. You can build the code by running the following command.

```shell
python build_cpp.py
```

The built binary is saved to the `pyglimshow/` directory, and you can import the Python module using the following code.

```python
import pyglimshow
```

Once the compilation is complete, you can relocate the `pyglimshow/` directory to your working directory.

## Usage

The following code is a simple example of showing the image on fullscreen.

```python
import time
import numpy as np
import pyglimshow

# Initialize a window
screen = pyglimshow.FullScreen()

# Get the screen size
width = screen.width
height = screen.height

# Create an image
img_rgb = np.fromfunction(lambda y, x, c: 255 * (c == 0) + x / (width - 1) * 255 * (c == 1) + y / (height - 1) * 255 * (c == 2), (height, width, 3)).astype(np.uint8)

# Display the image
screen.imshow(img_rgb)

# Do some tasks here
time.sleep(3)
```

The "imshow" method calls the ["glfwSwapBuffers"](https://www.glfw.org/docs/3.0/group__context.html#ga15a5a1ee5b3c2ca6b15ca209a12efd14) function, which swaps the image and waits for the swap using vsync. This ensures that the image is changed after the "imshow" method is finished. However, I have found that vsync does not always work properly on my Windows, which may be a limitation of GLFW. I'll discuss this issue for procam synchronization capture in the next section.

If you are working on time-sensitive tasks, uploading and rendering a large image may be crucial. You can use "set_next"and "swap_buffers" methods instead of "imshow".

```python
# Upload and draw the image before showing.
# The image is not displayed in this line.
screen.set_next(img_rgb)

# Swap the image that is set at the previous line.
# The image will be displayed after this line.
screen.swap_buffers()
```

