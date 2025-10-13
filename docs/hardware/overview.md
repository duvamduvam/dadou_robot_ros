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

## Devices
All motors are drived by a I2C PCA9685 PWM directly from RPI4, it diminish the connection and risk to to RPI
![PCA9685](../../docs/pictures/consumable-parts/PCA9685.png)

The I2C signal from RPI is isolated by Isolateur I2C bidirectionnel ISO1540-STEMMA
![Wheel system](../../docs/pictures/consumable-parts/i2c-isolator.png)
### Wheels differential drive
![Wheel system](../../docs/pictures/wheel-motor.jpg)
**The PWM signal is send to the cytron smartdrive motor driver 40Amp 10V-45V SmartDrive DC Motor Driver**
![cytron smart drive](../../docs/pictures/consumable-parts/smartdrive.png)
**The motors are two cycle motors brushless 250W**
![cytron smart drive](../../docs/pictures/consumable-parts/brushless-motor.png)

### Arms, eyes and mouth servos motors
**The motors for arms and mouth RC Servo ASME-MR 380kg cm 360°**
![cytron smart drive](../../docs/pictures/consumable-parts/arm-motor.png)                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                
**The motors for the eyes is a JX Servo CLS-12V7346 46KG 12V**
![cytron smart drive](../../docs/pictures/consumable-parts/servo-cls-12V.png)    

### Power supply
The battery is a lithium 18650 of 40c cells (8*5) (I m not exactly sure now)
The out voltage and the charge is manages by a BMS Daly Smart BMS Li-ion 7S LiFePo4 4S APP BMS 8S 24V Lifepo4 BMS 16S.
It delivers 24V 
![cytron smart drive](../../docs/pictures/consumable-parts/bms-24V-30A.png)    
12V is generer by electric convertisso MEAN WELL SD-50B-24 -> 12
![cytron smart drive](../../docs/pictures/consumable-parts/convertisseur.png)    
5V is genererated by electric convertisso MEAN WELL SD-50B-24 -> 5
![cytron smart drive](../../docs/pictures/consumable-parts/convertisseur.png)

## Electronics board
Document diagrams, pinouts, and maintenance procedures here. Include photos or links under `docs/hardware/assets/` as they become available.
The main board connected to RPI
![cytron smart drive](../../docs/pictures/main-board.jpg)   
The shematic of the board, it mostly connect i2c for pwm control, and ledstrip and matix led from 74AHCT125 quad level shiffter
![cytron smart drive](../../docs/pictures/electronics/main-board.png)   
The audio board manage relay, so it can activate the audio output, redirect wirless audio and rpi audio to the output
![cytron smart drive](../../docs/pictures/audio-board.jpg)   
The shematic of the board, it drivers relays from i2c I/O board PCF8574, and 9V power supply for audio devices
![cytron smart drive](../../docs/pictures/electronics/audio-board.png)   

## Maintenance Checklist
- Inspect cabling before each performance
- Verify servo calibration after transport
- Confirm LED strips are firmly attached and diffused correctly for stage lighting
- Test emergency stop procedures (describe them in `docs/operations.md`)
