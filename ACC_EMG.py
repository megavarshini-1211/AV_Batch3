import keyboard
import time
import numpy as np
from pal.products.qcar import QCar, QCarRealSense

# -------- INIT --------
myCar = QCar(readMode=1, frequency=20)   # increased frequency
myCam = QCarRealSense(mode='Depth')      # ONLY depth (faster)

BASE_SPEED = 0.35

STOP_DISTANCE = 25
SLOW_DISTANCE = 35

print("ADAS ACTIVE 🚨 (FAST MODE)")
print("Arrow Keys → Move | CTRL+C → Quit")

try:
    while True:

        throttle = 0.0
        steering = 0.0

        # -------- READ DEPTH --------
        myCam.read_depth()
        depth_img = myCam.imageBufferDepthPX

        # Fix shape if needed
        if len(depth_img.shape) == 3:
            depth_img = depth_img[:, :, 0]

        h, w = depth_img.shape

        center_region = depth_img[h//2-10:h//2+10, w//2-10:w//2+10]
        center_depth = float(np.mean(center_region))

        # -------- CONTROL --------
        if keyboard.is_pressed('up'):
            throttle = BASE_SPEED

        if keyboard.is_pressed('down'):
            throttle = -BASE_SPEED

        if keyboard.is_pressed('left'):
            steering = 0.3

        if keyboard.is_pressed('right'):
            steering = -0.3

        # -------- ADAS --------
        if center_depth <= STOP_DISTANCE and throttle > 0:
            throttle = 0
            print("🚨 BRAKE")

        elif center_depth <= SLOW_DISTANCE and throttle > 0:
            throttle = BASE_SPEED * 0.3
            print("⚠️ SLOW")

        # -------- SEND --------
        myCar.write(throttle, steering)
        myCar.read()

        print(
            f"Depth: {center_depth:.2f} | "
            f"Throttle: {throttle:.2f}"
        )

        time.sleep(0.02)   # faster loop

except KeyboardInterrupt:
    print("Stopped")

finally:
    myCar.write(0, 0)
