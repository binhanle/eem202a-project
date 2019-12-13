---
title:  Exploration
layout: template
filename: method_explore
--- 


## Table of Contents
* [Discontinued Approaches](#discontinued-approaches)
  * [Direct CNN Approach](#direct-cnn-approach)
  * [SyncNet-Inspired Approach](#syncNet-inspired-approach)


## Discontinued Approaches

### Direct CNN Approach

This was the first attempted approach towards solving the audio/video synchronization problem. This was also the one highlighted in the initial proposal. The audio and video were trained separately in two convolutional neural networks (CNNs).

<p align="center">
	<img src="https://github.com/binhanle/eem202a-project/blob/master/Images/strat1.png" />
	<br/>
	<strong>CNN Architecture</strong>
</p>

The reason why we did not pursue this approach is...

This approach can be found under:
"Name for Strategy 1 colab notebook"

### SyncNet-Inspired Approach

The third attemtped strategy was based on the SyncNet paper. They were able to accomplish audio-video synchronization for a window size of only 5 frames. 

<p align="center">
	<img src="https://github.com/binhanle/eem202a-project/blob/master/Images/strat3.png"/>
	<br/>
	<strong>Source: https://www.robots.ox.ac.uk/~vgg/publications/2016/Chung16a/chung16a.pdf</strong>
</p>
	
The reason why we did not pursue this strategy is...

This approach can be found under:
"Name for Strategy 3 colab notebook"
