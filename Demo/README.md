# How to run the demo
- Tested on Ubuntu 19.10

## Get VLC
`sudo apt install vlc`

## Download dlib face landmarks file
`wget https://github.com/JeffTrain/selfie/raw/master/shape_predictor_68_face_landmarks.dat`

## Set up Python environment
- Anaconda is recommended. Install here https://www.anaconda.com/distribution/
- Create environment:

```
conda create -n avsync python=3.6
conda activate avsync
```

## Install required packages
```
pip install google-api-python-client
pip install oauth2client
pip install scipy
pip install tqdm
pip install webrtcvad
pip install imutils
pip install opencv-contrib-python
conda install -c conda-forge dlib
```

## Run the demo
`python detect_AV_desync.py example_25.mp4`

- Follow the instructions
