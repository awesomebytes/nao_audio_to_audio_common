#! /usr/bin/env python
# -*- coding: utf-8 -*-
"""
Created on 04/12/14

@author: Sam Pfeiffer

Play stream of topic of Naoqi audio

"""
import rospy
# sudo apt-get install python-alsaaudio
import alsaaudio
from naoqi_msgs.msg import AudioBuffer

NAOQI_AUDIO_TOPIC = '/naoqi_microphone/audio_raw'

class PlayNaoqiAudioTopic():
    def __init__(self):
        rospy.loginfo("Getting audio card...")
        self.device = alsaaudio.PCM()
        self.device.setformat(alsaaudio.PCM_FORMAT_S16_LE) # format corresponding to the buffers in the bag => if you use nao_sensors node, 
        self.device_configured = False
        rospy.loginfo("Done!")
        # the setting (format, channels, rate) can be done only once (and should only most probably)
        rospy.loginfo("Setting up subscriber to " + NAOQI_AUDIO_TOPIC)
        self.sub = rospy.Subscriber(NAOQI_AUDIO_TOPIC, AudioBuffer, self.audio_cb)
        rospy.loginfo("Done!")
        

    def audio_cb(self, msg):
        rospy.loginfo("Callback received!")
        if not self.device_configured:
            self.device.setchannels(len(msg.channelMap))
            self.device.setrate(msg.frequency)
            self.device_configured = True
        tmp = list(msg.data)
        # Empirically I've seen that every msg has a data field with 10920 items
        # every item is a sample from each channel
        # in my bag there are 4 channels:
        # frequency: 16000
        # channelMap: [0, 2, 1, 4]
        # [CHANNEL_FRONT_LEFT, CHANNEL_FRONT_RIGHT, CHANNEL_FRONT_CENTER, CHANNEL_REAR_CENTER]
        # This means that 10920 / 4 = 2730 samples for each channel
        # which 16000 / 2730 = 5, so we have 1/5 of a second in every message
        # We could make a little buffer to have better audio? (right now it stops all the time)
        dataBuff = ""
        
        for i in range (0,len(tmp)) :
            if tmp[i]<0 :
                tmp[i]=tmp[i]+65536
            dataBuff = dataBuff + chr(tmp[i]%256)
            dataBuff = dataBuff + chr( (tmp[i] - (tmp[i]%256)) /256)
        
        self.device.write(dataBuff)

if __name__=="__main__":
    rospy.init_node('play_audio_msgs')
    
    PNAT = PlayNaoqiAudioTopic()
    rospy.spin()


