#https://medium.com/@umdfirecoml/a-step-by-step-guide-on-how-to-download-your-google-drive-data-to-your-jupyter-notebook-using-the-52f4ce63c66c

from apiclient import discovery
from httplib2 import Http
from oauth2client import file, client, tools
import io
from googleapiclient.http import MediaIoBaseDownload
import subprocess
from scipy import signal
from tqdm import tqdm
import contextlib
import sys
import wave
import os
import webrtcvad
from scipy.spatial import distance as dist
from imutils import face_utils
import numpy as np
import imutils
import time
import dlib
import cv2

# grab the indexes of the facial landmarks for the mouth
# Note: https://www.pyimagesearch.com/2017/04/10/detect-eyes-nose-lips-jaw-dlib-opencv-python/
(mStart, mEnd) = (49, 68)

# initialize dlib's face detector (HOG-based) and then create
# the facial landmark predictor
# Note: http://dlib.net/train_shape_predictor.py.html
print("[INFO] loading facial landmark predictor...")

detector = dlib.get_frontal_face_detector()
predictor_file = 'shape_predictor_68_face_landmarks.dat'
predictor = dlib.shape_predictor(predictor_file)

def get_mouth_aspect_ratio(mouth):

    # MAR Equations using three vertical distances
    # compute the euclidean distances between the two sets of
    # vertical mouth landmarks (x, y)-coordinates
    A = dist.euclidean(mouth[2], mouth[9])  # 51, 59
    B = dist.euclidean(mouth[3], mouth[8])  # 52, 58
    C = dist.euclidean(mouth[4], mouth[7])  # 53, 57

    # compute the euclidean distance between the horizontal
    # mouth landmark (x, y)-coordinates
    D = dist.euclidean(mouth[0], mouth[6])  # 49, 55

    # compute the mouth aspect ratio
    mar = (A + B + C) / (3.0 * D)

    # return the mouth aspect ratio
    return mar


# define one constants, for mouth aspect ratio to indicate open mouth
# MOUTH_AR_THRESH = 0.55

def mouth_aspect_ratio(frame):
    #frame = imutils.resize(frame, width=640)
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    rects = detector(gray, 0)

    # If there are no faces, return zero
    if not rects:
        return 0

    # determine the facial landmarks for the face region, then
    # convert the facial landmark (x, y)-coordinates to a NumPy
    # array
    shape = predictor(gray, rects[0])
    shape = face_utils.shape_to_np(shape)

    # extract the mouth coordinates, then use the
    # coordinates to compute the mouth aspect ratio
    mouth = shape[mStart:mEnd]
    return get_mouth_aspect_ratio(mouth)

def read_wave(path):
    with contextlib.closing(wave.open(path, 'rb')) as wf:
        num_channels = wf.getnchannels()
        assert num_channels == 1
        sample_width = wf.getsampwidth()
        assert sample_width == 2
        sample_rate = wf.getframerate()
        assert sample_rate in (8000, 16000, 32000, 48000)
        pcm_data = wf.readframes(wf.getnframes())
        return pcm_data, sample_rate


class Frame(object):
    def __init__(self, bytes, timestamp, duration):
        self.bytes = bytes
        self.timestamp = timestamp
        self.duration = duration


def frame_generator(frame_duration_ms, audio, sample_rate):
    n = int(sample_rate * (frame_duration_ms / 1000.0) * 2)
    offset = 0
    timestamp = 0.0
    duration = (float(n) / sample_rate) / 2.0
    while offset + n < len(audio):
        yield Frame(audio[offset:offset + n], timestamp, duration)
        timestamp += duration
        offset += n


def vad_classification(sample_rate, frame_duration_ms, vad, a_frames):
    is_speech = 0
    output_binary_list = []

    for frame in a_frames:
        is_speech = vad.is_speech(frame.bytes, sample_rate)
        if (is_speech):
            output_binary_list.append(1)
        else:
            output_binary_list.append(0)
    return output_binary_list

def mouth_aspect_ratio_binary(frame, MOUTH_AR_THRESH):
    mar = mouth_aspect_ratio(frame)
    if mar > MOUTH_AR_THRESH:
        # Mouth is open
        return 1

    # Mouth is closed
    return 0

def get_voice_activity(audio, sample_rate, VAD_agg):
    vad = webrtcvad.Vad(VAD_agg)
    audio_frames = frame_generator(10, audio, sample_rate)
    audio_frames = list(audio_frames)
    return vad_classification(sample_rate, 10, vad, audio_frames)

def get_gdrive_params():
    obj = lambda: None
    lmao = {"auth_host_name": 'localhost', 'noauth_local_webserver': 'store_true', 'auth_host_port': [8080, 8090],
            'logging_level': 'ERROR'}
    for k, v in lmao.items():
        setattr(obj, k, v)

    # authorization boilerplate code
    SCOPES = 'https://www.googleapis.com/auth/drive.readonly'
    store = file.Storage('token.json')
    creds = store.get()
    # The following will give you a link if token.json does not exist, the link allows the user to give this app permission
    if not creds or creds.invalid:
        flow = client.flow_from_clientsecrets('client_id.json', SCOPES)
        creds = tools.run_flow(flow, store, obj)

    DRIVE = discovery.build('drive', 'v3', http=creds.authorize(Http()))
    #ID of shareable link
    #file_id = '1Ht1Q_ZNcg7PXjwovVI-RLt-ZuUSAaW0wmFWS0OKdSgw'
    file_id = '1-2Cj3U7avgbnsjQEZuDwe8q9wRL4zL3D'
    request = DRIVE.files().get_media(fileId=file_id)
    # replace the filename and extension in the first field below
    fh = io.FileIO('MAR_VAD_params.txt', mode='w')
    downloader = MediaIoBaseDownload(fh, request)
    done = False
    while done is False:
        status, done = downloader.next_chunk()
        print("Download %d%%." % int(status.progress() * 100))

    params = []
    with open("MAR_VAD_params.txt", 'r', encoding="utf-8-sig") as f:
        for line in f:
            params.append(float(line))

    #params[0] = VAD_agg and params[1] = MOUTH_AR_THRESHOLD
    return int(params[0]), params[1]


def extract_video(video_file):
    frames = []
    cap = cv2.VideoCapture(video_file)
    frame_rate = cap.get(cv2.CAP_PROP_FPS)
    print('The frame rate is {} FPS'.format(frame_rate))
    while cap.isOpened():
        success, frame = cap.read()
        if success == False:
            break

        frames.append(frame)

    return frames, frame_rate


def preprocess_video(frames, num_window_frames):
    # Specify feature extraction method
    get_video_features = mouth_aspect_ratio

    output_list = []
    for frame in tqdm(frames):
        # Get video features
        features = get_video_features(frame)
        output_list.append(features)

    # Smooth output
    b, a = signal.bessel(4, 0.2)
    smoothed = signal.filtfilt(b, a, output_list)

    # Normalize output
    return (smoothed - np.min(smoothed)) / (np.max(smoothed) - np.min(smoothed))

def to_binary(array, threshold):
    # Replaces elements >= threshold with 1 and the rest with 0
    return np.where(0, 1, array >= threshold)

def extract_audio(video_file, audio_file):

    # Pull audio stream from video
    subprocess.call(['ffmpeg', '-y', '-i', video_file, '-ac', '1', '-ar', '32000', audio_file])

    return read_wave(audio_file)


def preprocess_audio(audio, sample_rate, num_video_frames, VAD_agg):
    # Select feature extraction method
    get_audio_features = get_voice_activity

    # Get audio features
    output_list = get_audio_features(audio, sample_rate, VAD_agg)

    # Resize output to match length of frame list
    resampled = signal.resample(output_list, num_video_frames)

    # Smooth output
    b, a = signal.bessel(4, 0.2)
    smoothed = signal.filtfilt(b, a, resampled)

    # Get rid of overshoots in resampled signal
    output_binary = to_binary(smoothed, 0.5)

    return np.array(output_binary)

def main(args):

    #Takes path to video file as input
    #Creates a synced version of the video

    video_file = args[0]
    img_rows, img_cols = 32, 32
    num_window_frames = 30

    VAD_agg, MOUTH_AR_THRESHOLD = get_gdrive_params()
    print(VAD_agg)
    print(MOUTH_AR_THRESHOLD)

    vlc_input = video_file
    #quit_vlc = "vlc vlc://quit"
    quit_vlc = ["pkill", "vlc"]

    subprocess.Popen(["vlc", vlc_input])
    start_time = int(round(time.time() * 1000))

    computed_delay = 0

    #Define file names for processing
    video_dir = os.path.dirname(video_file)
    video_name = os.path.splitext(os.path.basename(video_file))[0]
    audio_file = os.path.join(video_dir, video_name + '.wav')
    output_video = os.path.join(video_dir, video_name + '_synced.mp4')

    #Extract video and audio
    frames, frame_rate = extract_video(video_file)
    audio, sample_rate = extract_audio(video_file, audio_file)

    #Preprocessing/feature extraction phase
    Xv = preprocess_video(frames, num_window_frames)
    Xa = preprocess_audio(audio, sample_rate, len(frames), VAD_agg)

    #Correlation to find the time offset
    Xv_np = np.hstack(Xv)
    Xa_np = np.hstack(Xa)
    corr = np.correlate(Xv_np, Xa_np, mode='same')
    index = np.argmax(corr)
    computed_delay = index - len(Xv_np) // 2
    computed_delay = 0.040 * computed_delay
    print(computed_delay)

    #Create new corrected video
    subprocess.call(['ffmpeg', '-i', video_file, '-itsoffset', str(computed_delay), '-i', video_file, '-map', '0:v', '-map', '1:a', '-c', 'copy', output_video])

    #Get time of execution
    new_start = (int(round(time.time() * 1000)) - start_time)/1000


    #Quit and restart vlc with synced video at the same spot
    print(subprocess.check_output(quit_vlc))
    vlc_new_start = "--start-time=" + str(new_start)
    vlc_input_synced = output_video

    #TODO: Add vlc_new_start as argument
    subprocess.Popen(["vlc", vlc_new_start, vlc_input_synced])

if __name__ == '__main__':
    main(sys.argv[1:])





