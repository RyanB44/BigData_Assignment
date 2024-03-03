import numpy as np
import json
from redis_connect import get_redis_connection
import matplotlib.pyplot as plt

r = get_redis_connection()


class Process:

    def __init__(self):
        self.popularity_vs_duration()
        print(self.get_only_track_names())
        self.plot_explicits()

    def popularity_vs_duration(self):
        """Create scatter plot for popularity vs duration to see if there is a correlation

         Returns:
             n/a shows a plot
         """
        x = []
        y = []
        for i in range(50):
            json_data = r.json().get('playlist:tracks:track{idx}'.format(idx=i))
            data = json.loads(json_data)
            x.append(data['items'][0]['track']['popularity'])
            y.append(data['items'][0]['track']['duration_ms'])

        x = np.array(x)
        y = np.array(y)
        plt.scatter(x, y)
        plt.show()

    def get_only_track_names(self):
        """Create a list of track names for the first 50 tracks in the playlist

         Returns:
             tracknames: a list of all track names
         """
        tracknames = []
        for i in range(50):
            tracknames.append(r.json().get('playlist:tracks:track{idx}:items:track:name'.format(idx=i)))
        return tracknames

    def plot_explicits(self):
        """Create pie chart on which songs are explicit vs which are not

         Returns:
             n/a shows a plot
         """
        numexplicit = 0
        numtotal = 0
        for i in range(100):
            json_data = r.json().get('playlist:tracks:track{idx}'.format(idx=i))
            data = json.loads(json_data)
            if data['items'][0]['track']['explicit']:
                numexplicit += 1
            numtotal += 1

        x = np.array([numexplicit, numtotal - numexplicit])
        labels = ['Explicit', 'Non-Explicit']
        plt.pie(x, labels=labels)
        plt.show()
