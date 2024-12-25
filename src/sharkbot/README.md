from watchdog.observers.winapi import WAIT_TIMEOUTfrom jinja2.nodes import Getattr

# Sharkbot Code Organization

The 2025 Sharkbot is a "command-based" robot. 

## Sharkbot Class

The "entry point" for the robot is the `Sharkbot` class. This class will change very rarely, as it mostly exists to hold the `RobotSystems` container class.

## RobotSystems Class
The `RobotSystems` class is a container for all of the robot's subsystems. It is responsible for creating the subsystems. This class will only change when subsystems are added or removed.

## Subsystems
The `subsystems` directory contains the definitions for the robots subsystem. A subsystem is a logical group of hardware that works together to perform a specific function. For example, the `Drive` subsystem is responsible for controlling the robot's drive motors. The `Vision` subsystem is responsible for interfacing with the camera.

## Commands

The `commands` directory contains the definitions for the robot's commands. A command is a small piece of code that performs a specific task. For example, the `FireCommand` class is responsible for the sequence of events that occur when the robot's `Shooter` subsystem fires a ball. In a simple case, maybe that's just opening a gate, waiting for the ball to clear, and closing the gate. 

## Constants

The `constants` directory contains the definitions for the robot's constants. Constants are values that are used throughout the robot code. For example, the `DriveConstants` class contains the maximum speed of the robot's drive motors.

## Simulation

The `simulation` directory contains the definitions for the robot's simulation. The simulation is a way to test the robot code without having the physical robot. The simulation code should be as close to the real robot code as possible. (Note: This approach may be a little too advanced for the 2025 season)

## Tests

The `tests` directory contains the definitions for the robot's tests. Tests are small pieces of code that verify that the robot code works as expected. For example, the `DriveTest` class might verify that the robot drives straight when the `Drive` subsystem is commanded to drive straight.

## Utilities

The `utilities` directory contains the definitions for the robot's utilities. Utilities are small pieces of code that are used throughout the robot code. For example, the `MathUtils` class might contain utility functions for doing math operations.