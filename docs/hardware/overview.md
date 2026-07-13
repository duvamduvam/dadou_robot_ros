# Hardware Overview

## Physical Specification
- Weight: ~50 kg wood & metal frame
- Mobility: two driven wheels, stabilised by the controller commands
- Upper body: two arms (no hands) with servo actuation
- Head: LED strips for eyes and a removable LED mouth
- Power: ensure the battery/PSU setup is documented in the operations sheet (add details as they evolve)

## Sensors & Inputs
- Serial-connected glove (RP2040) that translates performer gestures
- Optional onboard sensors (I2C accelerometer, etc.) configured through `robot_config.py`

## Vision & camera

### In service: USB webcam
A USB UVC webcam (Jieli chipset) is head-mounted and driven from the **vision Raspberry Pi 5**
(see `../dadou_vision_ros`), captured by OpenCV at 640×480 MJPG in `person_tracker_node.py`.
Three properties are load-bearing and must be known before anyone swaps it out:

- **It caps at 16.7 fps** while MediaPipe only burns 24 % of the CPU. The camera — not the
  compute — is the bottleneck of the perception loop.
- **It is also the microphone.** ALSA alias `casque_mic` → card U20, declared in the vision
  Pi's `/etc/asound.conf`. `chat_node` V2 depends on it. Replacing the webcam with a CSI
  module therefore *requires* buying a separate USB microphone — this is not a like-for-like swap.
- **Its auto-exposure converges slowly** (hence the 15 warm-up frames in `photo-camera.sh`);
  it already falsified the LED face calibration once.

### Evaluated 2026-07-13, not purchased: CSI camera (IMX219 130°)

Candidate module: **IMX219 8 MP, 130° FOV, MINI CSI (22-pin), 15 cm FFC — €9.39**
<https://fr.aliexpress.com/item/1005006912887641.html>

Selection criteria (use these to re-pick if the listing dies — stock was low):

| Criterion | Why it matters here |
| --- | --- |
| **IMX219**, not OV5647 | Sensor of the official Camera Module v2: first-class libcamera support (`dtoverlay=imx219`), and clearly better in low light than the 2013-era OV5647. |
| **22-pin "mini CSI" / "for Pi 5"** | The Pi 5 uses the narrow 22-pin connector. A 15-pin Pi 4 module additionally needs a 15→22 adapter cable. |
| **No IR LEDs / no "night vision"** | Those modules are **NoIR** — no IR-cut filter — which washes colours out to pink under stage light and degrades the very image MediaPipe consumes. Didier never plays in the dark; night vision is a defect here, not a feature. |
| **~130° FOV** | 77° ≈ the current webcam (no gain). 160–200° fisheye distorts so hard that `person_follower`'s bounding-box→heading mapping stops being linear. |

Open points, to settle **before** any purchase or migration:

- **Ribbon length.** Modules ship with ~15 cm; head-to-body needs an official Raspberry Pi 5
  camera cable (200 / 300 / 500 mm). Check which connector the camera board itself carries —
  these boards are often 15-pin on the camera side and 22-pin on the Pi side, which is exactly
  what the official Pi 5 cables are.
- **Mechanics — the strongest argument for staying on USB.** An FPC ribbon is not designed for
  repeated flexing, and it would cross the *moving neck joint* (gaze pans the head). A USB cable
  with strain relief survives that; a ribbon fatigues and cracks.
- **Software cost is the real price, not the €9.** `cv2.VideoCapture` cannot see a CSI camera on
  Pi 5 / Bookworm — no legacy V4L2 path. It requires libcamera (Picamera2, or the `camera_ros`
  ROS 2 node) **inside the vision Docker container**, with the libcamera stack and tuning files
  baked into the image.
- **Distortion.** Even at 130° there is barrel distortion: a person at the frame edge reads as
  "less off-centre" than they are. The box→heading gain must be **re-checked under the camera
  protocol**, never assumed.
- **Two cameras are possible.** The Pi 5 has two CSI/DSI connectors, both usable as cameras at
  once (`cam0` / `cam1`; libcamera can even software-sync their frames). Use case not decided —
  stereo depth would be a project of its own (calibration + rectification), whereas wide+narrow
  or front+rear is realistic. It doubles the ISP/CPU load on a Pi 5 that will also carry whisper
  and piper in V2.

## Devices
All motors are driven by an I2C PCA9685 PWM board attached to the Raspberry Pi 4, reducing wiring complexity and electrical load on the Pi.
![PCA9685 PWM driver](../../docs/pictures/consumable-parts/PCA9685.png)
*PCA9685 PWM driver board used for the robot actuators.*

The I2C signal from the Pi is isolated with an ISO1540 STEMMA bidirectional isolator to protect the main board.
![I2C isolator](../../docs/pictures/consumable-parts/i2c-isolator.png)
*ISO1540 I2C isolator between the Raspberry Pi and the actuator bus.*

### Wheels differential drive
![Wheel system](../../docs/pictures/wheel-motor.jpg)
*Wheel assemblies and mounting hardware.*

The PWM signal feeds a Cytron SmartDrive 40 A motor driver (10–45 V) that powers the wheel motors.
![Cytron SmartDrive motor driver](../../docs/pictures/consumable-parts/smartdrive.png)
*Cytron SmartDrive DC motor driver.*

Each wheel uses a 250 W brushless cycle motor.
![Brushless cycle motor](../../docs/pictures/consumable-parts/brushless-motor.png)
*Brushless 250 W wheel motor.*

### Arms, eyes and mouth servos
The arms and mouth are controlled by ASME-MR 380 kg·cm continuous-rotation RC servos.
![ASME-MR servo](../../docs/pictures/consumable-parts/arm-motor.png)
*ASME-MR high-torque servo for arms and mouth.*

The eyes use a JX Servo CLS-12V7346 (46 kg·cm, 12 V).
![JX CLS-12V servo](../../docs/pictures/consumable-parts/servo-cls-12V.png)
*JX CLS-12V7346 servo dedicated to the eyes.*

### Power supply
The battery pack is built from 18650 cells rated at 40 C (8×5 configuration, capacity to be confirmed).

A Daly Smart BMS (Li-ion, 7S/8S/16S capable) manages charging and 24 V output for the high-power domain.
![Daly BMS](../../docs/pictures/consumable-parts/bms-24V-30A.png)
*Daly Smart BMS supervising the main battery pack.*

12 V is generated by a Mean Well SD-50B-24 DC/DC converter.
![12 V converter](../../docs/pictures/consumable-parts/convertisseur.png)
*Mean Well SD-50B-24 converter producing the 12 V rail.*

5 V is generated by a second Mean Well SD-50B-24 configured for 5 V output.
![5 V converter](../../docs/pictures/consumable-parts/convertisseur.png)
*Mean Well SD-50B-24 converter producing the 5 V rail.*

## Electronics board
Document diagrams, pinouts, and maintenance procedures here. Include photos or links under `docs/hardware/assets/` as they become available.
The main distribution board interfaces the Raspberry Pi with the PWM drivers, LED strips, and matrix through 74AHCT125 level shifters.
![Main distribution board](../../docs/pictures/main-board.jpg)
*Main electronics board mounted inside the robot.*

![Main board schematic](../../docs/pictures/electronics/main-board.png)
*Schematic of the main distribution board (I2C routing, level shifting, LED connectors).*

The audio board manages relays to switch audio sources between wireless receivers and the Raspberry Pi, while also distributing 9 V power to the audio devices.
![Audio relay board](../../docs/pictures/audio-board.jpg)
*Audio board handling source selection and relay control.*

![Audio board schematic](../../docs/pictures/electronics/audio-board.png)
*Schematic of the audio relay board (PCF8574 I/O expander and power regulation).*

## Maintenance Checklist
- Inspect cabling before each performance
- Verify servo calibration after transport
- Confirm LED strips are firmly attached and diffused correctly for stage lighting
- Test emergency stop procedures (describe them in `docs/operations.md`)
