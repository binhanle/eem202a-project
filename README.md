# Video and Audio Synchronization
UCLA ECE M202A Project, Fall 2019

## Table of Contents
* [Authors](#authors)
* [Abstract](#abstract)
* [Prior Works](#prior-works)
* [Technical Approaches](#technical-approaches)
* [Experimental Methods](#experimental-methods)
* [Timeline](#timeline)
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

A couple of works had proposed their own trained machine learning systems to detect the presence of audio-visual synchronization in some given pairs of video and audio inputs [6,7]. Nevertheless, there is limited information of concrete methods that can be used to resolve the detected time offsets between a pair of video and audio inputs. Given this point, there is a need to develop a working audio-visual synchronization system that enables follow-up synchronization after the detection of a time offset.    


## Technical Approach

## Methodology:

### External Recording:

In order to capture what a user would see and hear from the video, thereby encompassing all latency that could be introduced between the audio/video files, a recording device external to the video player must be introduced. The external recording can be handled by the same computer, or by an external device. Screen recording software such as Camtasia and OBS (for Windows, Mac) or built-in screen recording for iOS and Android can directly record the video, while using a built-in microphone to record the audio. This method relies on the use of an internal microphone, which is available in most, but not all common computing devices. This can also be carried out by an external device, which can be as sophisticated and customized as need be for the purposes of the recording. Both methods have their advantages and disadvantages, but the simplicity of on screen recording and the ability to compile all software into a convenient and deployable package beats the possible customization provided by an external device and the problem case where a user may not have an internal microphone available to use.

### Demultiplexing of Video/Audio Files:

In order to properly run a neural network analysis and subsequent shifting of the video and audio stream files, the original video file must be demultiplexed. FFmpeg is a powerful tool which provides the capability to strip away the audio from a video file, while also allowing them to be spliced back together following the calculated time shift. Once these files have been isolated, they can be further processed. Through multiple stages of processing for each file, the relevant information can be extracted, normalized, and fed into the designed neural network. This drastically decreases the computational complexity of the data to be passed through the network.

### Processing, Features, and the Neural Network:

This project focuses on videos that portray a single full frontal speaker, where the audio leads the video. This allows for lip speech recognition software to be used as an additional tool for audio extraction of the video file. Additionally, using existing pixel-to-sound technology [4], frames where speech actually occurs can be isolated and one can determine the various start and stop points of semi-continuous speech. Lastly, a frequency analysis on the audio will reveal certain spikes in the speaker’s speech, and can be further analyzed using speech recognition tools like CMUSphinx. These, combined with the lip recognition analysis of the video, provide the means to draw correlations between the audio and video files. By combining all of these data processing techniques, there should be sufficient features to train a neural network. The neural network itself will be a supervised learner. It is trained by inputting multiple sets of inputs (features) along with their known respective outputs, or labels (time shift between the audio/video). Subsequent test inputs with unknown outputs can then theoretically be correctly classified. The architecture of the neural network itself is a different challenge, which will be tackled in the coming weeks of this project’s development.

### Time injection:

Once the required time shift has been identified by the neural network output, the FFmpeg tool can be used again to inject this lead or lag in the audio file. It can also recombine the audio and video stream files, and output the synchronized video file. It will be difficult to inject the delay directly into the original video without interrupting it in some way. The time injection process itself is very quick, so any personal computer would be more than capable of executing this in a trivial amount of time, in order to keep the user experience as seamless as possible.
	
## Data Sets for Neural Network Training/Validation:

As it was mentioned before, the scope of this project will be limited to videos that feature a full-frontal view of a single speaker, where the audio leads the video. These videos will be recorded in a controlled environment. The plan is to shoot 5-7 different videos, with varying speaker location, speech, volume, ambient noise, etc. This will give the neural network a variety of cases on which it can be trained, which will make it more effective when the transition is made to testing on other types of videos. 
Though the architecture of the neural network is not yet defined, the way in which it will be trained is relatively known. The neural network output represents the time delay between the audio and video streams, and in the case of training this will be provided for each set of inputs. FFmpeg can be used to create an audio lead of 1ms to 250ms for each video, in increments of 1ms. This provides a large training set for the neural network. This also provides a large enough range over which to compare the performance of the model for small time offsets compared to large ones. For the purpose of training and testing the network, k-fold cross validation will be used. This means that “k-1” sets of data will be used as the training set, and 1 set will be used as the test set to check the accuracy of the network, where one set is the data from a single video. The value “k” represents the number of different videos that will be recorded and used as data sets, which is still variable at this stage. The test set is then switched with one of the other sets used for training, and this process is repeated until every set has been used as the test set. The training set combination that yields the best results will be used for subsequent testing.

## Validating the Neural Network

A test set for the neural network provides the best measure of its performance. The calculated outputs (labels) can be compared to their known ones, and an error value can be computed for each set of input features. The average error across all outputs will be used to determine the best training set given this first set of data, according to k-fold cross validation. One of the primary goals is to keep this error below 40 ms for all output values, which would fall within a threshold of non-detectability from the perspective of a viewer [9]. In other words, a human would not recognize any synchronization problems if the out-of-sync audio and video are within 40ms of each other. If for some reason this goal is not achievable given the current data, the audio lead increment for creating training data will be decreased from 1ms to 0.5ms. If this does not resolve the issue, then other approaches will have to be taken (shorter increment, more data sets, more features, etc.).

Following this process, a second set of test videos will be acquired. These will test the accuracy of the trained network. With a 40 ms error tolerance, it is possible to have a success rate of over 90% for all test cases. Once this has been accomplished, the next step is to test on random videos found on the internet (e.g. YouTube). They will still feature full-frontal shots of a single speaker, but this will test the versatility of the neural network.

## Timeline

### Legend
| Status | Color |
| --- | :---: |
| Scheduled | ![blue](https://placehold.it/32/3d85c6/000000?text=+) |
| In progress | ![yellow](https://placehold.it/32/f1c232/000000?text=+) |
| Completed | ![green](https://placehold.it/32/6aa84f/000000?text=+) |
| Aborted | ![red](https://placehold.it/32/cc0000/000000?text=+) |

| Major Objective with Subtasks | Week 5 | Week 6 | Week 7 | Week 8 | Week 9  | Week 10 | Delivery |
| --- | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **I. Datasets** |
| Create own customized datasets (full frontal, single person): Loic, Mark, An | ![yellow](https://placehold.it/32/f1c232/000000?text=+) | ![blue](https://placehold.it/32/3d85c6/000000?text=+) |
| Experiment with video streaming sites, to test real-time performance (optional): Loic, Mark, An | | | | ![blue](https://placehold.it/32/3d85c6/000000?text=+) | ![blue](https://placehold.it/32/3d85c6/000000?text=+) |
| **II. Capture audio and video from user end** |
| Select hardware/software tools: Mark | ![yellow](https://placehold.it/32/f1c232/000000?text=+) | ![blue](https://placehold.it/32/3d85c6/000000?text=+) |
| Experiment with other tools and make a performance comparison (optional): Mark | | | | ![blue](https://placehold.it/32/3d85c6/000000?text=+) | ![blue](https://placehold.it/32/3d85c6/000000?text=+) |
| **III. Handle the captured audio and video inputs** |
| Determine what tools to use for demuxing audio/video of .mp4 files: Mark | ![yellow](https://placehold.it/32/f1c232/000000?text=+) | ![blue](https://placehold.it/32/3d85c6/000000?text=+) |
| Create translation into a usable format for the feature extraction program: Mark | | ![blue](https://placehold.it/32/3d85c6/000000?text=+) | ![blue](https://placehold.it/32/3d85c6/000000?text=+) |
| Expand to other video formats (optional): Mark, An, Loic | | | | | ![blue](https://placehold.it/32/3d85c6/000000?text=+) | ![blue](https://placehold.it/32/3d85c6/000000?text=+) |
| **IV. Design ML network** |
| Define features to extract from video/audio: An, Loic, Mark | ![yellow](https://placehold.it/32/f1c232/000000?text=+) | ![blue](https://placehold.it/32/3d85c6/000000?text=+) |
| Build software to perform feature extraction: An | | ![blue](https://placehold.it/32/3d85c6/000000?text=+) | ![blue](https://placehold.it/32/3d85c6/000000?text=+) |
| Determine network architecture: An, Mark, Loic | | ![blue](https://placehold.it/32/3d85c6/000000?text=+) | ![blue](https://placehold.it/32/3d85c6/000000?text=+) | ![blue](https://placehold.it/32/3d85c6/000000?text=+) |
| Train network: An | | | | ![blue](https://placehold.it/32/3d85c6/000000?text=+) |
| **V. Create wrapper program** |
| Define how to handle time injection: Loic | | | ![blue](https://placehold.it/32/3d85c6/000000?text=+) |
| Integrate the ML portion and resulting delay injection: Loic | | | | ![blue](https://placehold.it/32/3d85c6/000000?text=+) | ![blue](https://placehold.it/32/3d85c6/000000?text=+) |
| **VI. Translate into real-time system (optional)** |
| Make video/audio capture and processing run in the background: Mark | | | | | ![blue](https://placehold.it/32/3d85c6/000000?text=+) | ![blue](https://placehold.it/32/3d85c6/000000?text=+) |
| Implement real time delay injection: Loic | | | | | ![blue](https://placehold.it/32/3d85c6/000000?text=+) | ![blue](https://placehold.it/32/3d85c6/000000?text=+) |

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
