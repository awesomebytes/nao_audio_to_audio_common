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
        self.audio_buffer = []
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
        self.audio_buffer.extend(msg.data)
        #rospy.loginfo("len(msg.data):" + str(len(msg.data)))

        
    def run(self):
        # Empirically I've seen that every msg has a data field with 10920 items
        # every item is a sample from each channel
        # in my bag there are 4 channels:
        # frequency: 16000
        # channelMap: [0, 2, 1, 4]
        # [CHANNEL_FRONT_LEFT, CHANNEL_FRONT_RIGHT, CHANNEL_FRONT_CENTER, CHANNEL_REAR_CENTER]
        # This means that 10920 / 4 = 2730 samples for each channel
        # which 16000 / 2730 = 5, so we have 1/5 of a second in every message
        # We could make a little buffer to have better audio? (right now it stops all the time)
        # Also:
        # rostopic hz /naoqi_microphone/audio_raw
        # average rate: 5.065
        #     min: 0.124s max: 0.242s std dev: 0.05200s window: 4
        # average rate: 4.644
        #     min: 0.000s max: 0.370s std dev: 0.10493s window: 9
        # average rate: 4.901
        #     min: 0.000s max: 0.434s std dev: 0.11124s window: 15

        one_audio_data_size = 10920
        one_second = one_audio_data_size * 5
        ten_seconds = one_second * 10
        seconds_to_buffer = ten_seconds
        while not rospy.is_shutdown():
            #rospy.loginfo("len(self.audio_buffer):" + str(len(self.audio_buffer)))
            if len(self.audio_buffer) >= seconds_to_buffer: # if one second of audio is in the buffer
                rospy.loginfo("Buffer has " + str(  len(self.audio_buffer) / one_second  ) + "s of audio, playing.")
                tmp = list(self.audio_buffer)
                self.audio_buffer = self.audio_buffer[seconds_to_buffer:] # Leaving whatever extra data is there
                dataBuff = ""
                for i in range (0,len(tmp)) :
                    if tmp[i]<0 :
                        tmp[i]=tmp[i]+65536
                    dataBuff = dataBuff + chr(tmp[i]%256)
                    dataBuff = dataBuff + chr( (tmp[i] - (tmp[i]%256)) /256)
                self.device.write(dataBuff)
                

if __name__=="__main__":
    rospy.init_node('play_audio_msgs_buffered_')
    
    PNAT = PlayNaoqiAudioTopic()
    PNAT.run()


