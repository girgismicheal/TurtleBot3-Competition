# TurtleBot3-Competition

## Installations:

- Install Noetic version for this link
(https://emanual.robotis.com/docs/en/platform/turtlebot3/quick-start/)


## Env Build

export TURTLEBOT3_MODEL=waffle_pi <br>
source /home/girgis/Desktop/catkin_ws/devel/setup.bash <br>
roslaunch turtlebot3_gazebo turtlebot3_world.launch <br>

## Robot Move

export TURTLEBOT3_MODEL=waffle_pi <br>
roslaunch turtlebot3_teleop turtlebot3_teleop_key.launch <br>


## manipulatotion

git clone https://github.com/ROBOTIS-GIT/turtlebot3_manipulation.git <br> 
git clone https://github.com/ROBOTIS-GIT/turtlebot3_manipulation_simulations.git <br> 
git clone https://github.com/ROBOTIS-GIT/open_manipulator_dependencies.git <br>
sudo apt install ros-noetic-ros-control* ros-noetic-control* ros-noetic-moveit* <br>
cd .. && catkin_make <br>

## End nodes
killall gzserver && killall gzclient



## inti env
export TURTLEBOT3_MODEL=waffle_pi <br>
source /home/girgis/Desktop/foot_ball_ws/devel/setup.bash<br>
roslaunch turtlebot3_gazebo turtlebot3_empty_world.launch<br>

export TURTLEBOT3_MODEL=waffle_pi<br>
roslaunch turtlebot3_teleop turtlebot3_teleop_key.launch<br>


roslaunch turtlebot3_gazebo turtlebot3_world.launch<br>

## reset env
killall gzserver && killall gzclient<br>
roslaunch turtlebot3_gazebo turtlebot3_empty_world.launch<br>

## Run Logic
cd /Desktop/foot_ball_ws/src/ROS_turtlebot3_OpenCV<br>
python3 Ball_and_Goal_follower.py<br>


