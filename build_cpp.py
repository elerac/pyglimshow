import argparse
import subprocess
import os
import shutil
from nanobind.stubgen import StubGen


def green_print(msg):
    print("\033[92m" + msg + "\033[0m")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", type=str, default="Release", help="Configuration type")
    args = parser.parse_args()

    # Build nanobind module
    # Remove build directory
    shutil.rmtree("build", ignore_errors=True)

    # Run cmake and build
    ret1 = subprocess.run(["cmake", "-S", ".", "-B", "build"], shell=True)
    ret2 = subprocess.run(["cmake", "--build", "build", "--config", args.config], shell=True)
    if ret1.returncode != 0 or ret2.returncode != 0:
        raise Exception("Failed to build nanobind module")
    green_print("Finished building nanobind module")

    # In windows, copy the built module
    # and rename Debug to _glimshow_impl
    if os.name == "nt":
        src = f"build/{args.config}"
        dst = "glimshow/_glimshow_impl"
        if os.path.exists(dst):
            shutil.rmtree(dst)
        shutil.copytree(src, dst)
    else:
        raise

    # Generate __init__.py
    with open("glimshow/_glimshow_impl/__init__.py", "w") as f:
        f.write("from ._glimshow_impl import *")

    green_print(f"Moved {src} to {dst}, and generated __init__.py")

    # Generate pyi file
    import glimshow

    module = glimshow._glimshow_impl._glimshow_impl
    sg = StubGen(module)
    sg.put(module)
    pyi = sg.get()
    with open("glimshow/_glimshow_impl/__init__.pyi", "w") as f:
        f.write(pyi)

    green_print("Generated pyi file")

    green_print("Successfully built nanobind module")


if __name__ == "__main__":
    main()
