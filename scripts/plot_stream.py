#! /usr/bin/env python
# -*- coding: utf-8 -*-
"""
Created on 05/12/14

@author: Sam Pfeiffer

Plot stream of topic of Naoqi audio

"""
from naoqi_msgs.msg import AudioBuffer

NAOQI_AUDIO_TOPIC = '/naoqi_microphone/audio_raw'

from bokeh.plotting import figure, output_server, show, cursession
from scipy import arange
from bokeh.models.renderers import GlyphRenderer
import time
import rospy

class PlotAudio():
    def __init__(self):
        rospy.loginfo("Setting up plot")
        self.MAX_DATA = 1000000 #* 10 # this was one message
        self.x_data = [0]
        self.y_data = [0]
        output_server("audio_plot")
        self.p1 = figure(title="Audio plot")
        self.p1.line(self.x_data, self.y_data,
            color="#0000FF",
            tools="pan,resize,wheel_zoom", 
            width=1200,
            height=300,
            legend='value of thing')
        show()
        self.renderer = self.p1.select(dict(type=GlyphRenderer))
        self.ds = self.renderer[0].data_source
        
        self.audio_data_buffer = []
        rospy.loginfo("Setting up sub")
        self.sub = rospy.Subscriber(NAOQI_AUDIO_TOPIC, AudioBuffer, self.audio_cb)
        rospy.loginfo("Done!")
        
    def audio_cb(self, data):
        rospy.loginfo("Callback received!")
        print "<Previous y_data len: " + str(len(self.y_data))
        self.y_data.extend(data.data)
        #self.y_data = data.data
        print ">After y_data len: " + str(len(self.y_data))
        
        print "--------------"
        print "len of y_data: " + str(len(self.y_data))
        excess_of_data = None
        if len(self.y_data) > self.MAX_DATA:
            print "excess of data: " + str(len(self.y_data) - self.MAX_DATA)
            excess_of_data = len(self.y_data) - self.MAX_DATA
#             self.x_data = arange(self.x_data[excess_of_data], (len(self.x_data) - 1) * 0.01, 0.01).tolist()
            self.y_data = self.y_data[excess_of_data:]
            
        print "<Previous x_data len: " + str(len(self.x_data))
        if excess_of_data:
            new_times = arange(self.x_data[-1], len(self.y_data) * 0.01 + self.x_data[-1], 0.01).tolist()
            print "Initial time: " + str(self.x_data[-1])
            self.x_data = new_times[:len(self.y_data)]
            print "Final time: "+ str(self.x_data[-1])
            
        else: # if we are just adding data to the array
            new_times = arange(self.x_data[-1], len(data.data) * 0.01 + self.x_data[-1], 0.01).tolist()
            self.x_data.extend(new_times[:len(self.y_data)])
        print ">After x_data len: " + str(len(self.x_data))
        
        if len(self.x_data) != len(self.y_data):
            rospy.logerr("Error, not same size")
            exit(0)


        
        
    def run(self):
        while not rospy.is_shutdown():
            print "<<<<<< Updating plot >>>>>"
            self.ds.data["x"] = self.x_data
            self.ds.data["y"] = self.y_data
            self.ds._dirty = True
            cursession().store_objects(self.ds)
        
            time.sleep(0.01)

if __name__=="__main__":
    rospy.init_node('plot_audio_msgs_data_')
    PA = PlotAudio()
    PA.run()
    

