#!/usr/bin/env python
import rospy 
from geometry_msgs.msg import PoseStamped
from mavros_msgs.msg import * 
from mavros_msgs.srv import *
from sensor_msgs.msg import NavSatFix


class Agent:

    def __init__ (self, id):
        self.state = State()
        self.gps_pose = NavSatFix()
        self.mode = "OFFBOARD"
        self.id = id
        self.local_pose = PoseStamped()

        self.get_local_pose()
        self.get_gps_pose()

        rospy.Subscriber("/uav{}/mavros/state".format(self.id), State, self.state_callback)

        rospy.wait_for_service("/uav{}/mavros/set_mode".format(self.id)) 
        self.set_mode_client = rospy.ServiceProxy("/uav{}/mavros/set_mode".format(self.id), SetMode)

        rospy.wait_for_service("/uav{}/mavros/cmd/arming".format(self.id))
        self.arming_client = rospy.ServiceProxy("/uav{}/mavros/cmd/arming".format(self.id), CommandBool)

        pose = PoseStamped()
        pose.pose.position.x = 0
        pose.pose.position.y = 0
        pose.pose.position.z = 5

        pose_pub = rospy.Publisher("/uav0/mavros/setpoint_position/local", PoseStamped, queue_size=10)
        

        last_request = rospy.Time.now()

        if self.state.mode != "OFFBOARD" and (rospy.Time.now() - last_request > rospy.Duration(5.0)):
            if self.set_mode_client(base_mode=0, custom_mode="OFFBOARD"):
                last_request = rospy.Time.now()
        else:
            if not self.state.armed and (rospy.Time.now()-last_request > rospy.Duration(5.0)):
                self.arming_client(True)
                last_request = rospy.Time.now()
                pose_pub.publish(pose)
                    

    def state_callback(self, data):
        self.state = data
        print(data)

    def local_pose_callback(self, data):
        self.local_pose = data

    def gps_pose_callback(self, data):
        self.gps_pose = data


    def get_local_pose(self):
        rospy.Subscriber("/uav{}/mavros/local_position/pose".format(self.id), PoseStamped, self.local_pose_callback)
        return self.local_pose

    def set_mode(self, mode="OFFBOARD"):
        set_mode = SetMode()
        set_mode._response_class.custom_mode = mode
        set_mode._response_class.base_mode = 0

        rospy.wait_for_service("/uav{}/mavros/set_mode".format(self.id)) 
        set_mode_client = rospy.ServiceProxy("/uav{}/mavros/set_mode".format(self.id), SetMode)
        set_mode_client(base_mode=set_mode._request_class.custom_mode, custom_mode=set_mode._request_class.custom_mode)

        self.mode = mode

    def arm(self):
        rospy.wait_for_service("/uav{}/mavros/cmd/arming".format(self.id))
        arming_client = rospy.ServiceProxy("/uav{}/mavros/cmd/arming".format(self.id), CommandBool)
        arming_client(True)

    
    def takeoff(self, z=5):
        
        #rospy.wait_for_service("/uav{}/mavros/cmd/takeoff".format(self.id)) 
        #takeoff_client = rospy.ServiceProxy("/uav{}/mavros/cmd/takeoff".format(self.id), CommandTOL)
        #takeoff_client(altitude=0.01, latitude=self.gps_pose.latitude, longitude=self.gps_pose.longitude, min_pitch=0, yaw=0)
        #print("TAKING OFF")
        #self.set_mode_client(base_mode=0, custom_mode=self.mode)
        #rospy.sleep(5)

        pose = PoseStamped()
        pose.pose.position.x = self.get_local_pose().pose.position.x
        pose.pose.position.y = self.get_local_pose().pose.position.y
        pose.pose.position.z = z
        print("TAKING OFF")

        self.goto(pose)
  

    def goto(self, pose):
        pose_pub = rospy.Publisher("/uav{}/mavros/setpoint_position/local".format(self.id), PoseStamped, queue_size=10)
        pose_pub.publish(pose)

    def get_gps_pose(self):
        rospy.Subscriber("/uav{}/mavros/global_position/global".format(self.id), NavSatFix, self.gps_pose_callback)
        return self.gps_pose

    def offboard(self):
        last_request = rospy.Time.now()
        if self.state.mode != "OFFBOARD" and (rospy.Time.now() - last_request > rospy.Duration(5.0)):
            if self.set_mode_client(base_mode=0, custom_mode="OFFBOARD"):
                last_request = rospy.Time.now()
        else:
            if not self.state.armed and (rospy.Time.now()-last_request > rospy.Duration(5.0)):
                self.arming_client(True)
                last_request = rospy.Time.now()