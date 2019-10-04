# Spacey Clapper

## Azure Kinect Features

The Azure Kinect is a very capable little device. I have lots of experience using previous Kinect devices for scene segmentation, gestureal interfaces, skeleton tracking, point cloud rendering and so much more. A lot of those features are quicker, higher resolution, more robust, and in a smaller package for this iteration. 

Because the prompt specifically asked me to explore a new feature, I wanted to dig into parts of the Kinect that are vastly different from previous generations, or that I just don't have as much experience with. The circular microphone array on the Azure Kinect immediately caught my interest.

## Documentation of prototype

__TODO__

## Project Vision

I am proposing an interactive installation where the primary interaction is clapping. This clapping gets localized by the Azure Kinect microphone array and triggers a number of effects in the space.

1. Spot lights that pulse at the location from which the clap originated
   * I'm imagining augmenting the sound localization with the 3D camera to be able to pick out individuals in the space
2. The audio of the clap will get added to a sequencer to be able to be replayed
   * The clap audio may be modified, for example with pitch shifting or granular synthesis

As people add to the 'track', older samples will be dropped. If nobody is interacting with the track, previous sequences can fade in and out as the installation "dreams."

## Setup

dev setup details can be found in the Github Wiki for this project
