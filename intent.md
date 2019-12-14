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
* [Project Timeline](#timeline)


## Primary Goals:
- Develop a machine-learning based model to properly recognize and quantify video and audio time offsets for videos of a single speaker in full-frontal view, with an error less than 40ms <strong>Completed</strong>
- Define a performance spectrum of the model for varying delays between the audio and video streams, to determine the range of its best use case <strong>Completed</strong>

## Stretch Goals:
- Create a backend program to run in real time, to capture the on screen video, determination in time offset, and make the necessary correction, all automatically <strong>Completed</strong>
- Expand analysis to similar video types, acquired from various web sources (YouTube) <strong>Completed</strong>
- Implement delay compensation for a common video streaming service <strong>Aborted</strong>

## Deliverables
- All datasets -- full-frontal recordings of Loic, An, and Mark, and full-frontal online recordings
- Scripts that demultiplex audio/video files, preprocess the audio/video streams, and inject time delay into video streams
- Suitable neural network architecture for determining time offset
- Program that restores audio/video synchronization offline
- Complete demonstration of synchronizing audio and video on a laggy live stream
- Final presentation video

Dataset Google drive link found under Datasets section.

Demo video, local machine test script with readme, final presentation video found here:
https://drive.google.com/drive/folders/1bkACCd296XZr6WN9FIi9VbwKCZhVBETt?usp=sharing

YouTube Link to Video:
https://youtu.be/VBxVKRHk9VY

## Success Metrics
- Errors in software (potentially a major obstacle as many packages and dependencies need to be installed/utilized correctly)
- Neural network training speed
- Error between estimated and actual time offset

## Project Timeline

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
