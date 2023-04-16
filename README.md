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


## manipulatotion

git clone https://github.com/ROBOTIS-GIT/turtlebot3_manipulation.git
git clone https://github.com/ROBOTIS-GIT/turtlebot3_manipulation_simulations.git
git clone https://github.com/ROBOTIS-GIT/open_manipulator_dependencies.git
sudo apt install ros-noetic-ros-control* ros-noetic-control* ros-noetic-moveit*
cd .. && catkin_make
