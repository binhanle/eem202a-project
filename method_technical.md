---
title:  Technical Approach
layout: template
filename: method_technical
--- 

## Table of Contents
* [Methodology](#methodology)
  * [Media Capturing](#media-capturing)
  * [Demultiplexing of Video and Audio Files](#demultiplexing-of-video-and-audio-files)
  * [Feature Processing](#feature-processing)
    * [Mouth Aspect Ratio](#mouth-aspect-ratio)
    * [Voice Activity Detection](#voice-activity-detection)
    * [Cross-Correlation](#cross-correlation)
  * [Time Offset Injection](#time-offset-injection)
* [Datasets](#datasets)
* [Training and Optimization of Parameters](#training-and-optimization-of-parameters)



### Methodology

#### Media Capturing

In order to capture what a user would see and hear from the video, thereby encompassing all latency that could be introduced between the audio/video files, a recording device external to the video player must be introduced. The external recording can be handled by the same computer, or by an external device. Screen recording software such as Camtasia and OBS (for Windows, Mac, FFmpeg) or built-in screen recording for iOS and Android can directly record the video, while using a built-in microphone to record the audio. This method relies on the use of an internal microphone, which is available in most, but not all common computing devices. This can also be carried out by an external device, which can be as sophisticated and customized as need be for the purposes of the recording. Both methods have their advantages and disadvantages, but the simplicity of on screen recording and the ability to compile all software into a convenient and deployable package beats the possible customization provided by an external device and the problem case where a user may not have an internal microphone available to use.

FFmpeg was selected for screen recording, due to its versatility across operating systems and the ability to have it controlled by some backend process. "Insert details about screen capture"

<p align="center">
	<img src="https://github.com/binhanle/eem202a-project/blob/gh-pages/Images/media_capture.png"/>
	<br/>
	<strong>Media Capture Technique</strong>
</p>

This functionality has been built, but was not implemented as a part of this project's demonstration system. After some research, it was determined that most streaming services these days do not have API support for backend audio delay injection. The FFmpeg screen capture can be used to capture a certain length of video and audio, which is processed, and then a time offset is determined. However, this cannot be directly reinjected. For the purposes of this project, it is assumed that the entire video file is available for processing. A future development would be the integration of the media capturing with the rest of the system when some version of the delay injection APIs are released.

#### Demultiplexing of Video and Audio Files

In order to properly run a neural network analysis and subsequent shifting of the video and audio stream files, the original video file must be demultiplexed. FFmpeg is a powerful tool which provides the capability to strip away the audio from a video file, while also allowing them to be spliced back together following the calculated time shift. Once these files have been isolated, they can be further processed. Through multiple stages of processing for each file, the relevant information can be separately extracted and processed. By extracting information from the audio stream and the video frames, the computational complexity is also drastically reduced.

#### Feature Processing

This project focuses on videos that portray a single full frontal speaker, in case where both the audio leads and lags the video. Initially, the plan was to only focus on cases where audio lags the video, but the selected approach proved to be robust. For the purposes of correcting this audio and video stream offset, two major feature extraction techniques were applied: mouth aspect ratio computation (MAR) and voice activity detection (VAD). The leading hypothesis was that the various start and end points of identified speech in the video could be correlated with the start and end points of speech in the audio. If there was some sort of offset between the two streams, a cross-correlation technique could be applied to find the optimal allignment, and hence the time offset.

##### Mouth Aspect Ratio

This calculation is broken up into two steps: the face detection and the MAR computation. The dlib python module is first used to extract the detected face from each frame. This face is then matched to a shape landmark prediction file, where each coordinate in the file corresponds to a specific point on the face. The coordinates for the mouth are extracted from this file, and for each frame the MAR is computed based on the euclidian distances between the opposite horizontal landmarks and the euclidian distances between the opposite vertical landmarks of the mouth. 

<p align="center">
	<img height="400" src="https://github.com/binhanle/eem202a-project/blob/gh-pages/Images/mar_descriptor.png"/>
	<br/>
	<strong>MAR Example</strong>
</p>
<br/>

The output from the MAR function is a list of values corresponding to the aspect ratio of the mouth. Its size is equal to the total number of frames. 
The mouth aspect ratio implementation was inspired by the following: https://github.com/mauckc/mouth-open

##### Voice Activity Detection

Voice activity detectors are very common for speech processing, specifically when it comes to speech recognition in devices like Siri or Alexa. WebRTCVAD was the python module used to take care of the voice activity detection, which was created for the Google WebRTC project and is supposedly one of the best VADs available. The selected VAD takes a 10ms section of audio at a time and assigns a binary 1 or 0 based on whether speech was detected during that period of time. It also takes an aggresiveness parameter argument of 0, 1, 2, or 3 which determines how strictly it classifies periods of sound as speech or silence. A higher VAD aggresiveness will generally result in less segments being classified as speech. 

<p align="center">
	<img src="https://github.com/binhanle/eem202a-project/blob/gh-pages/Images/vad_descriptor.png"></img>
	<br/>
	<strong>VAD Detection Example 
		<br/> 
		Source: http://practicalcryptography.com/miscellaneous/machine-learning/voice-activity-detection-vad-tutorial/
	</strong>
</p>
<br/>

The extracted audio from the video file is fed through the VAD, and the output is a binary list corresponding to the sections of detected speech and silence. Following this, the data is resampled and smoothed to match the number of frames in the video file. 
The implementation was inspired by the following: https://github.com/wiseman/py-webrtcvad


##### Cross-Correlation

The voice activity detection and mouth aspect ration computation both provide two lists of the same size. A cross-correlation is run to determine the optimal allignment between these two vectors, and determine what time offset (if any) exists between them. The following two figures demonstrate an example of this process:

<p align="center">
	<img src="https://github.com/binhanle/eem202a-project/blob/gh-pages/Images/av_data.png"></img>
	<br/>
	<strong>MAR and VAD Output for 0ms Offset Video</strong>
</p>
<br/>

<p align="center">
	<img src="https://github.com/binhanle/eem202a-project/blob/gh-pages/Images/cross_corr.png"></img>
	<br/>
	<strong>Cross-Correlation of Video and Audio Features for 0ms Offset Video</strong>
</p>
<br/>

#### Time Offset Injection

Once the required time shift has been identified by the neural network output, the FFmpeg tool is used again to inject the lead or lag in the audio file. The delay-injected audio and original video files are then combined.  The original video file is not modified in any way, and instead a new synchronized video file is created.

The following diagram summarizes the data pipeline:

<p align="center">
	<img src="https://github.com/binhanle/eem202a-project/blob/gh-pages/Images/strat2.png"></img>
	<br/>
	<strong>System Block Diagram</strong>
</p>

### Datasets

As it was mentioned before, the scope of this project will be limited to videos that feature a full-frontal view of a single speaker. These videos used in the training and testing datasets were a combination of videos found on the internet, and videos filmed ourselves. By verifying that the implementation works on both types of videos, we are able to show the robustness of our system on different types of full-frontal speaker videos. By using the pydub python module, silence could be manually inserted at the beginning or the end of the audio file to artifically inject offsets between the video and audio streams. This allows for dozens of datasets to be created from a single base video. FFmpeg was used to separate the original video and audio streams, and to also combine the shifted audio streams with the original video stream to create the data sets. The links to the Google Drive with the data files can be found below:

https://drive.google.com/drive/folders/1clnnBK1GhL06HXMhgHZnuj5A2MMUhfNW?usp=sharing

### Training and Optimization of Parameters
