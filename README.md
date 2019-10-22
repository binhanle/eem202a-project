# Video and Audio Synchronization

## Abstract
Popular streaming websites, such as YouTube, often receive reports of video and audio offsets from their users. However, from their end, the server-side video and audio files are perfectly synchronized, and some latency is actually introduced by the time these files reach a viewer’s local video player. This latency is oftentimes non-deterministic, meaning it can only truly be resolved by doing a real-time analysis of the video and audio input from the user’s end and subsequently carrying out some corrective action. The purpose of this project is to quickly analyze a video’s audio cues and determine how much offset exists between the audio and video files, then perform the necessary time shift to realign them. By pointing a camera directly at the screen playing the video, we are able to capture what the user sees and hears, then transmit the information back to the host computer for processing and time shifting. This feedback system will execute a single time as soon as it is identified, and will focus on cases were the audio leads the video.

## Authors
Mark Chen
An Le
Loic Maxwell

## Previous Works

