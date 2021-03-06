#!/usr/bin/env python

# imports
import sys
import numpy as np
import json

# ros imports
import rospy
from std_msgs.msg import String



class MAAS_node:

    def __init__(self, num_of_points):

        # subscribers
        self.sample_sub = rospy.Subscriber("/sample/data", String, self.sampled_data_callback)

        self.status_sub = rospy.Subscriber('/update/status', String, self.status_data_callback)


        # publishers
        self.maas_pub = rospy.Publisher('/maas/data', String, queue_size = 10) # jsonified data

        # data samples collected so far
        self.json_dict_samples = {"sample_values": []}

	# current points of interest
	self.POIs =  {"POIs": []}
	
	# number of POI points to publish
	self.num_of_points = num_of_points
	


############################# Subscriber Callback functions ####################
    def sampled_data_callback(self, data):
	
	print("receieved sample data")
	message = json.loads(data.data)
	sample = message["sample"][0]
	
	# get the agent_id, x and y and z locations of the agent's location, measurement type (e.g. depth), and measurement value 
	agent_id = sample["agent_id"]
	x = sample["x"]
	y = sample["y"]
	z = sample["z"]
	measurement_type = sample["measurement_type"]
	measurement_value = sample["measurement_value"]

 	self.json_dict_samples['sample_values'].append({"agent_id":agent_id, "x": x, "y": y,  "z": z, "measurement_type":measurement_type, "measurement_value":measurement_value})
	#print(self.json_dict['sample_values'])

    def status_data_callback(self, data):
	
	print("receieved status data")
	message = json.loads(data.data)
	status = message["status"][0]

	# get the agent_id, x and y and z locations of the agent's location, measurement type (e.g. depth), and measurement value 
	agent_id = status["agent_id"]
	x = status["x"]
	y = status["y"]
	z = status["z"]
	
 	#self.json_dict_samples['sample_values'].append({"agent_id":agent_id, "x": x, "y": y,  "z": z, "measurement_type":measurement_type, "measurement_value":measurement_value})
	print("Got status update from agent: "+str(agent_id)+ "x: "+ str(x) + "y: "+str(y)+ "z: "+str(z))

############################# Publisher functions ##############################
    def compute_POIs(self):
	
	# reset map
	self.POIs =  {"POIs": []}
	print("compute")	
	
	for i in xrange(self.num_of_points):
	    x = 3.3+i
	    y = 5.2
	    z = 3.4
	    measurement_type = "depth"	
	    score = 5.5

 	    self.POIs['POIs'].append({"x": x, "y": y,  "z": z, "measurement_type":measurement_type, "score":score})
	

    def publish_points(self):

	# compute k best points
	self.compute_POIs()
        # publish action
        self.maas_pub.publish(json.dumps(self.POIs))



############################# Main #############################################
def main():
    # init ros node
    rospy.init_node('MAAS', anonymous = True)

    # class instance
    MAAS_instance = MAAS_node(5)

    # create ros loop
    pub_rate = 1 # hertz
    rate = rospy.Rate(pub_rate)

    while (not rospy.is_shutdown()):
        # do some stuff if necessary
	print("Publish Points of Interest")
	MAAS_instance.publish_points()
	
        # ros sleep (sleep to maintain loop rate)
        rate.sleep()

if __name__ == '__main__':
    try:
        main()
    except rospy.ROSInterruptException:
        pass
