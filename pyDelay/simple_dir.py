import math
import soundcard as sc
import numpy as np
import scipy.signal
from matplotlib.mlab import rms_flat
from spacebrew import Spacebrew
import traceback

rate = 96000
soundSpeed = 343 # m/s
client = Spacebrew('mic_array', server='localhost')
client.addPublisher('000', 'range')
client.addPublisher('060', 'range')
client.addPublisher('120', 'range')
client.addPublisher('x', 'number')
client.addPublisher('y', 'number')
client.addPublisher('z', 'number')
client.addPublisher('vector', 'vector3')
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

def getIntersection(axisAngleA, planeDistanceA, axisAngleB, planeDistanceB):
    bA = planeDistanceA/math.cos(axisAngleA)
    mA = math.tan(-axisAngleA)
    bB = planeDistanceB/math.cos(axisAngleB)
    mB = math.tan(-axisAngleB)
    x = (bA-bB) / (mB - mA)
    r = np.array([x, mA * x + bA])
    print('intersection: {:.2f},{:.2f} {}'.format(axisAngleA, axisAngleB, str(r)))
    return r

def processC(data):
    # separate the audio by channel
    channels = [[sample[channel] for sample in data] for channel in range(7)]

    # calculate the mic<->mic offset relative to the sound source
    d000 = getDist(channels[1], channels[4])
    d060 = getDist(channels[2], channels[5])
    d120 = getDist(channels[3], channels[6])
    print('distances 0: {:.4f} 60: {:.4f} 120: {:.4f}'.format(d000, d060, d120))
    print(max(d000, d060, d120))

    # calculate the angular offset between the mic<->mic axis
    # and the mic<->sound_source axis
    compareto = .08
    c000 = -1 if np.abs(d000) > compareto else math.acos(d000/compareto)
    c060 = -1 if np.abs(d060) > compareto else math.acos(d060/compareto)
    c120 = -1 if np.abs(d120) > compareto else math.acos(d120/compareto)
    print('angles 0: {:.2f} 60: {:.2f} 120: {:.2f}'.format(c000, c060, c120))

    # calculate the distance along the mic<->mic axis
    # that the mic<->sound_source normalized vector projects to
    D000 = math.cos(c000)
    D060 = math.cos(c060)
    D120 = math.cos(c120)
    print('axis_length 0: {:.2f} 60: {:.2f} 120: {:.2f}'.format(D000, D060, D120))

    # calculate the intersections of the planes defined by
    # that mic<->mic axis and their normalized&projected source distance
    point = np.array([0., 0.])
    numToAvg = 0
    if c000 != -1:
        if c060 != -1:
            point += getIntersection(0, D000, math.pi / 3, D060)
            numToAvg += 1
        if c120 != -1:
            point += getIntersection(0, D000, math.pi * 2 / 3, D120)
            numToAvg += 1
    if c060 != -1:
        if c120 != -1:
            point += getIntersection(math.pi / 3, D060, math.pi * 2 / 3, D120)
            numToAvg += 1
    if numToAvg == 0:
        ## no valid values to use for triangulation, so lets just cut bait
        return

    point = point / numToAvg

    # calculate the "height" of the mic<->source vector
    M = np.linalg.norm(point)
    z = math.sqrt(1 - M * M) if M <= 1 else 0
    point = np.append(point, z)
    print('point: {}'.format(str(point)))

    # publish values
    client.publish('x', point[0])
    client.publish('y', point[1])
    client.publish('z', point[2])
    client.publish('vector', list(point))

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
                print('processed')
except Exception as e:
    print(e)
    traceback.print_exc()
    client.stop()
