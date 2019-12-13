# Video and Audio Synchronization
UCLA ECE M202A Project, Fall 2019

## Table of Contents
* [Authors](#authors)
* [Abstract](#abstract)
* [Prior Work](#prior-work)
* [Technical Approach (Methodology, Data, Validation)](#technical-approach-methodology-data-validation)
* [Timeline](#timeline)
* [Deliverables](#deliverables)
* [Success Metrics](#success-metrics)
* [References](#references)

## Authors
- Mark Chen
- An Le
- Loic Maxwell

## Abstract
Popular streaming services, such as YouTube and Twitch, often receive reports of video and audio offsets from their users. However, from their end, the server-side video and audio files are perfectly synchronized, and latencies are actually introduced unpredictably before both video and audio are outputted from these users’ edge devices. Those latencies are often non-deterministic and can only truly be resolved by performing a real-time analysis and subsequent timing corrections on both video and audio inputs at the users’ side. The purpose of this project is to quickly analyze a video’s audio cues and determine how much offset exists between the audio and video files, then perform the necessary time shift to realign them. By using audio and screen capture technology, we are able to identify what a user sees and hears. Specific features are then extracted from the captured and audio and video streams, and passed through a trained neural network to determine the required time shift. This feedback system will run continuously during a streaming session and properly correct the timings of video and audio streams as soon as an offset is identified.

## Prior Work
Audio-visual synchronization is a major factor when determining the quality of a streaming service. Traditionally, scientists work on temporal coordination between audio and video streams to minimize the impact of cumulative latencies at end-users’ multimedia devices [1,2]. However, this approach often requires knowledge of the data transmission protocol applied on audio and video streams and derivations of complicated timing equations. Moreover, the outcome of synchronization can vary if latencies are introduced randomly across the entire streaming path [3]. To bypass these complications while improving the results of audio-visual synchronization, researchers begin to incorporate feature-based analysis on audio and video streams.

The emergence of machine learning helps boost the uses of feature-based analysis in audio-visual synchronization. A variety of machine learning models become available for extracting definitive features that can correlate audio and visual data based on the entailed events. For instance, Zhao et al. introduce a system that can locate the region of pixels on a video frame that correspond to a sound source in the audio stream [4]. Another notable example is the Lip Reading machine learning model from Torfi et al. that matches human voices to lip motions [5]. With the advantage of utilizing feature-based information to correlate audio and video streams, one can likely design a machine learning model to classify whether a streaming service has its video and audio synced at a good accuracy.  

"Insert SyncNet Paper Info"

A couple of works had proposed their own trained machine learning systems to detect the presence of audio-visual synchronization in some given pairs of video and audio inputs [6,7]. Nevertheless, there is limited information of concrete methods that can be used to resolve the detected time offsets between a pair of video and audio inputs. Given this point, there is a need to develop a working audio-visual synchronization system that enables follow-up synchronization after the detection of a time offset.    


## Attempted but Discontinued Approaches

### Direct CNN Approach

This was the first attempted approach towards solving the audio/video synchronization problem. This was also the one highlighted in the initial proposal. The audio and video were trained separately in two convolutional neural networks (CNNs).

<p align="center">
	<img src="https://github.com/binhanle/eem202a-project/blob/master/Images/strat1.png"></img>
</p>

The reason why we did not pursue this approach is...

This approach can be found under:
"Name for Strategy 1 colab notebook"

### SyncNet Approach

The third attemtped strategy was based on the SyncNet paper. They were able to accomplish audio-video synchronization for a window size of only 5 frames. 

<p align="center">
	<img src="https://github.com/binhanle/eem202a-project/blob/master/Images/strat3.png"></img>
	<strong>Source: https://www.robots.ox.ac.uk/~vgg/publications/2016/Chung16a/chung16a.pdf</strong>
</p>
	
The reason why we did not pursue this strategy is...

This approach can be found under:
"Name for Strategy 3 colab notebook"

## Technical Approach (Methodology, Data, Validation)

### Methodology

#### Media Capturing

In order to capture what a user would see and hear from the video, thereby encompassing all latency that could be introduced between the audio/video files, a recording device external to the video player must be introduced. The external recording can be handled by the same computer, or by an external device. Screen recording software such as Camtasia and OBS (for Windows, Mac, FFmpeg) or built-in screen recording for iOS and Android can directly record the video, while using a built-in microphone to record the audio. This method relies on the use of an internal microphone, which is available in most, but not all common computing devices. This can also be carried out by an external device, which can be as sophisticated and customized as need be for the purposes of the recording. Both methods have their advantages and disadvantages, but the simplicity of on screen recording and the ability to compile all software into a convenient and deployable package beats the possible customization provided by an external device and the problem case where a user may not have an internal microphone available to use.

FFmpeg was selected for screen recording, due to its versatility across operating systems and the ability to have it controlled by some backend process. "Insert details about screen capture"

<p align="center">
	<img src="https://github.com/binhanle/eem202a-project/blob/master/Images/media_capture.png"></img>
	<strong>Media Capture Technique</strong>
</p>

This functionality has been built, but was not implemented as a part of this project's demonstration system. After some research, it was determined that most streaming services these days do not have API support for backend audio delay injection. The FFmpeg screen capture can be used to capture a certain length of video and audio, which is processed, and then a time offset is determined. However, this cannot be directly reinjected. For the purposes of this project, it is assumed that the entire video file is available for processing. A future development would be the integration of the media capturing with the rest of the system when some version of the delay injection APIs are released.

#### Demultiplexing of Video/Audio Files

In order to properly run a neural network analysis and subsequent shifting of the video and audio stream files, the original video file must be demultiplexed. FFmpeg is a powerful tool which provides the capability to strip away the audio from a video file, while also allowing them to be spliced back together following the calculated time shift. Once these files have been isolated, they can be further processed. Through multiple stages of processing for each file, the relevant information can be separately extracted and processed. By extracting information from the audio stream and the video frames, the computational complexity is also drastically reduced.

#### Processing, Features, and Cross-Correlation

This project focuses on videos that portray a single full frontal speaker, in case where both the audio leads and lags the video. Initially, the plan was to only focus on cases where audio lags the video, but the selected approach proved to be robust. For the purposes of correcting this audio and video stream offset, two major feature extraction techniques were applied: mouth aspect ratio computation (MAR) and voice activity detection (VAD). The leading hypothesis was that the various start and end points of identified speech in the video could be correlated with the start and end points of speech in the audio. If there was some sort of offset between the two streams, a cross-correlation technique could be applied to find the optimal allignment, and hence the time offset.

##### Mouth Aspect Ratio

The mouth aspect ratio was implemented based on the following:
https://github.com/mauckc/mouth-open

This calculation is broken up into two steps: the face detection and the MAR computation. The dlib python module is first used to extract the detected face from each frame. This face is then matched to a shape landmark prediction file, where each coordinate in the file corresponds to a specific point on the face. The coordinates for the mouth are extracted from this file, and for each frame the MAR is computed based on the euclidian distances between the opposite horizontal landmarks and the euclidian distances between the opposite vertical landmarks of the mouth. 

<p align="center">
	<img src="https://github.com/binhanle/eem202a-project/blob/master/Images/media_capture.png"></img>
	<strong>MAR Example</strong>
</p>

The output from the MAR function is a list of values corresponding to the aspect ratio of the mouth. Its size is equal to the total number of frames. 

##### Voice Activity Detection

Voice activity detectors are very common for speech processing, specifically when it comes to speech recognition in devices like Siri or Alexa. WebRTCVAD was the python module used to take care of the voice activity detection, which was created for the Google WebRTC project and is supposedly one of the best VADs available. The selected VAD takes a 10ms section of audio at a time and assigns a binary 1 or 0 based on whether speech was detected during that period of time. It also takes an aggresiveness parameter argument of 0, 1, 2, or 3 which determines how strictly it classifies periods of sound as speech or silence. A higher VAD aggresiveness will generally result in less segments being classified as speech. 

<p align="center">
	<img src="https://github.com/binhanle/eem202a-project/blob/master/Images/vad_descriptor.png"></img>
	<strong>VAD Detection Example. Source: http://practicalcryptography.com/miscellaneous/machine-learning/voice-activity-detection-vad-tutorial/</strong>
</p>

The extracted audio from the video file is fed through the VAD, and the output is a binary list corresponding to the sections of detected speech and silence. Following this, the data is resampled and smoothed to match the frame length of the video file. 


##### Cross-Correlation

The voice activity detection was able to produce
#### Time injection

Once the required time shift has been identified by the neural network output, the FFmpeg tool is used again to inject the lead or lag in the audio file. The delay-injected audio and original video files are then combined.  The original video file is not modified in any way, and instead a new synchronized video file is created.

The following diagram summarizes the data pipeline:

<p align="center">
	<img src="https://github.com/binhanle/eem202a-project/blob/master/Images/strat2.png"></img>
	<strong>System Block Diagram</strong>
</p>

### Data Sets for Training/Validation

As it was mentioned before, the scope of this project will be limited to videos that feature a full-frontal view of a single speaker. These videos used in the training and testing datasets were a combination of vid. For the purposes of training the system

### Training, Optimization of Parameters


### Testing the

A test set for the neural network provides the best measure of its performance. The calculated outputs (labels) can be compared to their known ones, and an error value can be computed for each set of input features. The average error across all outputs will be used to determine the best training set given this first set of data, according to k-fold cross validation. One of the primary goals is to keep this error below 40 ms for all output values, which would fall within a threshold of non-detectability from the perspective of a viewer [9]. In other words, a human would not recognize any synchronization problems if the out-of-sync audio and video are within 40ms of each other. If for some reason this goal is not achievable given the current data, the audio lead increment for creating training data will be decreased from 1ms to 0.5ms. If this does not resolve the issue, then other approaches will have to be taken (shorter increment, more data sets, more features, etc.).

Following this process, a second set of test videos will be acquired. These will test the accuracy of the trained network. With a 40 ms error tolerance, it is possible to have a success rate of over 90% for all test cases. Once this has been accomplished, the next step is to test on random videos found on the internet (e.g. YouTube). They will still feature full-frontal shots of a single speaker, but this will test the versatility of the neural network.


## Test Results


### Processing the entire clip:



### Using a Variable Window Size

"Insert computational time(window size) vs. accuracy info"

## Limitations

## Next Steps

## Timeline

### Legend

| Status | Color |
| --- | :---: |
| Scheduled | ![blue](https://placehold.it/32/3d85c6/000000?text=+) |
| In progress | ![yellow](https://placehold.it/32/f1c232/000000?text=+) |
| Completed | ![green](https://placehold.it/32/6aa84f/000000?text=+) |
| Aborted | ![red](https://placehold.it/32/cc0000/000000?text=+) |

### Schedule

| Major Objective with Subtasks | Week 5 | Week 6 | Week 7 | Week 8 | Week 9 | Week 10 |
| --- | :---: | :---: | :---: | :---: | :---: | :---: |
| **I. Datasets** |
| Find datasets online (full frontal, single person): Loic, Mark, An | ![green](https://placehold.it/32/6aa84f/000000?text=+) | ![green](https://placehold.it/32/6aa84f/000000?text=+) | ![green](https://placehold.it/32/6aa84f/000000?text=+) | ![green](https://placehold.it/32/6aa84f/000000?text=+)
| Collect own datasets (full frontal, single person): Loic, Mark, An | | | | |![green](https://placehold.it/32/6aa84f/000000?text=+)|![green](https://placehold.it/32/6aa84f/000000?text=+)|
| Experiment with video streaming sites, to test real-time performance (optional): Loic, Mark, An | | | | ![red](https://placehold.it/32/cc0000/000000?text=+) | ![red](https://placehold.it/32/cc0000/000000?text=+) |
| **II. Capture audio and video from user end** |
| Select hardware/software tools: Mark | ![green](https://placehold.it/32/6aa84f/000000?text=+) | ![green](https://placehold.it/32/6aa84f/000000?text=+) |
| Implementation (optional): Mark | | | | ![green](https://placehold.it/32/6aa84f/000000?text=+) | ![green](https://placehold.it/32/6aa84f/000000?text=+) |
| **III. Handle the captured audio and video inputs** |
| Determine what tools to use for demuxing audio/video of .mp4 files: Mark | ![green](https://placehold.it/32/6aa84f/000000?text=+) | ![green](https://placehold.it/32/6aa84f/000000?text=+) |
| Create translation into a usable format for the feature extraction program: Mark | | ![green](https://placehold.it/32/6aa84f/000000?text=+) | ![green](https://placehold.it/32/6aa84f/000000?text=+) |
| Expand to other video formats (optional): Mark, An, Loic | | | | | ![red](https://placehold.it/32/cc0000/000000?text=+) | ![red](https://placehold.it/32/cc0000/000000?text=+) |
| **IV. Data Processing and Time Offset Computation** |
| Define features to extract from video/audio: An, Loic, Mark | ![green](https://placehold.it/32/6aa84f/000000?text=+) | ![green](https://placehold.it/32/6aa84f/000000?text=+) |
| Build software to perform feature extraction: An | | ![green](https://placehold.it/32/6aa84f/000000?text=+) | ![green](https://placehold.it/32/6aa84f/000000?text=+) |
| Cross-correlation implementation: An | | | | ![green](https://placehold.it/32/6aa84f/000000?text=+) |
| Complete processing pipeline: An, Mark, Loic | | ![green](https://placehold.it/32/6aa84f/000000?text=+) | ![green](https://placehold.it/32/6aa84f/000000?text=+) | ![green](https://placehold.it/32/6aa84f/000000?text=+) | ![green](https://placehold.it/32/6aa84f/000000?text=+) |
| Optimization on training data: An | | | | | ![green](https://placehold.it/32/6aa84f/000000?text=+) |
| **V. Create wrapper program** |
| Define how to handle time injection: Loic | | | | ![green](https://placehold.it/32/6aa84f/000000?text=+) |
| Integrate the processing, resulting delay injection, and video player: Loic | | | | ![green](https://placehold.it/32/6aa84f/000000?text=+) | ![green](https://placehold.it/32/6aa84f/000000?text=+) |
| **VI. Translate into real-time system (optional)** |
| Make video/audio capture and processing run in the background: Mark | | | | | ![green](https://placehold.it/32/6aa84f/000000?text=+) | ![green](https://placehold.it/32/6aa84f/000000?text=+) |
| Implement real time delay injection: Loic | | | | | ![red](https://placehold.it/32/cc0000/000000?text=+) | ![red](https://placehold.it/32/cc0000/000000?text=+) |

### Objectives

#### Primary:
- Develop a machine-learning based model to properly recognize and quantify video and audio time offsets for videos of a single speaker in full-frontal view, with an error less than 40ms
- Define a performance spectrum of the model for varying delays between the audio and video streams, to determine the range of its best use case

#### Stretch:

- Create a backend program to run in real time, to capture the on screen video, determination in time offset, and make the necessary correction, all automatically
- Expand analysis to similar video types, acquired from various web sources (YouTube)
- Implement delay compensation for a common video streaming service

## Deliverables
- The training/validation set -- full-frontal recordings of Loic, An, and Mark
- Scripts that demultiplex audio/video files, preprocesses the audio/video streams, and inject time delay into video streams
- Suitable neural network architecture for determining time offset
- Program that restores audio/video synchronization offline
- Complete demonstration of synchronizing audio and video on a laggy live stream

## Success Metrics
- Errors in software (potentially a major obstacle as many packages and dependencies need to be installed/utilized correctly)
- Neural network training speed
- Error between estimated and actual time offset
- Seamlessness of audio/video resynchronization

## References
[1] Zhang, Jingfeng, LiI, Ying, and Wei, Yanna. “Efficient Media Synchronization Method for Video Telephony System.” IEEE 2008 International Conference on Audio, Language and Image Processing (2008): 1073–1076. http://dx.doi.org/10.1109/ICALIP.2008.4589974

[2] Kim, Cjanwoo, Seo, Kwang-Deok, and Sung, Wonyoong. “Efficient Media Synchronization Method for Video Telephony System.” IEICE Transactions on Information and Systems E89-D, no. 6 (2006): 1901–1905. https://doi.org/10.1093/ietisy/e89-d.6.1901.

[3] Elhajj, Imad H., Nadine Bou Dargham, Ning Xi, and Yunyi Jia. “Real-Time Adaptive Content-Based Synchronization of Multimedia Streams.” Advances in Multimedia 2011 (2011): 1–13. https://doi.org/10.1155/2011/914062.

[4] Zhao, Hang, Chuang Gan, Andrew Rouditchenko, Carl Vondrick, Josh McDermott, and Antonio Torralba. “The Sound of Pixels.” ArXiv:1804.03160 [Cs.CV] (2018). http://arxiv.org/abs/1804.03160.

[5] Torfi, Amirsina, Seyed Mehdi Iranmanesh, Nasser Nasrabadi, and Jeremy Dawson. “3D Convolutional Neural Networks for Cross Audio-Visual Matching Recognition.” IEEE Access 5 (2017): 22081–22091. https://doi.org/10.1109/ACCESS.2017.2761539.

[6] Marcheret, Etienne, Gerasimos Potamianos, Josef Vopicka, and Vaibhava Goel. “Detecting Audio-Visual Synchrony Using Deep Neural Networks,” INTERSPEECH 2015, 16th Annual Conference of the International Speech Communication Association (2015): 548–552.

[7] Chung, Joon Son, and Andrew Zisserman. “Out of Time: Automated Lip Sync in the Wild.” In Computer Vision – ACCV 2016 Workshops, edited by Chu-Song Chen, Jiwen Lu, and Kai-Kuang Ma, 10117:251–263. Cham: Springer International Publishing, 2017. https://doi.org/10.1007/978-3-319-54427-4_19.

[8] Sieranoja, Sami, Md Sahidullah, Tomi Kinnunen, Jukka Komulainen, and Abdenour Hadid. “Audiovisual Synchrony Detection with Optimized Audio Features.” In 2018 IEEE 3rd International Conference on Signal and Image Processing (ICSIP), 377–381. Shenzhen: IEEE, 2018. https://doi.org/10.1109/SIPROCESS.2018.8600424.

[9] EBU Recommendation R37-2007. “The relative timing of the sound and visual components of a television signal” (2007). https://tech.ebu.ch/docs/r/r037.pdf
