"""Sample Webots controller for the inverted pendulum benchmark."""

from controller import Supervisor
import os
import math

# Get pointer to the robot.
robot = Supervisor()

# Get the time step of the current world.
timestep = int(robot.getBasicTimeStep())

# Get pointers to the position sensor and enable it.
ps = robot.getPositionSensor('pendulum sensor')
ps.enable(timestep)

# Get pointers to the motors and set target position to infinity (speed control).
leftMotor = robot.getMotor("left wheel motor")
rightMotor = robot.getMotor("right wheel motor")
leftMotor.setPosition(float('+inf'))
rightMotor.setPosition(float('+inf'))
leftMotor.setVelocity(0.0)
rightMotor.setVelocity(0.0)
maxSpeed = min(rightMotor.getMaxVelocity(), leftMotor.getMaxVelocity())

# Define the PID control constants and variables.
KP = float(os.environ.get('P_GAIN', '31.4'))
KI = 100.5
KD = float(os.environ.get('D_GAIN', '0'))
integral = 0.0
previous_position = 0.0

# Initialize the robot speed (left wheel, right wheel).
leftMotor.setVelocity(0.0)
rightMotor.setVelocity(0.0)

# Main loop: perform a simulation step until the simulation is over.
while robot.step(timestep) != -1:
    # Read the sensor measurement.
    position = ps.getValue()

    # Stop the robot when the pendulum falls.
    if math.fabs(position) > math.pi * 0.5:
        leftMotor.setVelocity(0.0)
        rightMotor.setVelocity(0.0)
        print("Score: %lf" % robot.getTime())
        print("P_GAIN: %lf" % KP)
        print("I_GAIN: %lf" % KI)
        print("D_GAIN: %lf" % KD)
        with open('result.txt', 'w') as f:
            f.write('%lf %lf %lf %lf' % (robot.getTime(), KP, KI, KD))
        robot.simulationQuit(0)

    # PID control.
    integral = integral + (position + previous_position) * 0.5 / timestep
    derivative = (position - previous_position) / timestep
    speed = KP * position + KI * integral + KD * derivative

    # Clamp speed to the maximum speed.
    if speed > maxSpeed:
        speed = maxSpeed
    elif speed < -maxSpeed:
        speed = -maxSpeed

    # Set the robot speed (left wheel, right wheel).
    leftMotor.setVelocity(-speed)
    rightMotor.setVelocity(-speed)

    # Store previous position for the next controller step.
    previous_position = position
