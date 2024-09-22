import os
import time
import shutil
import concurrent.futures
import numpy as np
import cv2
import EasyPySpin
import pyglimshow
import pyglimshow.helper


def main():
    cap = EasyPySpin.VideoCapture(0)
    cap.set(cv2.CAP_PROP_EXPOSURE, 1 / 480 * 1e6)
    cap.set(cv2.CAP_PROP_GAIN, 15)
    cap.set_pyspin_value("TriggerMode", "On")

    num_main_images = 120
    num_dummy_images = 30

    dir_dst = "captured"

    screen = pyglimshow.FullScreen()
    width = screen.width
    height = screen.height
    shape = screen.shape  # (height, width, 3)

    # Create a list of images to display
    image_list_dummy = [np.full(shape, 128, dtype=np.uint8) for _ in range(num_dummy_images)]
    image_list_dummy = [np.full(shape, 128, dtype=np.uint8) for _ in range(num_dummy_images)]
    image_list_main = [pyglimshow.helper.create_number_image(shape, i) for i in range(num_main_images)]
    image_list = image_list_dummy + image_list_main + image_list_dummy

    # Start capturing
    print("Start capturing")
    image_list_captured = []
    cap.cam.BeginAcquisition()
    screen.set_next(image_list[0])
    time_start_capture = time.time()
    for i in range(len(image_list)):
        time_strat = time.time()

        # Simple way
        # screen.imshow(image_list[i])
        # ret, frame = cap.read()

        # Advanced way using swap_buffers and set_next
        screen.swap_buffers()
        time.sleep(0.001)

        cap.cam.TriggerSoftware.Execute()
        with concurrent.futures.ThreadPoolExecutor() as executor:
            future = executor.submit(cap.read)

        if i < len(image_list) - 1:
            screen.set_next(image_list[i + 1])

        ret, frame = future.result()

        image_list_captured.append(frame)

        time_end = time.time()
        elapsed = time_end - time_strat
        fps = 1 / (elapsed + 1e-10)
        print(f"{i} fps: {fps:.2f}")
    # End capturing
    time_end_capture = time.time()
    print("End capturing")
    print(f"Capture time: {time_end_capture - time_start_capture:.2f} s")

    # End acquisition and restore trigger mode
    cap.cam.EndAcquisition()
    cap.set_pyspin_value("TriggerMode", "Off")

    # Export captured images
    shutil.rmtree(dir_dst, ignore_errors=True)
    os.makedirs(dir_dst, exist_ok=True)
    for i, img in enumerate(image_list_captured):
        img = cv2.cvtColor(img, cv2.COLOR_BayerRG2BGR)
        cv2.imwrite(f"{dir_dst}/img_{i}.png", img)


if __name__ == "__main__":
    main()
