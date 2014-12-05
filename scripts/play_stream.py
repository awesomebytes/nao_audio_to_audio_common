#! /usr/bin/env python
# -*- coding: utf-8 -*-
"""
Created on 04/12/14

@author: Sam Pfeiffer

Play stream of topic of Naoqi audio

"""
import rospy
import ossaudiodev
from naoqi_msgs.msg import AudioBuffer

NAOQI_AUDIO_TOPIC = '/naoqi_microphone/audio_raw'

class PlayNaoqiAudioTopic():
    def __init__(self):
        # To get rid of:
        # self.device = ossaudiodev.open('w')
        # IOError: [Errno 2] No such file or directory: '/dev/dsp'
        # I tried installing: sudo apt-get install alsa-oss
        # and executing:
        # aoss python play_stream.py
        # but it didn't work
        # Then I tried:
        #  padsp ./play_stream.py
        # and it did kind of work
        self.device = ossaudiodev.open('w')
        #format = ossaudiodev.AFMT_S16_LE
        #self.device.setfmt(ossaudiodev.AFMT_S16_LE) # format corresponding to the buffers in the bag => if you use nao_sensors node, 
        self.device_configured = False
        # Let's assume msg is a ros AudioBuffer message

        
        # the setting (format, channels, rate) can be done only once
        rospy.loginfo("Setting up sub")
        self.sub = rospy.Subscriber(NAOQI_AUDIO_TOPIC, AudioBuffer, self.audio_cb)
        rospy.loginfo("Done!")
        

    def audio_cb(self, msg):
        rospy.loginfo("Callback received!")
        if not self.device_configured:
            #self.device.channels(len(msg.channelMap))
            #self.device.speed(msg.frequency)
            self.device_configured = True
            
        tmp = list(msg.data)
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


