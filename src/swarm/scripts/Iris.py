#!/usr/bin/env python
import rospy 
import numpy as np
import mavros

from geometry_msgs.msg import Point, PoseStamped, Twist 
from sensor_msgs.msg import NavSatFix, Image
from mavros_msgs.msg import * 
from std_msgs.msg import String
from mavros_msgs.srv import * 
from decimal import * 
from math import radians, cos, sin, asin, sqrt

class Iris:

    def __init__ (self, id):

        self.id = id
        self.local_pose = PoseStamped()

        pose = PoseStamped()
        pose.pose.position.x = 0
        pose.pose.position.y = 0
        pose.pose.position.z = 5
    
        global state 
    
    
        def state_callback(data):
        
            global state
            #print("ok")
            state = data
            #rospy.loginfo(data.connected)
            return
    
        def state_listener():
            rospy.Subscriber("/uav0/mavros/state", State, state_callback)
            rate = rospy.Rate(100)
            rate.sleep()
            #rospy.spin()
    
    
    
    
    
        print("ok")
    
        rospy.init_node('takeoff', anonymous=True)
        rate = rospy.Rate(10)
        rospy.wait_for_service("/uav0/mavros/cmd/arming")
        arming_client = rospy.ServiceProxy("/uav0/mavros/cmd/arming", CommandBool)
        rospy.wait_for_service("/uav0/mavros/set_mode") 
        set_mode_client = rospy.ServiceProxy("/uav0/mavros/set_mode", SetMode)
        pose_pub = rospy.Publisher("/uav0/mavros/setpoint_position/local", PoseStamped, queue_size=10)
        pose_pub.publish(pose)
        set_mode = SetMode()
        set_mode._response_class.custom_mode = "OFFBOARD"
        set_mode._response_class.base_mode = 0
        print("ok")
        state_listener()
        for i in range(100):
            pose_pub.publish(pose)
            state_listener()
        print(state.connected) 
        last_request = rospy.Time.now()

        while not rospy.is_shutdown():
            if state.mode != "OFFBOARD" and (rospy.Time.now() - last_request > rospy.Duration(5.0)):
                if set_mode_client(base_mode=0, custom_mode="OFFBOARD"):
                    print("OFFBOARD")
                    last_request = rospy.Time.now()
            else:
                if not state.armed and (rospy.Time.now()-last_request > rospy.Duration(5.0)):
                    arming_client(True)
                    last_request = rospy.Time.now()

            rospy.Subscriber("/uav{}/mavros/local_position/pose".format(self.id), PoseStamped, self.local_pose_callback)
            if self.local_pose.pose.position.z > 4:
                break
            pose_pub.publish(pose)

         
            
    
           
    def goto(self, pose):
        pose_pub = rospy.Publisher("/uav{}/mavros/setpoint_position/local".format(self.id), PoseStamped, queue_size=10)
        pose_pub.publish(pose)

    def local_pose_callback(self, data):
        self.local_pose = data
    