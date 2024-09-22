#include <iostream>
#include <chrono>
#include <algorithm>
#include <string>
#include <GL/glew.h>
#include <GLFW/glfw3.h>
#include "gl_imshow.hpp"

#include <nanobind/nanobind.h>
#include <nanobind/ndarray.h>
#include <nanobind/stl/tuple.h>

namespace nb = nanobind;
using namespace nb::literals;

class FullScreen
{
private:
    size_t width = 0;
    size_t height = 0;
    GLFWwindow *window = nullptr;
    GL2dImagePanel *imgPanel = nullptr;

public:
    FullScreen()
    {
        // Initialize GLFW
        if (!glfwInit())
        {
            throw std::runtime_error("Failed to initialize GLFW");
        }

        // Terminate GLFW on exit
        atexit(glfwTerminate);

        // Set up GLFW window for full screen
        glfwWindowHint(GLFW_AUTO_ICONIFY, GL_FALSE);
        glfwWindowHint(GLFW_RESIZABLE, GLFW_FALSE);

        // Get monitor
        GLFWmonitor *primaryMonitor = glfwGetPrimaryMonitor();
        const GLFWvidmode *mode = glfwGetVideoMode(primaryMonitor);
        width = mode->width;
        height = mode->height;

        // Create a window
        window = glfwCreateWindow(width, height, "pyglimshow", primaryMonitor, NULL);

        if (window == NULL)
        {
            glfwTerminate();
            throw std::runtime_error("Failed to create GLFW window");
        }

        // Make the window's context current
        glfwMakeContextCurrent(window);

        // Initialize GLEW
        glewExperimental = GL_TRUE;
        if (glewInit() != GLEW_OK)
        {
            throw std::runtime_error("Failed to initialize GLEW");
        }

        // Hide mouse cursor
        glfwSetInputMode(window, GLFW_CURSOR, GLFW_CURSOR_HIDDEN);

        // Enable v-sync
        glfwSwapInterval(1);

        // Create GL2dImagePanel
        imgPanel = new GL2dImagePanel(width, height);
        imgPanel->init();

        // Set gray background
        glClearColor(0.5f, 0.5f, 0.5f, 0.0f);
        glClear(GL_COLOR_BUFFER_BIT);
        glfwSwapBuffers(window);
        glfwPollEvents();
        glViewport(0, 0, width, height);

        uint8_t *data = new uint8_t[width * height * 3];
        std::fill(data, data + width * height * 3, 128);
        for (int i = 0; i < 32; i++)
        {
            imgPanel->updateImage(data);
            imgPanel->draw();
            glfwSwapBuffers(window);
            glfwPollEvents();
        }
        delete[] data;
    }

    ~FullScreen()
    {
        delete imgPanel;
        glfwTerminate();
    }

    void set_next(const nb::ndarray<const uint8_t, nb::shape<-1, -1, 3>, nb::device::cpu, nb::c_contig> &img)
    {
        if (img.shape(0) != height || img.shape(1) != width)
        {
            throw std::runtime_error("Invalid image size! Expected: " + std::to_string(height) + "x" + std::to_string(width) + ", got: " + std::to_string(img.shape(0)) + "x" + std::to_string(img.shape(1)));
        }
        imgPanel->updateImage(img.data());
        imgPanel->draw();
    }

    void swap_buffers()
    {
        glfwSwapBuffers(window);
        glfwPollEvents();
    }

    void imshow(const nb::ndarray<const uint8_t, nb::shape<-1, -1, 3>, nb::device::cpu, nb::c_contig> &img)
    {
        set_next(img);
        swap_buffers();
    }

    size_t get_width() const
    {
        return width;
    }

    size_t get_height() const
    {
        return height;
    }

    // bool shouldClose()
    // {
    //     return !glfwWindowShouldClose(window);
    // }
};

NB_MODULE(_pyglimshow_impl, m)
{
    // m.def("add", [](int a, int b)
    //       { return a + b; });

    nb::class_<FullScreen>(m, "FullScreen")
        .def(nb::init<>())
        .def("imshow", &FullScreen::imshow)
        .def("swap_buffers", &FullScreen::swap_buffers)
        .def("set_next", &FullScreen::set_next)
        .def_prop_ro("width", &FullScreen::get_width)
        .def_prop_ro("height", &FullScreen::get_height)
        .def_prop_ro("shape", [](const FullScreen &self)
                     { return std::make_tuple(self.get_height(), self.get_width(), 3); });
}