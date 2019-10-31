# Spacey Clapper

<div style="padding:56.25% 0 0 0;position:relative;"><iframe src="https://player.vimeo.com/video/369975776" style="position:absolute;top:0;left:0;width:100%;height:100%;" frameborder="0" allow="autoplay; fullscreen" allowfullscreen></iframe></div><script src="https://player.vimeo.com/api/player.js"></script>
<p><a href="https://vimeo.com/369975776">Audio Localization Demo</a> from <a href="https://vimeo.com/quinkennedy">quin kennedy</a> on <a href="https://vimeo.com">Vimeo</a>.</p>

## Azure Kinect Features

The Azure Kinect is a very capable little device. I have lots of experience using previous Kinect devices for scene segmentation, gestureal interfaces, skeleton tracking, point cloud rendering and so much more. A lot of those features are quicker, higher resolution, more robust, and in a smaller package for this iteration. 

Because the prompt specifically asked me to explore a new feature, I wanted to dig into parts of the Kinect that are vastly different from previous generations, or that I don't have as much experience with. The circular microphone array on the Azure Kinect immediately caught my interest.

## Documentation of prototype

I have put together a technical prototype which listens for claps and snaps, 
and calculates the direction from which the sound came. Even though solutions 
for this exist which are much more robust than what I could build in a couple of days, 
I wanted to prove out that the Kinect microphone array was accessible enough 
and high-quality enough to be able to support this use-case without getting 
into the weeds on implementing or compiling research-grade projects. 

![visualization][im0]
*This shows a clap coming almost directly from the right side of the kinect*

This prototype uses Python to analyze the microphone channels and calculate 
the directionality of sound sources. That direction is published over 
Spacebrew to allow for flexibility in the visualization side. 
I put together a simple web visualizer (shown above) to display the direction relative to the 
Azure Kinect in both plan and azimuth view.

See the [Github Wiki][0] for details on setting up the prototype.

## Project Vision

I am proposing an interactive installation where the primary interaction is clapping. This clapping gets localized by the Azure Kinect microphone array and triggers a number of effects in the space.

1. Spot lights that pulse at the location from which the clap originated
   * I'm imagining augmenting the sound localization with the 3D camera to be able to pick out individuals in the space
2. The audio of the clap will get added to a sequencer to be able to be replayed and looped into a percussive track
   * The clap audio may be modified, for example with pitch shifting or granular synthesis

As people add to the 'track', older samples will be dropped. If nobody is interacting with the track, previous sequences can fade in and out as the installation "dreams."

![installation view][im1]

This installation view shows an arrangement with:

* an upside-down kinect mounted in the top center of the space
* a mirror redirecting the depth camera to see the floor to allow for depth-assisted clapper locating
* a moving mirror lights to highlight the identified clapper
* speakers in the grid
* LED panels scattered around the walls and in the floor which will additionally react based on the spatialized sound and activate the space with ambient content.


[0]: https://github.com/Embodied-Space/AzureKinectExperiments/wiki/Dev-Setup
[im0]: images/sound-source-01a.png
[im1]: images/installation-view.jpg
