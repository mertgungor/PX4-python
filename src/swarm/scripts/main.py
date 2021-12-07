#!/usr/bin/env python
import rospy 
from geometry_msgs.msg import PoseStamped
from mavros_msgs.msg import * 
from mavros_msgs.srv import *
from Agent import Agent 
from Iris import Iris 
from swarm.srv import PoseCommand

pose = PoseStamped()
pose.pose.position.x = 5
pose.pose.position.y = 0
pose.pose.position.z = 5

global state 


def state_callback(data):
    
    global state
    state = data
    return

def state_listener():
    rospy.Subscriber("/uav0/mavros/state", State, state_callback)
    rate = rospy.Rate(100)
    rate.sleep()
    #rospy.spin()



if __name__ == '__main__':
    iris = Iris(0)
    rospy.sleep(5)
    print("going")
    iris.goto(pose)



    #rospy.init_node('takeoff', anonymous=True)
    #rate = rospy.Rate(10)
    #sec5 = rospy.Rate(0.2)
#
    #rospy.wait_for_service("/uav0/mavros/cmd/arming")
    #arming_client = rospy.ServiceProxy("/uav0/mavros/cmd/arming", CommandBool)
#
    #rospy.wait_for_service("/uav0/mavros/set_mode") 
    #set_mode_client = rospy.ServiceProxy("/uav0/mavros/set_mode", SetMode)
#
    #pose_pub = rospy.Publisher("/uav0/mavros/setpoint_position/local", PoseStamped, queue_size=10)
    #pose_pub.publish(pose)
#
    #state_listener()
#
    #for i in range(100):
    #    pose_pub.publish(pose)
    #    state_listener()
#
    #print(state.connected) 
    #
#
    #last_request = rospy.Time.now()
#
    #while not rospy.is_shutdown():
    #    if state.mode != "OFFBOARD" and (rospy.Time.now() - last_request > rospy.Duration(5.0)):
    #        if set_mode_client(base_mode=0, custom_mode="OFFBOARD"):
    #            last_request = rospy.Time.now()
    #    else:
    #        if not state.armed and (rospy.Time.now()-last_request > rospy.Duration(5.0)):
    #            arming_client(True)
    #            last_request = rospy.Time.now()
    #    pose_pub.publish(pose)
    #agent0 = Agent(0)
    ##print(agent0.state)
    #rospy.sleep(3)
    ##print(agent0.state)
    #agent0.takeoff()
    #rospy.sleep(5)
        
    