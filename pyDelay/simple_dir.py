import math
import soundcard as sc
import numpy as np
import scipy.signal
from matplotlib.mlab import rms_flat
from spacebrew import Spacebrew

rate = 96000
soundSpeed = 343 # m/s
client = Spacebrew('mic_array', server='localhost')
client.addPublisher('000', 'range')
client.addPublisher('060', 'range')
client.addPublisher('120', 'range')
client.start()

# open the mic array
mic = sc.get_microphone('Azure Kinect')

def crest_factor(signal):
    """
    Crest factor of a 1D signal
    """
    peak = np.amax(np.absolute(signal))
    rms = rms_flat(signal)
    if rms == 0:
        rms = .000001
    return peak/rms

def process(data):
    # separate the audio by channel
    channels = [[sample[channel] for sample in data] for channel in range(7)]
    
    maxs = [np.argmax(channel) for channel in channels]
    maxvs = [channels[i][maxs[i]] for i in range(7)]
    print('loudest recording from channel ' + str(np.argmax(maxs)) + ":" + str(maxvs[np.argmax(maxs)]))
    first = np.argmin(maxs)
    last = np.argmax(maxs)
    deltaSamp = maxs[last] - maxs[first]
    deltaSec = deltaSamp / rate
    deltaM = deltaSec * soundSpeed
    print('first loudest from channel ' + str(np.argmin(maxs)))
    print('last loudest from channel ' + str(np.argmax(maxs)))
    print('samp: ' + str(deltaSamp) + ' sec: ' + str(deltaSec) + ' mm: ' + str(deltaM*1000))
    npc = np.correlate(channels[first], channels[last], 'full')
    scc = scipy.signal.correlate(channels[first], channels[last], 'full')
    print('match at ' + str(np.argmax(npc)) + ' vs ' + str(np.argmax(scc)))
    delay = int(len(npc)/2) - np.argmax(npc)
    distance = delay / rate * soundSpeed
    print('delay: ' + str(delay) + ' dist: ' + str(distance))

def getDist(chA, chB):
    corr = np.correlate(chA, chB, 'full')
    delay = int(len(corr) / 2) - np.argmax(corr)
    distance = delay / rate * soundSpeed
    return distance

def processC(data):
    # separate the audio by channel
    channels = [[sample[channel] for sample in data] for channel in range(7)]
    d000 = getDist(channels[1], channels[4])
    d060 = getDist(channels[2], channels[5])
    d120 = getDist(channels[3], channels[6])
    print('0: {:.4f} 60: {:.4f} 120: {:.4f}'.format(d000, d060, d120))
    print(max(d000, d060, d120))
    compareto = .08
    c000 = -1 if np.abs(d000) > compareto else math.acos(d000/compareto)
    c060 = -1 if np.abs(d060) > compareto else math.acos(d060/compareto)
    c120 = -1 if np.abs(d120) > compareto else math.acos(d120/compareto)
    print('0: {:.2f} 60: {:.2f} 120: {:.2f}'.format(c000, c060, c120))
    aa = np.abs([c000, c060, c120])
    mi = np.argmin(aa);
    client.publish('000', c000 / math.pi * 1023)
    client.publish('060', c060 / math.pi * 1023)
    client.publish('120', c120 / math.pi * 1023)

try:
    with mic.recorder(samplerate=rate) as recorder:
        while True:
            data = recorder.record(numframes=1024)
            #normalize all data?
            data /= np.max(np.abs(data))
            cf = crest_factor(data)
            if cf > 5:
                print(cf)
                processC(data)
except:
    client.stop()
