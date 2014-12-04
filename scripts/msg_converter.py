#! /usr/bin/env python
# -*- coding: utf-8 -*-
"""
Created on 04/12/14

@author: Sam Pfeiffer


"""
import rospy
import numpy
from naoqi_msgs.msg import AudioBuffer
from audio_common_msgs.msg import AudioData

AUDIO_COMMON_TOPIC = '/audio'
NAOQI_AUDIO_TOPIC = '/naoqi_microphone/audio_raw'

class converterNaoqiAudioToAudioCommon():
    def __init__(self):
        rospy.loginfo("Setting up pub and sub")
        self.pub =rospy.Publisher(AUDIO_COMMON_TOPIC, AudioData)
        self.sub = rospy.Subscriber(NAOQI_AUDIO_TOPIC, AudioBuffer, self.audio_cb)
        rospy.loginfo("Done!")

        
    def audio_cb(self, data):
        #ab = AudioBuffer()
        # int16[] data
        print "."
        ad = AudioData()
        # uint8[] data
#         for item in data.data:
#             ad.data.append(item)
        data_uint8 = numpy.array(data.data, dtype=numpy.uint8)
        ad.data = data_uint8.tolist()
        self.pub.publish(ad)

if __name__=="__main__":
    rospy.init_node('convert_audios_msgs_')
    
    c = converterNaoqiAudioToAudioCommon()
    rospy.spin()
