nao_audio_to_audio_common
=========================

Just a container for a script that takes Naoqi AudioBuffer messages and converts (kinda) to audio_common AudioData message

WARNING: This does not actually work!

I execute:

    roslaunch audio_play play.launch 

From [audio_common](https://github.com/ros-drivers/audio_common) package, which listens to
```/audio```  topic.

Then I execute:

    rosrun nao_audio_to_audio_common msg_converter.py

Which mainly gets the messages from [Naoqi audio](https://github.com/ros-naoqi/naoqi_bridge/blob/master/naoqi_msgs/msg/AudioBuffer.msg) which I have in a rosbag that you can find in this repo ```microNAO_2014-12-04-18-10-49.bag```.

I play it with:

    rosbag play microNAO_2014-12-04-18-10-49.bag

And _converts them_ to audio_common_msgs [AudioData](https://github.com/ros-drivers/audio_common/blob/hydro-devel/audio_common_msgs/msg/AudioData.msg) message. The "conversion" is just uint16 to uint8... which is probably completely wrong. But I wanted to see if anything would actually sound doing this... and no, it didn't work.

