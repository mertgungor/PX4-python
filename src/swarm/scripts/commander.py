#!/usr/bin/env python

import rospy
from mavros_msgs.srv import CommandTOL 
from geometry_msgs.msg import PoseStamped, TwistStamped
from nav_msgs.msg import Odometry
from sensor_msgs.msg import NavSatFix

import math

from swarm.srv import PoseCommand

from copy import deepcopy

gps_pose = NavSatFix()
odomery_pose = Odometry()


def wait_until_pose(x, y, z):
    rate = rospy.Rate(5)
    error = 0.5
    dx = x - odomery_pose.pose.pose.position.x
    dy = y - odomery_pose.pose.pose.position.y
    dz = z - odomery_pose.pose.pose.position.z
    distance = math.sqrt(abs(math.pow(dx,2) + math.pow(dy,2) + math.pow(dz,2)))

    while True:
        rate.sleep()
        
        dx = x - odomery_pose.pose.pose.position.x
        dy = y - odomery_pose.pose.pose.position.y
        dz = z - odomery_pose.pose.pose.position.z
        distance = math.sqrt(abs(math.pow(dx,2) + math.pow(dy,2) + math.pow(dz,2)))


        if distance < error:
            return True
        else:
            continue

def current_gps_pose_callback(data):
    global gps_pose
    gps_pose = deepcopy(data)

def current_odometry_pose_callback(data):
    global odomery_pose
    odomery_pose = deepcopy(data)
    
    
def current_odometry_pose():
    odometry_sub = rospy.Subscriber("/mavros/global_position/local", Odometry, current_odometry_pose_callback)

def current_gps_pose():
    pose_sub = rospy.Subscriber("/mavros/global_position/global", NavSatFix, current_gps_pose_callback)

def land(): # doesn't work !!!!!!!!!!!! 
    try:

        pose_commander(odomery_pose.pose.pose.position.x, odomery_pose.pose.pose.position.y, 0)

        rospy.wait_for_service("/mavros/cmd/land")

        land_service = rospy.ServiceProxy("/mavros/cmd/land", CommandTOL)
        land_service(min_pitch=0, yaw=0, latitude=0, longitude=0, altitude=0)

        print("land service called")

    except rospy.ServiceException as e:

        print("Service call failed: %s"%e)
        return False

def pose_commander(x, y, z):

    try:

        rospy.wait_for_service("PoseCommand")

        client = rospy.ServiceProxy("PoseCommand", PoseCommand)
        resp = client(x, y, z)

        wait_until_pose(x, y, z)

        return resp
    except rospy.ServiceException as e:
        print("Service call failed: %s"%e)
        return False

def draw_square(length):

    pose_commander(length, 0, length)

    pose_commander(length, length, length)

    pose_commander(0, length, length)

    pose_commander(0, 0, length)
    

if __name__ == "__main__":
    rospy.init_node("commander", anonymous=True)
    rate = rospy.Rate(0.5)
    rate.sleep()

    try:

        current_gps_pose()
        current_odometry_pose()
        
        print("waiting...")

        while True:
            rate.sleep()
            if odomery_pose.pose.pose.position.x != 0:
                print("ready")
                break

        draw_square(5)            


    except rospy.exceptions.ROSInterruptException:
        print("\nshutdown")

    
    