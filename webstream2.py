from picamera2.encoders import H264Encoder
import subprocess
import picamera2
import json
import shlex

vlcCommand="cvlc -vvv  stream:///dev/stdin --sout '#standard{access=http,mux=ts,dst:8080}' :demux=h264"
#conf = json.load(open('conf.json'))

with picamera2.Picamera2() as camera:
   #camera.resolution = tuple(conf["resolution"])
   #camera.framerate = conf["fps"]
   #camera.vflip = True
   #camera.hflip = True
    video_config = camera.create_video_configuration(main={"size": (1920, 1080)}, lores={"size": (640, 480)}, display="lores")
    camera.configure(video_config)
    encoder = H264Encoder(bitrate=10000000)
    cvlc = subprocess.Popen(shlex.split(vlcCommand), stdin=subprocess.PIPE)
    camera.start_recording(encoder,cvlc.stdin)
    camera.wait_recording(30)
    camera.stop_recording()
