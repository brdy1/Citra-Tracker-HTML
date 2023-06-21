Adapted version of accrue's Python and json-based tracker.

Still work in progress, no major releases

Requires Python 3.10+ to run. Tested only on 3.11, however.

To change the game, edit the *config.ini* file in the root directory. Replace *game = [gamename]* with the game you will be playing. Be sure to restart the tracker when you do.

To use, run the citra-updater.py file via Python. Then, either direct your favorite browser (tested only on Firefox and Chrome) to http://localhost:8000/tracker.html or add a browser source in OBS directly. Citra must have a ROM open for the tracker to check for data.

![image](https://i.imgur.com/I3AuMwz.png)