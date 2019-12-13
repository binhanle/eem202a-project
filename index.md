---
title: Introduction
layout: template
filename: index
--- 

## Table of Contents
* [Abstract](#abstract)
* [Prior Work](#prior-work)


## Abstract
Popular streaming services, such as YouTube and Twitch, often receive reports of video and audio offsets from their users. However, from their end, the server-side video and audio files are perfectly synchronized, and latencies are actually introduced unpredictably before both video and audio are outputted from these users’ edge devices. Those latencies are often non-deterministic and can only truly be resolved by performing a real-time analysis and subsequent timing corrections on both video and audio inputs at the users’ side. The purpose of this project is to quickly analyze a video’s audio cues and determine how much offset exists between the audio and video files, then perform the necessary time shift to realign them. By using audio and screen capture technology, we are able to identify what a user sees and hears. Once this information is collected, specific features relating to the speaker's mouth aspect ratio in the video stream and the voice activity detection of the audio stream are extracted. Then, a cross-correlation to determine the time offset between the two streams, and the original video file/stream can be realigned by advancing or delaying the audio.

## Prior Work
Audio-visual synchronization is a major factor when determining the quality of a streaming service. Traditionally, scientists work on temporal coordination between audio and video streams to minimize the impact of cumulative latencies at end-users’ multimedia devices [1,2]. However, this approach often requires knowledge of the data transmission protocol applied on audio and video streams and derivations of complicated timing equations. Moreover, the outcome of synchronization can vary if latencies are introduced randomly across the entire streaming path [3]. To bypass these complications while improving the results of audio-visual synchronization, researchers begin to incorporate feature-based analysis on audio and video streams.

The emergence of machine learning helps boost the uses of feature-based analysis in audio-visual synchronization. A variety of machine learning models become available for extracting definitive features that can correlate audio and visual data based on the entailed events. For instance, Zhao et al. introduce a system that can locate the region of pixels on a video frame that correspond to a sound source in the audio stream [4]. Another notable example is the Lip Reading machine learning model from Torfi et al. that matches human voices to lip motions [5]. With the advantage of utilizing feature-based information to correlate audio and video streams, one can likely design a machine learning model to classify whether a streaming service has its video and audio synced at a good accuracy.

A couple of works had proposed their own trained machine learning systems to detect the presence of audio-visual synchronization in some given pairs of video and audio inputs [6,7]. Nevertheless, there is limited information of concrete methods that can be used to resolve the detected time offsets between a pair of video and audio inputs. Given this point, there is a need to develop a working audio-visual synchronization system that enables follow-up synchronization after the detection of a time offset.    
