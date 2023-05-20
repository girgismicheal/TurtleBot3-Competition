#!/usr/bin/env python


from __future__ import print_function
import sys
import rospy
import cv2
from std_msgs.msg import String
from sensor_msgs.msg import Image
from cv_bridge import CvBridge, CvBridgeError
from geometry_msgs.msg import Twist
import numpy as np
import math


class TakePhoto:
    def __init__(self):
        
        self.pub=rospy.Publisher('/cmd_vel',Twist,queue_size=10)
        self.rate=rospy.Rate(1)
        self.rot=Twist()
        
        self.ball_is_taken=False
        self.reach_goal = False
        self.count = 0

        self.cx=0
        self.cy=0

        self.bridge = CvBridge()
        self.image_received = False
        
        # Connect image topic
        img_topic = "/camera/rgb/image_raw"
        self.image_sub = rospy.Subscriber(img_topic, Image, self.callback)

        # Allow up to one second to connection
        rospy.sleep(1)

    def callback(self, data):

        # Convert image to OpenCV format
        try:
            cv_image = self.bridge.imgmsg_to_cv2(data, "bgr8")
        except CvBridgeError as e:
            print(e)

        self.image_received = True
        self.image = cv_image
        #self.show_image(cv_image)
        
        if (not self.ball_is_taken):
           _,_,_ = self.find_ball(cv_image)
        elif self.ball_is_taken and not self.reach_goal:
            _,_,_,_ = self.find_goal(cv_image)
        elif self.ball_is_taken and self.reach_goal:
            # self.reach_goal and self.ball_is_taken:
            self.reach_goal=False
            self.ball_is_taken = False
        print(self.cy)
        self.move_to_object()


    def show_image(self,img):
        cv2.imshow("Image Window", img)
        cv2.waitKey(3)
        
    def find_goal(self, img, view=False, valiate = False):
        # print('find goal')
        valid_goal = False
        line_exist=False
        line = (0, 0)

        hsv_frame = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
        hsv_frame = cv2.resize(hsv_frame,(640,300))
        img = cv2.resize(img,(640,300))

        lower_red = np.array([0, 50, 50])
        upper_red = np.array([10, 255, 255])

        mask_frame = cv2.inRange(hsv_frame, lower_red, upper_red)
        cv2.imshow("mask", mask_frame)
        contours, _ = cv2.findContours(mask_frame,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
        contours = [con for con in contours if cv2.contourArea(con)>10]
        if len(contours) == 0:
            return line, valid_goal, line_exist, None
        
        # Merge contours into one
        largest_contours = sorted(contours, key=cv2.contourArea, reverse=True)[:int(math.ceil(len(contours)*0.9))]
        merged_contour = np.concatenate(largest_contours)

        # Find the bounding rectangle of the merged contour
        x, y, w, h = cv2.boundingRect(merged_contour)
        img = cv2.rectangle(img, (x, y),(x + w, y + h),(255, 0, 0), 2)

        valid_goal = (w/img.shape[1]) > 0.9
        line_exist=True
        if valid_goal:
            line = (x+(w/2), y+(w/2))
        else:
            line = (0, 0)
        
        if valiate==False:
            self.cx, self.cy = line
            print("cy", self.cy)
            # change
            if self.cy>300:
                self.reach_goal = True
                self.ball_is_taken=False
        # print(self.cx)
        cv2.imshow("window", img)
        cv2.waitKey(3)
        return line, valid_goal, line_exist, merged_contour


   
    def check_valid_ball(self, img, ball_contours, view=False):
        line, valid_goal, line_exist, line_contour = self.find_goal(img, False, valiate = True)
        if not line_exist: return True

        x_lowest_point_in_ball, y_lowest_point_in_ball = max(ball_contours, key=lambda p: p[0][1])[0]
        x_largest_point_in_line, y_largest_point_in_line = min(line_contour, key=lambda p: p[0][1])[0]

        if view:
            x, y = x_largest_point_in_line, y_largest_point_in_line
            img = cv2.rectangle(img, (x, y),(x + 10, y + 10),(255, 0, 0), 2)

            x, y = x_lowest_point_in_ball, y_lowest_point_in_ball
            img = cv2.rectangle(img, (x, y),(x + 10, y + 10),(255, 0, 255), 2)
        # check if the ball above line
        if y_lowest_point_in_ball < y_largest_point_in_line:
            return False
        return True

    def find_ball(self, img, view=False):
        self.reach_goal = False
        hsv_frame = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
        hsv_frame = cv2.resize(hsv_frame,(640,300))
        img = cv2.resize(img,(640,300))
        org_img = img.copy()

        lower_yellow = np.array([22, 50, 50])
        upper_yellow = np.array([30, 255, 255])

        mask_frame = cv2.inRange(hsv_frame, lower_yellow, upper_yellow)
        cv2.imshow("mask",mask_frame)
        contours, _ = cv2.findContours(mask_frame,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)

        min_area = 10
        # Iterate over all contours and filter out small ones
        filtered_contours = [con for con in contours if cv2.contourArea(con)>min_area and self.check_valid_ball(org_img.copy(), con)]
        largest_contours = sorted(filtered_contours, key=cv2.contourArea, reverse=True)

        ball = (0, 0)
        valid_goal = False
        ball_contours = None
        self.cx, self.cy = ball

        if len(largest_contours) > 0:
            ball_contours = largest_contours[0]
            x, y, w, h = cv2.boundingRect(ball_contours)
            img = cv2.rectangle(img, (x, y),(x + w, y + h),(255, 0, 0), 2)
            ball = (x+(w/2), y+(w/2))
            valid_goal=True

            self.cx, self.cy = ball
            # if(W>310 and self.cy>240):
            # print("ball taken",w, self.cy)
            if(w>330 and self.cy>330):
                self.cx, self.cy = (0,0)
                self.ball_is_taken=True
                # print("Taken")
            else:
                self.ball_is_taken=False
            
            #print(f"W={w}")
            #print(self.cx)

        cv2.imshow("window", img)
        cv2.waitKey(3)

        return ball, valid_goal, ball_contours   
        

    def move_to_object(self):
        if(self.cx==0):
            text="searching"
            print(self.ball_is_taken)
            print(self.reach_goal)
            
            if not self.ball_is_taken :
                # print("ball")
                self.rot.angular.z=0
                self.rot.linear.x=-0.1

            elif not self.reach_goal and self.ball_is_taken:
                # print("gaol ball")
                self.rot.angular.z=0.1
                self.rot.linear.x=0.01
            # elif self.reach_goal and self.ball_is_taken:
            #     print("gaol ball")
            #     self.rot.angular.z=0
            #     self.rot.linear.x=-1.1
                
            else:
                print("nothing")
                # self.count +=1
                # if self.count<150:
                #     self.rot.angular.z=0
                #     self.rot.linear.x=-0.1
                # elif 150 <= self.count and self.count <= 1170+150:
                #     self.rot.angular.z=0.15
                #     self.rot.linear.x=0
                # else:
                #     self.count =0
                #     self.rot.angular.z=0
                #     self.rot.linear.x=0
        else:
            obj_x=self.cx-320
            if(obj_x<=40 and obj_x>=-40):
                text="straight"
                self.rot.angular.z=0
                self.rot.linear.x=0.1
            elif(obj_x>60):
                text="Left"
                self.rot.angular.z=-0.1
                self.rot.linear.x=0
            elif(obj_x<-60):
                text="Right"
                self.rot.angular.z=0.1
                self.rot.linear.x=0
            # print(text)

        self.pub.publish(self.rot)
        

    def stop(self):
        self.rot.angular.z=0
        self.rot.linear.x=0
        self.pub.publish(self.rot)
        #print(text)


if __name__ == '__main__':

    # Initialize
    rospy.init_node('take_photo', anonymous=False)
    camera = TakePhoto()

    while not rospy.is_shutdown():
        # print("spain")
        rospy.sleep(0.1)
        rospy.spin()

    camera.stop

