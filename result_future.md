---
title: Evaluation
layout: template
filename: result_future
--- 


## Table of Contents
* [Strengths and Weaknesses](#strengths-and-weaknesses)
* [Future Direction](#future-direction)


## Strengths and Weaknesses
The strategy of identifying speaking & non-speaking portions from open mouth and voice activity then correlating the audio and video streams allows fast processing speed for time offset calculations. By considering the nature of injecting time offsets, this synchronization strategy ideally can work on any time offset length between a pair of audio and video streams. In addition, the mechanism of time offset calculation is intuitive and easy to understand. It appears that audiovisual synchronization is possible when given decisive features from the audio and video streams.

Because of its simplicity, the presented synchronization strategy is limited to video files that feature single-person, frontal-pose talks. Moreover, the system expects a speaker make pauses in his or her speech so that multiple starting and ending points of open mouth and human voice can be established. Another constraint of this synchronization strategy is that the speaker cannot lose his or her frontal pose or temporarily disappear from the scenes. These situations can potentially cause missing information in the video stream and thus reduce the performance of the audiovisual synchronization by the presented system. 


## Future Direction
The presented work can be expanded by including more decisive features for audiovisual correlation. The team will pursue further research in sound source recognitions so that multi-speaker scenarios can be covered the presented audiovisual synchronization strategy. Further investigation on correlating lip movements with phonemes can also be pursued for increasing the chance of correctly pairing a human voice with a speaker. Such an improvement can be made to avoid mismatches of open mouths and voice activities in multi-speaker video files. For addressing the consistent offset between open mouth and human voice, the team will explore literatures that document visual cues in human speech. After identifying the range of time offsets between open mouth motion and human voice activity, the team will determine equation(s) that can negate this innate discrepancy.
