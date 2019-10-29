# Video and Audio Synchronization

## Table of Contents
* [Authors](#authors)
* [Abstract](#abstract)
* [Prior Works](#prior-works)
* [Technical Approaches](#technical-approaches)
* [Experimental Methods](#experimental-methods)
* [References](#references)
* [Timeline](#timeline)

## Authors
- Mark Chen
- An Le
- Loic Maxwell

## Abstract
Popular streaming services, such as YouTube and Twitch, often receive reports of video and audio offsets from their users. However, from their end, the server-side video and audio files are perfectly synchronized, and latencies are actually introduced unpredictably before both video and audio are outputted from these users’ edge devices. Those latencies are often non-deterministic and can only truly be resolved by performing a real-time analysis and subsequent timing corrections on both video and audio inputs at the users’ side. The purpose of this project is to quickly analyze a video’s audio cues and determine how much offset exists between the audio and video files, then perform the necessary time shift to realign them. By using audio and screen capture technology, we are able to identify what a user sees and hears. Specific features are then extracted from the captured and audio and video streams, and passed through a trained neural network to determine the required time shift. This feedback system will run continuously during a streaming session and properly correct the timings of video and audio streams as soon as an offset is identified.

## Prior Works


## Technical Approaches


## Experimental Methods


## Timeline

| Task | Week 5 | Week 6 | Week 7 | Week 8 | Week 9  | Week 10 | Delivery |
| --- | --- | --- | --- | --- | --- | --- | --- |
| **I. Datasets** |
| Create own customized datasets (full frontal, single person) |
| Experiment with video streaming sites, to test real-time performance (optional) |
| **II. Capture audio and video from user end** |
| Select hardware/software tools |
| Experiment with other tools and make a performance comparison (optional) |
| **III. Handle the captured audio and video inputs** |
| Determine what tools to use for demuxing audio/video of .mp4 files |
| Create translation into a usable format for the feature extraction program |
| Expand to other video formats (optional) |
| **IV. Design ML network** |
| Define features to extract from video/audio |
| Build software to perform feature extraction |
| Determine network architecture |
| Train network |
| **V. Create wrapper program** |
| Define how to handle time injection |
| Integrate the ML portion and resulting delay injection |
| **VI. Translate into real-time system (optional)** |
| Make video/audio capture and processing run in the background |
| Implement real time delay injection |

## References
- Imad H. Elhajj, Nadine Bou Dargham, Ning Xi, and Yunyi Jia. 2011. “Real-Time Adaptive Content-Based Synchronization of Multimedia Streams.” *Advances in Multimedia*. https://doi.org/10.1155/2011/914062

- Detecting audio-visual synchrony using deep neural networks:\
https://www.semanticscholar.org/paper/Detecting-audio-visual-synchrony-using-deep-neural-Marcheret-Potamianos/a4d80ea114a924931cf87070b93885ca52ed6c42


- Audio-visual speech synchrony detection by a family of bimodal linear prediction models:\
https://books.google.com/books?hl=en&lr=&id=aqXD3iBuQewC&oi=fnd&pg=PA31&dq=related:vmS8Tt9PFPYJ:scholar.google.com/&ots=eHEcHta6Pk&sig=nufDCauh3XFJAaiXTNtWGeYvPrU#v=onepage&q&f=false


- MULTICOREWARE SHOWS LIPSYNC TO AUTODETECT A/V SYNC VIA DEEP LEARNING + GPUS:\
https://www.provideocoalition.com/multicoreware-shows-lipsync-to-autodetect-av-sync-via-deep-learning-gpus/amp/
LipSync and TextSync are software packages that allow you to quickly check if a video file or stream has synchronized audio, video, and subtitles:
https://lipsync.multicorewareinc.com


- Out of time: automated lip sync in the wild - University of Oxford:\
https://www.robots.ox.ac.uk/~vgg/publications/2016/Chung16a/chung16a.pdf


- Using timestamp to realize audio-video synchronization in Real-Time streaming media transmission:\
https://ieeexplore.ieee.org/document/4589974


- Lip Reading - Cross Audio-Visual Recognition
https://github.com/astorfi/lip-reading-deeplearning


- The Sound of Pixels -  locate image regions which produce sounds
http://sound-of-pixels.csail.mit.edu


- Audiovisual synchrony detection with optimized audio features
https://hal.inria.fr/hal-01889918/file/audiovisual_synchrony_2018.pdf

