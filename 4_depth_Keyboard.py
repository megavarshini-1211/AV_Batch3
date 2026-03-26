import keyboard
import time
import cv2
from pal.products.qcar import QCar, QCarRealSense

# -------- INIT --------
myCar = QCar(readMode=1, frequency=10)
myCam = QCarRealSense(mode='RGB, Depth')

BASE_SPEED = 0.35   # tune for ~1 m/s

print("Controls:")
print("Arrow Keys → Move car")
print("Q → Quit")

try:
    while True:

        # -------- CONTROL --------
        throttle = 0.0
        steering = 0.0

        if keyboard.is_pressed('up'):
            throttle = BASE_SPEED

        if keyboard.is_pressed('down'):
            throttle = -BASE_SPEED

        if keyboard.is_pressed('left'):
            steering = 0.3

        if keyboard.is_pressed('right'):
            steering = -0.3

        # Send to car
        myCar.write(throttle, steering)

        # -------- READ CAR --------
        myCar.read()

        # -------- RGB CAMERA --------
        myCam.read_RGB()
        rgb_img = myCam.imageBufferRGB
        cv2.imshow('RGB View', rgb_img)

        # -------- DEPTH CAMERA --------
        myCam.read_depth()
        depth_img = myCam.imageBufferDepthPX

        # Normalize depth → 0–255
        depth_bw = cv2.normalize(depth_img, None, 0, 255, cv2.NORM_MINMAX)
        depth_bw = depth_bw.astype('uint8')

        # Color version (better visualization)
        depth_color = cv2.applyColorMap(depth_bw, cv2.COLORMAP_JET)

        cv2.imshow('Depth B/W', depth_bw)
        cv2.imshow('Depth Color', depth_color)

        # -------- DEBUG --------
        center_depth = depth_img[depth_img.shape[0]//2, depth_img.shape[1]//2]

        print(
            f"Tach: {myCar.motorTach:.2f} | "
            f"Throttle: {throttle:.2f} | Steering: {steering:.2f} | "
            f"Center Depth: {center_depth}"
        )

        # -------- EXIT --------
        if cv2.waitKey(1) & 0xFF == ord('q'):
            print("\nStopped by user (Q pressed)")
            break

        time.sleep(0.05)

except KeyboardInterrupt:
    print("\nStopped by CTRL+C")

finally:
    myCar.write(0, 0)
    cv2.destroyAllWindows()
