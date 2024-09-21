cmake_minimum_required(VERSION 3.15...3.27)
project(_glimshow_impl)

if(CMAKE_VERSION VERSION_LESS 3.18)
  set(DEV_MODULE Development)
else()
  set(DEV_MODULE Development.Module)
endif()

find_package(Python 3.8 COMPONENTS Interpreter ${DEV_MODULE} REQUIRED)

# c++17
set(CMAKE_CXX_STANDARD 17)


if(NOT CMAKE_BUILD_TYPE AND NOT CMAKE_CONFIGURATION_TYPES)
set(CMAKE_BUILD_TYPE Release CACHE STRING "Choose the type of build." FORCE)
set_property(CACHE CMAKE_BUILD_TYPE PROPERTY STRINGS "Debug" "Release" "MinSizeRel" "RelWithDebInfo")
endif()

# Detect the installed nanobind package and import it into CMake
execute_process(
  COMMAND "${Python_EXECUTABLE}" -m nanobind --cmake_dir
  OUTPUT_STRIP_TRAILING_WHITESPACE OUTPUT_VARIABLE NB_DIR)
  list(APPEND CMAKE_PREFIX_PATH "${NB_DIR}")
  find_package(nanobind CONFIG REQUIRED)
  
# source directory
set(SOURCE_DIR "${CMAKE_CURRENT_SOURCE_DIR}/glimshow/cpp")

# Compile extension module
nanobind_add_module(_glimshow_impl "${SOURCE_DIR}/binding.cpp" "${SOURCE_DIR}/gl_imshow.cpp" "${SOURCE_DIR}/glsl_program_wrapper.cpp")

# GLFW
# find_package(glfw3 REQUIRED)

# GLEW
# find_package(GLEW REQUIRED)

# OpenGL
find_package(OpenGL REQUIRED)

# Compile GLFW
set(GLFW_BUILD_EXAMPLES OFF CACHE BOOL " " FORCE)
set(GLFW_BUILD_TESTS OFF CACHE BOOL " " FORCE)
set(GLFW_BUILD_DOCS OFF CACHE BOOL " " FORCE)
set(GLFW_BUILD_INSTALL OFF CACHE BOOL " " FORCE)
set(GLFW_INSTALL OFF CACHE BOOL " " FORCE)
set(GLFW_USE_CHDIR OFF CACHE BOOL " " FORCE)

add_subdirectory("${CMAKE_CURRENT_SOURCE_DIR}/ext/glfw")
add_subdirectory("${CMAKE_CURRENT_SOURCE_DIR}/ext/glew-cmake")

# Link the library to the executable
target_link_libraries(_glimshow_impl PRIVATE glfw OpenGL::GL libglew_static)
