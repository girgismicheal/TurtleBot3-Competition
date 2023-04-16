# TurtleBot3-Competition

## Installations:

- Install Noetic version for this link
(https://emanual.robotis.com/docs/en/platform/turtlebot3/quick-start/)


## Env Build

export TURTLEBOT3_MODEL=waffle_pi
source /home/girgis/Desktop/catkin_ws/devel/setup.bash
roslaunch turtlebot3_gazebo turtlebot3_world.launch

## Robot Move

export TURTLEBOT3_MODEL=waffle_pi
roslaunch turtlebot3_teleop turtlebot3_teleop_key.launch
