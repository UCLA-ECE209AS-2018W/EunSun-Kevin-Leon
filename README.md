# Automatic Firewall
## Eun Sun Lee, Leon Kozinakov, Zhengxu Xia

## Background

**Material Selection:**

*NVIDIA Jetson TK1 -* This board was chosen as the primary computer on the car for a good reason. The integrated GPU is CUDA enabled which means it can do complicated image processing and computer vision tasks in near-real-time. We have multiple high-bandwidth sensor inputs, so we do need the performance on-board.

<img src="https://en.wikipedia.org/wiki/PfSense#/media/File:Pfsense_logo.png" width="250">

*Teensy 3.2 Microcontroller -* This is the microcontroller that interfaces with the motors to relieve some of the duties from the main computer. The choice is somewhat arbitrary since other uControllers could also work, but the Teensy is cheap and Arduino compatible, so writing software for it is straightforward.

<img src="https://www.pjrc.com/teensy/teensy32_front_pinout.png" width="250">

*LIDAR -* This is a very expensive and accurate sensor and is the primary means of obstacle detection for the car. The angle and distance resolution is much higher than camera or IR only based designs.

<img src="https://acroname.com/sites/default/files/styles/large/public/r359-ust-10lx.jpg?itok=N8epOYVl" width="250">

*9DOF IMU -* This sensor is important for the car to know how fast it is moving, so that it can know how to predict collisions. The alternative would be to mount rotation sensors on the wheel and angle readers on the servos, but this would be a lot more involved since we are working with a set chassis.

<img src="https://cdn.sparkfun.com//assets/parts/1/1/7/7/5/14001-05.jpg" width="250">

*ZED Camera and Structure Sensor -* These are both optional of course, since we are already using LIDAR, however their output might not be redundant. It's better to instead try to implement sensor fusion, to get a clearer picture of the car's surroundings.

<img src="https://cdn.stereolabs.com/img/product/ZED_product_main.jpg" width="300">

**Manufacturing & Assembly**

The base chassis for this project is the Traxxas, and by itself it's just a simple RC car. Our goal is to take out some of the internals and create a housing for all of our sensors, computers, batteries, and interconnects. The F1/10th organization released some CAD files that were used on a laser cutter to "print" the components necessary for the housing. We had hoped that this process would go smoothly, however manufacturing the parts proved to be a bit of a pain. Due to precision inaccuracies in the software used to print the components, all the pieces were printed 1% too small, and we did not notice untill we had to mate the housing to the chassis of the car. This meant that we wasted the only sheet of plastic large enough, so we had to order a new set. This caused us to delay the assembly later on. Once we had finaly resolved this issue, we were ready to move on to the assembly of the Teensy circuit and the re-wiring of the car's internals. This was also somethng we had hoped would take a couple of hours, but incomplete and out-of-date schematics on the F1/10th website forced us to reverse engineer the circuit. After soldering and testing it, we moved to the IMU and LIDAR. Unfortunately, our IMU was a different size than the original and consequently we had to redesign some CAD files to have it fit the car. The LIDAR was also missing a power cable, so we had to create a custom one by tapping into the power going to the Jetson. Finally, the main battery we were using was too large to fit into the chassis, so we ended up simply taping it to the bottom of the chassis, so at least the car would have a low center of gravity.

## Progressive Testing

We figured that with a project this involved, it would be smart to do component and unit testing along the way to make sure we have a working car. We began by testing the mechanical fit of the parts we manufactured to the rest of the car to make sure they would eventually fit during assembly. Then, while connecting the Teensy circuit on a protoboard, we did continuity testing with a digital multimeter at every step of the way. We are not experts at soldering so had to make sure there were no short circuits that would damage the Teensy microcontroller. We also tested flashing the Teensy and running simple programs before connecting it to anything to make sure it worked out-of-the-box. Before mating the teensy circuit to the chassis and re-wiring, we first tested the Traxxas RC car in its normal RC operating mode to see if there were any manufacturing errors, and luckily there weren't any. We did some stress testing including hard impacts, breaking from high speed, testing high RPM on the motors, and how much weight it could carry. After mating the Teensy to the chassis, we tested to see the normal operation was maintained, and then we also tested that the kill switch on the autonomous mode was functioning. We then moved on to the sensors. We tested and calibrated the IMU first, including flashing it with some updated firmware that can perform AHRS (attitude heading reference system) calculations. Next came the LIDAR, which we tested using software provided by the manufacturer. The car was now ready for system-level testing with autonomous software running.

## Coding and Environment Setup

#### Teensy 3.2 Firmware

The Teensy Microcontroller we're using has a simple 32bit ARM chip, and programming it is very simple if you have a .hex file with your firmware. However, we wanted an easier way to do code development, so we used Teensyduino, a library that works with the Arduino IDE. This makes writing code for the Teensy very simple. We began by using some starter code from the F1/10th Github, which we modified according to the values we tuned as explained in the Testing section above. The Teensy essentially waits in a loop for messages to arrive over a Serial link to the NVIDIA Jetson main computer. The messages might involve changing heading, changing speed, or stopping altogether. The Teensy just executes whatever the main CPU tells it.

#### NVIDIA Jetson TK1

This is the true brain of the autonomous vehicle. The first step was to verify basic functionality and install an OS, a custom kernel, and a custom NVIDIA driver package. Once those steps were complete, we could start installing drivers for all of our hardware, and of course ROS. Robot Operating System is a set of libraries, protocols, conventions and tools that enable quick writing of code for robots. The way it works is hiearchical by design, so you'd have multiple nodes running in a package. For us, each node was a python script, so that we only had to compile once, and then we could make incremental changes without re-compiling. We also had the Jetson itself set-up with Arduino IDE so that we could compile and re-flash the firmware all on the car.

The set-up process for the Jetson was much more involved, so if you want to see a step-by-step procedure, visit the docs folder.

## Results

We started with the PID algorithm supplied by F1/10. It was a very simple algorithm that involved maintaining a fixed distance to a wall on the right while driving forward. It searched for a corner, and then was able to navigate around the corner. This approach ignored anything happening in front of or to the left of the car, so our first task was to incorporate more sensory inputs into the control loop. 

We wanted to be able to drive down the center of a hallway and navigate turns either to the left of the right. We were able to get the car to drive down the center by taking the existing framework for the right wall and mirror it on the left. Then, instead of maintaining a fixed distance to the right wall, the car maintains an equal distance on both its left and its right.

We also implemented an auto-brake system so that the car would stop running itself into walls. Basically, if the car is heading straight for a wall, and it doesn't see any way out, it throws itself in reverse at full power until it stops. We were able to drive into a wall head-on at our full normal operating speed and brake before impact.
  
