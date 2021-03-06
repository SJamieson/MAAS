#!/usr/bin/env python


# imports
import sys
import numpy as np
import json

# ros imports
import rospy
from std_msgs.msg import String


class MAAS_Controller:
    def __init__(self):

         # subscribers
        self.poi_sub = rospy.Subscriber("/maas/data", String, self.data_callback)
	# POI command publisher   	
	self.goto_pub = rospy.Publisher('/sample/goto', String, queue_size = 10) # jsonified data
	    
    
    
    def data_callback(self, data):

	# json loads
        temp_data = json.loads(data.data)
	
	print("I got the POIs - how exciting!")
	print(data.data)
	
	# get POI
	message = json.loads(data.data)
	poi = message['POIs'][0]
	#agent_id = sample["agent_id"]
	x = poi["x"]
	y = poi["y"]
	z = poi["z"]
	measurement_type = poi["measurement_type"]
	score = poi["score"]

	agent_id = 1

	# reset the data - and send it  	
	self.json_dict = {'GoTo': []}
	self.json_dict['GoTo'].append({"agent_id":agent_id, "x": x, "y": y,  "z": z, "measurement_type":measurement_type})
	
        # publish action
        self.goto_pub.publish(json.dumps(self.json_dict))
    

	


############################# Main #############################################
def main():

    # init ros node
    rospy.init_node('test_controller', anonymous = True)

    # class instance
    test_instance = MAAS_Controller()

    # create ros loop
    pub_rate = 10 # hertz
    rate = rospy.Rate(pub_rate)

    while (not rospy.is_shutdown()):
        print("Controller is alive")
        # ros sleep (sleep to maintain loop rate)
        rate.sleep()

if __name__ == '__main__':
    try:
        main()
    except rospy.ROSInterruptException:
        pass
