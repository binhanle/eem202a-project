---
title: Objectives
layout: template
filename: intent
--- 

## Table of Contents
* [Primary Goals](#primary-goals)
* [Stretch Goals](#stretch-goals)
* [Deliverables](#deliverables)
* [Success Metrics](#success-metrics)


#### Primary Goals:
- Develop a machine-learning based model to properly recognize and quantify video and audio time offsets for videos of a single speaker in full-frontal view, with an error less than 40ms <strong>Completed</strong>
- Define a performance spectrum of the model for varying delays between the audio and video streams, to determine the range of its best use case <strong>Completed</strong>

#### Stretch Goals:
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
