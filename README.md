# Video and Audio Synchronization

## Abstract
Popular streaming services, such as YouTube and twitch, often receive reports of video and audio offsets from their users. However, from their end, the server-side video and audio files are perfectly synchronized, and latencies are actually introduced unpredictably until both video and audio are outputted from these users’ edge devices. Those latencies are often non-deterministic and can only truly be resolved by performing a real-time analysis and subsequent timing corrections on both video and audio inputs at the users’ side. The purpose of this project is to quickly analyze a video’s audio cues and determine how much offset exists between the audio and video files, then perform the necessary time shift to realign them. By using audio and screen capture technology, we are able to identify what a user sees and hears. Specific features are then extracted from the captured and audio and video streams, and passed through a trained neural network to determine the required time shift. This feedback system will run continuously during a streaming session and properly correct the timings of video and audio streams as soon as an offset is identified.

## Authors
- Mark Chen
- An Le
- Loic Maxwell

## Previous Works
- Elhajj, Imad H., Nadine Bou Dargham, Ning Xi, and Yunyi Jia. 2011. “Real-Time Adaptive Content-Based Synchronization of Multimedia Streams.” *Advances in Multimedia*. https://doi.org/10.1155/2011/914062.
