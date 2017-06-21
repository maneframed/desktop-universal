# desktop-universal
Universal Desktop Client for Maneframe. 

## Design notes
- Python 3.5 is used to maintain compatibility with core ML library, Tensorflow. As of June 20, 2017 Tensorflow library is only compatible with Windows Python 3.5
- WebSockets have been used for bi-directional communication between Desktop software and Web-API. We tried looking into socketIO, however client support has been confined to 
a single rarely maintained library. In comparison Websockets library has been very well maintained, hence we decided to go with Websockets implementation rather than socketIO.
- TKInter is chosen for the very first version of the software due to time restrictions, we have all intention to move to QT5 or another advanced visualization library.
