# HandsfreeTV

HandsfreeTV was created with the intent of giving everyone a hands-free experience while watching entertainment. We approached this idea by combining two previously disjoint user-interfaces, voice and gesture recognition. By combining these two modules we can create a natural and comprehensive way to interact with today’s digital entertainment.

As of now, HandsfreeTV works to use voice and gestures to search for and control YouTube videos. You can find a video demo [here](https://youtu.be/1v2MmMLJ3HA).

## Gesture Detection

For gesture detection we are currently using an open-source Google Research project called [MediaPipe](https://github.com/google/mediapipe). We are using their [realtime hand-tracking](https://ai.googleblog.com/2019/08/on-device-real-time-hand-tracking-with.html) to get hand features and passing that image to a custom CNN model trained on over 15,000 collected images. Currently, the model can has 7 classifiers (fist, palm, right, left, up, down, and other).

<p align="center">
    <img src="gesture_tracking.gif" width="640" height="470"/>
</p>

## Voice Control

Our voice control module uses Google Cloud Platform's [Speech-to-Text](https://cloud.google.com/speech-to-text/). Specifically we are always [streaming audio.](https://cloud.google.com/speech-to-text/docs/streaming-recognize) 

## Putting it Together

Currently, HandsfreeTV uses 4 hand gestures to control YouTube videos (fist-pause, palm-play, up-volume up, down-volume down). If the voice control module hears the keyword "Search" at the beginning of a phrase, the rest of the phrase is used to search on YouTube and the first result is opened up. All of the YouTube interactions are handled using Selenium.

## What's next

The goal for HandsfreeTV was to test an alternative user-interface for Smart TV's that does not include touch. Uses for this include removing the need for remotes or scrolling through a recipe while your hands are dirty from cooking. Thus YouTube was a good platform to test these new modules, but the long-term goal would be to incorporate HandsfreeTV directly onto Smart TV's for their applications to utilize.

In addition, because this project was hacked together at SBHacks 2020, there are many improvements to be made: 
1. Overall Code Structure - Modulize each component, rather than throwing everything in one `main.py`
2. Properly retrieve data from MediaPipe - Currently we are using a rudimentary hack of writing images to files and reading the second most recently modified file to pass data from MediaPipe to our code. Alternative methods to fixing this:
    * Passing images through shared memory or TCP sockets
    * Writing a python wrapper around MediaPipe - this method would also allow us to retrieve intermediate information such as feature locations rather than just the final image output.
