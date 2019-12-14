---
title: Introduction
layout: template
filename: index
--- 

## Table of Contents
* [Abstract](#abstract)
* [Prior Work](#prior-work)
* [References](#references)


## Abstract
Popular streaming services, such as YouTube and Twitch, often receive reports of video and audio offsets from their users. However, from their end, the server-side video and audio files are perfectly synchronized, and latencies are actually introduced unpredictably before both video and audio are outputted from these users’ edge devices. Those latencies are often non-deterministic and can only truly be resolved by performing a real-time analysis and subsequent timing corrections on both video and audio inputs at the users’ side. The purpose of this project is to quickly analyze a video’s audio cues and determine how much offset exists between the audio and video files, then perform the necessary time shift to realign them. By using audio and screen capture technology, we are able to identify what a user sees and hears. Once this information is collected, specific features relating to the speaker's mouth aspect ratio in the video stream and the voice activity detection of the audio stream are extracted. Then, a cross-correlation to determine the time offset between the two streams, and the original video file/stream can be realigned by advancing or delaying the audio.

## Prior Work
Audio-visual synchronization is a major factor when determining the quality of a streaming service. Traditionally, scientists work on temporal coordination between audio and video streams to minimize the impact of cumulative latencies at end-users’ multimedia devices [1,2]. However, this approach often requires knowledge of the data transmission protocol applied on audio and video streams and derivations of complicated timing equations. Moreover, the outcome of synchronization can vary if latencies are introduced randomly across the entire streaming path [3]. To bypass these complications while improving the results of audio-visual synchronization, researchers begin to incorporate feature-based analysis on audio and video streams.

The emergence of machine learning helps boost the uses of feature-based analysis in audio-visual synchronization. A variety of machine learning models become available for extracting definitive features that can correlate audio and visual data based on the entailed events. For instance, Zhao et al. introduce a system that can locate the region of pixels on a video frame that correspond to a sound source in the audio stream [4]. Another notable example is the Lip Reading machine learning model from Torfi et al. that matches human voices to lip motions [5]. With the advantage of utilizing feature-based information to correlate audio and video streams, one can likely design a machine learning model to classify whether a streaming service has its video and audio synced at a good accuracy.

A couple of works had proposed their own trained machine learning systems (e.g. SyncNet) to detect the presence of audio-visual synchronization in some given pairs of video and audio inputs [6,7]. Nevertheless, there is limited information of concrete methods that can be used to resolve the detected time offsets between a pair of video and audio inputs. Given this point, there is a need to develop a working audio-visual synchronization system that enables follow-up synchronization after the detection of a time offset.    


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
