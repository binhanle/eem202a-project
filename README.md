# Video and Audio Synchronization
UCLA ECE M202A Project, Fall 2019

https://binhanle.github.io/eem202a-project/

## Table of Contents
* [Authors](#authors)
* [Abstract](#abstract)
* [Prior Work](#prior-work)
* [Technical Approach (Methodology, Data, Validation)](#technical-approach-methodology-data-validation)
* [Results](#results)
* [Strength and Weakness](#strength-and-weakness)
* [Future Directions](#future-directions)
* [Timeline](#timeline)
* [Deliverables](#deliverables)
* [Success Metrics](#success-metrics)
* [References](#references)

## Authors
- Mark Chen
- An Le
- Loic Maxwell

## Abstract
Popular streaming services, such as YouTube and Twitch, often receive reports of video and audio offsets from their users. However, from their end, the server-side video and audio files are perfectly synchronized, and latencies are actually introduced unpredictably before both video and audio are outputted from these users’ edge devices. Those latencies are often non-deterministic and can only truly be resolved by performing a real-time analysis and subsequent timing corrections on both video and audio inputs at the users’ side. The purpose of this project is to quickly analyze a video’s audio cues and determine how much offset exists between the audio and video files, then perform the necessary time shift to realign them. By using audio and screen capture technology, we are able to identify what a user sees and hears. Once this information is collected, specific features relating to the speaker's mouth aspect ratio in the video stream and the voice activity detection of the audio stream are extracted. Then, a cross-correlation to determine the time offset between the two streams, and the original video file/stream can be realigned by advancing or delaying the audio.

## Prior Work
Audio-visual synchronization is a major factor when determining the quality of a streaming service. Traditionally, scientists work on temporal coordination between audio and video streams to minimize the impact of cumulative latencies at end-users’ multimedia devices [1,2]. However, this approach often requires knowledge of the data transmission protocol applied on audio and video streams and derivations of complicated timing equations. Moreover, the outcome of synchronization can vary if latencies are introduced randomly across the entire streaming path [3]. To bypass these complications while improving the results of audio-visual synchronization, researchers begin to incorporate feature-based analysis on audio and video streams.

The emergence of machine learning helps boost the uses of feature-based analysis in audio-visual synchronization. A variety of machine learning models become available for extracting definitive features that can correlate audio and visual data based on the entailed events. For instance, Zhao et al. introduce a system that can locate the region of pixels on a video frame that correspond to a sound source in the audio stream [4]. Another notable example is the Lip Reading machine learning model from Torfi et al. that matches human voices to lip motions [5]. With the advantage of utilizing feature-based information to correlate audio and video streams, one can likely design a machine learning model to classify whether a streaming service has its video and audio synced at a good accuracy.

A couple of works had proposed their own trained machine learning systems to detect the presence of audio-visual synchronization in some given pairs of video and audio inputs [6,7]. Nevertheless, there is limited information of concrete methods that can be used to resolve the detected time offsets between a pair of video and audio inputs. Given this point, there is a need to develop a working audio-visual synchronization system that enables follow-up synchronization after the detection of a time offset.    


## Attempted but Discontinued Approaches

### Direct CNN Approach

This was the first attempted approach towards solving the audio/video synchronization problem. This was also the one highlighted in the initial proposal. The model consists of two CNNs, a concatenation step to join the branches, several fully-connected layers, and a linear output neuron that represents the frame offset between the audio and video inputs. The CNNs were trained simultaneously on video frame windows and spectrograms from their corresponding audio segments.

<p align="center">
	<img src="https://github.com/binhanle/eem202a-project/blob/master/Images/strat1.png" />
	<br/>
	<strong>CNN Architecture</strong>
</p>

We did not pursue this approach because initially, the model was trained on grayscale faces, which filled the neural network with irrelevant information besides the mouth movement. Despite applying the following fixes, the model could not achieve an adequate fit:

- Cropping out the mouth
- Using the difference between frames instead of the frames themselves
- Increasing the window size
- Adding more convolutional and fully-connected layers
- Training on only one video
- Limiting the maximum offset

Therefore, it is likely that our initial architecture is not suitable for this problem.

This approach can be found under:
"Name for Strategy 1 colab notebook"

### SyncNet Approach

The third attemtped strategy was based on the SyncNet paper [7]. The authors were able to accomplish audio-video synchronization at an accuracy of 81% with a window size of only 5 frames. SyncNet consists of two similar DNNs that output size-256 vectors. The inputs are a five-frame window and the MFCC features of the corresponding audio segment. The L2 distance between the output vectors determines whether an audio and video pair is synchronized. SyncNet is trained on genuine (in-sync) and false (out-of-sync) pairs. To find the audio-video offset of a particular video, one must extract audio and video pairs from the video, feed them to SyncNet, average the L2 distances over a set time, and repeat by manually sliding the audio and/or the video stream. The offset that returns the least average L2 distance is most likely the correct one.

<p align="center">
	<img src="https://github.com/binhanle/eem202a-project/blob/master/Images/strat3.png"/>
	<br/>
	<strong>Source: https://www.robots.ox.ac.uk/~vgg/publications/2016/Chung16a/chung16a.pdf</strong>
</p>
	
This strategy was not pursued for the following reasons:

- We had inadequate resources. The GPU provided by Google Colab barely had enough memory for training audio and video pairs from one video. In contrast, the authors trained SyncNet on hundreds of hours of video using high-end hardware.
- Although the SyncNet architecture was implemented on Google Colab using the parameters described in the paper, the model overfit. Possible factors include not enough training data, an unforeseen bug in the pair generation code, and poor video quality.

This approach can be found under:
"Name for Strategy 3 colab notebook"

## Technical Approach (Methodology, Data, Validation)

### Methodology

#### Media Capturing

In order to capture what a user would see and hear from the video, thereby encompassing all latency that could be introduced between the audio/video files, a recording device external to the video player must be introduced. The external recording can be handled by the same computer, or by an external device. Screen recording software such as Camtasia and OBS (for Windows, Mac, FFmpeg) or built-in screen recording for iOS and Android can directly record the video, while using a built-in microphone to record the audio. This method relies on the use of an internal microphone, which is available in most, but not all common computing devices. This can also be carried out by an external device, which can be as sophisticated and customized as need be for the purposes of the recording. Both methods have their advantages and disadvantages, but the simplicity of on screen recording and the ability to compile all software into a convenient and deployable package beats the possible customization provided by an external device and the problem case where a user may not have an internal microphone available to use.

FFmpeg was selected for screen recording, due to its versatility across operating systems and the ability to have it controlled by some backend process. "Insert details about screen capture"

<p align="center">
	<img src="https://github.com/binhanle/eem202a-project/blob/master/Images/media_capture.png"/>
	<br/>
	<strong>Media Capture Technique</strong>
</p>

This functionality has been built, but was not implemented as a part of this project's demonstration system. After some research, it was determined that most streaming services these days do not have API support for backend audio delay injection. The FFmpeg screen capture can be used to capture a certain length of video and audio, which is processed, and then a time offset is determined. However, this cannot be directly reinjected. For the purposes of this project, it is assumed that the entire video file is available for processing. A future development would be the integration of the media capturing with the rest of the system when some version of the delay injection APIs are released.

#### Demultiplexing of Video/Audio Files

In order to properly run a neural network analysis and subsequent shifting of the video and audio stream files, the original video file must be demultiplexed. FFmpeg is a powerful tool which provides the capability to strip away the audio from a video file, while also allowing them to be spliced back together following the calculated time shift. Once these files have been isolated, they can be further processed. Through multiple stages of processing for each file, the relevant information can be separately extracted and processed. By extracting information from the audio stream and the video frames, the computational complexity is also drastically reduced.

#### Processing, Features, and Cross-Correlation

This project focuses on videos that portray a single full frontal speaker, in case where both the audio leads and lags the video. Initially, the plan was to only focus on cases where audio lags the video, but the selected approach proved to be robust. For the purposes of correcting this audio and video stream offset, two major feature extraction techniques were applied: mouth aspect ratio computation (MAR) and voice activity detection (VAD). The leading hypothesis was that the various start and end points of identified speech in the video could be correlated with the start and end points of speech in the audio. If there was some sort of offset between the two streams, a cross-correlation technique could be applied to find the optimal allignment, and hence the time offset.

##### Mouth Aspect Ratio

This calculation is broken up into two steps: the face detection and the MAR computation. The dlib python module is first used to extract the detected face from each frame. This face is then matched to a shape landmark prediction file, where each coordinate in the file corresponds to a specific point on the face. The coordinates for the mouth are extracted from this file, and for each frame the MAR is computed based on the euclidian distances between the opposite horizontal landmarks and the euclidian distances between the opposite vertical landmarks of the mouth. 

<p align="center">
	<img height="400" src="https://github.com/binhanle/eem202a-project/blob/master/Images/mar_descriptor.png"/>
	<br/>
	<strong>MAR Example</strong>
</p>
<br/>

The output from the MAR function is a list of values corresponding to the aspect ratio of the mouth. Its size is equal to the total number of frames. 
The mouth aspect ratio implementation was inspired by the following: https://github.com/mauckc/mouth-open

##### Voice Activity Detection

Voice activity detectors are very common for speech processing, specifically when it comes to speech recognition in devices like Siri or Alexa. WebRTCVAD was the python module used to take care of the voice activity detection, which was created for the Google WebRTC project and is supposedly one of the best VADs available. The selected VAD takes a 10ms section of audio at a time and assigns a binary 1 or 0 based on whether speech was detected during that period of time. It also takes an aggresiveness parameter argument of 0, 1, 2, or 3 which determines how strictly it classifies periods of sound as speech or silence. A higher VAD aggresiveness will generally result in less segments being classified as speech. 

<p align="center">
	<img src="https://github.com/binhanle/eem202a-project/blob/master/Images/vad_descriptor.png"></img>
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
	<img src="https://github.com/binhanle/eem202a-project/blob/master/Images/av_data.png"></img>
	<br/>
	<strong>MAR and VAD Output for 0ms Offset Video</strong>
</p>
<br/>

<p align="center">
	<img src="https://github.com/binhanle/eem202a-project/blob/master/Images/cross_corr.png"></img>
	<br/>
	<strong>Cross-Correlation of Video and Audio Features for 0ms Offset Video</strong>
</p>
<br/>

#### Time injection

Once the required time shift has been identified by the neural network output, the FFmpeg tool is used again to inject the lead or lag in the audio file. The delay-injected audio and original video files are then combined.  The original video file is not modified in any way, and instead a new synchronized video file is created.

The following diagram summarizes the data pipeline:

<p align="center">
	<img src="https://github.com/binhanle/eem202a-project/blob/master/Images/strat2.png"></img>
	<br/>
	<strong>System Block Diagram</strong>
</p>

### Data Sets

As it was mentioned before, the scope of this project will be limited to videos that feature a full-frontal view of a single speaker. These videos used in the training and testing datasets were a combination of videos found on the internet, and videos filmed ourselves. By verifying that the implementation works on both types of videos, we are able to show the robustness of our system on different types of full-frontal speaker videos. By using the pydub python module, silence could be manually inserted at the beginning or the end of the audio file to artifically inject offsets between the video and audio streams. This allows for dozens of datasets to be created from a single base video. FFmpeg was used to separate the original video and audio streams, and to also combine the shifted audio streams with the original video stream to create the data sets. The links to the Google Drive with the data files can be found below:

https://drive.google.com/drive/folders/1clnnBK1GhL06HXMhgHZnuj5A2MMUhfNW?usp=sharing

### Training, Optimization of Parameters


## Results

### Processing the Entire Video File

The following test results come from two base videos. One of them is a clip of a CNN news report, while the other has been recorded by us. A total of 51 sets were created for each base video, corresponding to audio/video offsets of -1s to 1s in increments of 40ms. The following histogram shows the error between the computed offset and the true offset:

<p align="center">
	<img src="https://github.com/binhanle/eem202a-project/blob/master/Images/res_mar_thresh.png"></img>
	<br/>
	<strong>Error between Computed Offset and True Offset</strong>
</p>
<br/>

The error in the internet video's synchronization was consistently one frame, while the error in our own video's synchronization was consistently two frames. The fact that the synchronization process was able to achieve such a low error demonstrates the existence of a strong correlation between a speaker's mouth aspect ratio and the detected voice activity from the audio stream. However, the consistency of the error reveals some information that we had not previously considered. There is actually a delay between the time when a speaker opens their mouth and when sound actually comes out. This delay seems to depend on the speaker, but it may be possible to compensate for this error by computing an average across multiple videos with different speakers.

<br/>

A threshold technique was initially used to assign a binary value to the MAR. The binary value for a particular frame would determine whether the speaker's mouth was open or closed during that time, according to a specific threshold. In the optimization process described above, this threshold value was included in the optimization over the VAD aggressiveness value. However, the conversion from a continuous MAR to a binary MAR resulted in the unnecessary loss of information. The histogram below shows the computed error with a binary MAR, using the same dataset as the results above:


<p align="center">
	<img src="https://github.com/binhanle/eem202a-project/blob/master/Images/res_mar_no_thresh.png"></img>
	<br/>
	<strong>Error using Binary MAR</strong>
</p>
<br/>


### Using a Variable Window Size
A real-time implementation would not have access to the entire video. In light of this, the system was evaluated on sliding windows of size 1 to 12 seconds rather than whole videos. As before, the maximum offset between any audio-video pair was 25 frames in either direction. Audio-video pairs whose VAD component stayed constant were discarded as no useful information could be gleaned from the audio. As expected, the performance improved with larger window sizes:


<p align="center">
	<img src="https://github.com/binhanle/eem202a-project/blob/master/Images/res_var_win_size.png"></img>
	<br/>
	<strong>Error using Variable Window Size</strong>
</p>
<br/>


### Key Findings
* The mouth aspect ratios (MARs) of a speaker in the video has a good correlation to his or her voice activity in the audio.
* Using raw MARs instead of a binary MAR threshold gives better correlation between MAR and voice activity
* There is a consistent offset between when a person opens his or her mouth and when he or she start/resume the talk


## Strength and Weakness
The strategy of identifying speaking & non-speaking portions from open mouth and voice activity then correlating the audio and video streams allows fast processing speed for for time offset calculations. By considering the nature of injecting time offsets, this synchronization strategy ideally can work on any time offset length between a pair of audio and video streams. In addition, the mechanism of time offset calulation is intuitive and easy to understand. It appears that audiovisual synchronization is possible when given decisive features from the audio and video streams.

Because of its simplicity, the presented sychronization strategy is limited to video files that feature single-person, frontal-pose talks. Moreover, the system expects a speaker make pauses in his or her speech so that multiple starting and ending points of open mouth and human voice can be established. Another constraint of this sychronization strategy is that the speaker cannot lose his or her frontal pose or temproraily disppear from the scenes. These situations can potentially cause missing information in the video stram and thus reduce the performance of the audiovisual synchronization by the presented system. 


## Future Directions
The presented work can be expanded by including more decisive features for audiovisual correlation. The team will pursue further research in sound source recognitions so that multi-speaker scenarios can be covered the presented audiovisual synchronization strategy. Further investigation on correlating lip movements with phonemes can also be pursued for increasing the chance of correctly pairing a human voice with a speaker. Such a imporvement can be made to avoid mismatches of open mouths and voice acitivties in multi-speaker video files. For addressing the consistent offset between open mouth and human voice, the team will explore literatures that document visual cues in human speech. After idenifying the range of time offsets between open mouth motion and human voice acitivity, the team will determine equation(s) that can negate this innate discrepancy.


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

#### Primary:
- Develop a machine-learning based model to properly recognize and quantify video and audio time offsets for videos of a single speaker in full-frontal view, with an error less than 40ms <strong>Completed</strong>
- Define a performance spectrum of the model for varying delays between the audio and video streams, to determine the range of its best use case <strong>Completed</strong>

#### Stretch:
- Create a backend program to run in real time, to capture the on screen video, determination in time offset, and make the necessary correction, all automatically <strong>Completed</strong>
- Expand analysis to similar video types, acquired from various web sources (YouTube) <strong>Completed</strong>
- Implement delay compensation for a common video streaming service <strong>Aborted</strong>

## Deliverables
- All datasets -- full-frontal recordings of Loic, An, and Mark, and full-frontal online recordings
- Scripts that demultiplex audio/video files, preprocesses the audio/video streams, and inject time delay into video streams
- Suitable neural network architecture for determining time offset
- Program that restores audio/video synchronization offline
- Complete demonstration of synchronizing audio and video on a laggy live stream
- Final presentation video

Dataset Google drive link found under Datasets section.

Demo video, local machine test script with readme, final presentation video found here:
https://drive.google.com/drive/folders/1bkACCd296XZr6WN9FIi9VbwKCZhVBETt?usp=sharing

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
