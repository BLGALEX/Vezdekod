import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os.path

df = pd.read_csv("nyc_robots.csv", sep=";")
df.head()

starts = df.groupby('start station name').mean()
ends = df.groupby('end station name').mean()
starts_longitude = starts['start station longitude']
starts_latitude = starts['start station latitude']
ends_longitude = ends['end station longitude']
ends_latitude = ends['end station latitude']

min_latitude = 40.6875
max_latitude = 40.7785
min_longitude = -74.1110
max_longitude = -73.9503

if os.path.isfile('map.png'):
    m = plt.imread('map.png')
    print("File exist")
else:
    m = 255 * np.ones(shape=[512, 512, 3], dtype=np.uint8)
    print("File not exist")


fig1, ax1 = plt.subplots(figsize=(10, 8))
sc1 = ax1.scatter(starts_longitude, starts_latitude, zorder=1, alpha=0.7, c='g', s=15, label='first')
annot1 = ax1.annotate("", xy=(0, 0), xytext=(20, 20), textcoords="offset points",
                      bbox=dict(boxstyle="round", fc="w"),
                      arrowprops=dict(arrowstyle="->"))
annot1.set_visible(False)
ax1.set_title('Start points')
ax1.set_xlim(min_longitude, max_longitude)
ax1.set_ylim(min_latitude, max_latitude)
ax1.imshow(m, zorder=0, extent=[min_longitude, max_longitude, min_latitude, max_latitude], aspect='equal')

fig2, ax2 = plt.subplots(figsize=(10, 8))
sc2 = ax2.scatter(ends_longitude, ends_latitude, zorder=1, alpha=0.7, c='r', s=15, label='first')
annot2 = ax2.annotate("", xy=(0, 0), xytext=(20, 20), textcoords="offset points",
                      bbox=dict(boxstyle="round", fc="w"),
                      arrowprops=dict(arrowstyle="->"))
annot2.set_visible(False)
ax2.set_title('End points')
ax2.set_xlim(min_longitude, max_longitude)
ax2.set_ylim(min_latitude, max_latitude)
ax2.imshow(m, zorder=0, extent=[min_longitude, max_longitude, min_latitude, max_latitude], aspect='equal')

fig1.canvas.set_window_title("Interactive map of Start points")
fig2.canvas.set_window_title("Interactive map of End points")


def update_annot1(ind):
    pos = sc1.get_offsets()[ind["ind"][0]]
    annot1.xy = pos
    text = "{}".format(" ".join(str(starts.index[ind["ind"][0]])))
    annot1.set_text(text)
    annot1.get_bbox_patch().set_facecolor('g')
    annot1.get_bbox_patch().set_alpha(0.4)


def hover1(event):
    vis = annot1.get_visible()
    if event.inaxes == ax1:
        cont, ind = sc1.contains(event)
        if cont:
            update_annot1(ind)
            annot1.set_visible(True)
            fig1.canvas.draw_idle()
        else:
            if vis:
                annot1.set_visible(False)
                fig1.canvas.draw_idle()


def update_annot2(ind):
    pos = sc2.get_offsets()[ind["ind"][0]]
    annot2.xy = pos
    text = "{}".format(" ".join(str(ends.index[ind["ind"][0]])))
    annot2.set_text(text)
    annot2.get_bbox_patch().set_facecolor('r')
    annot2.get_bbox_patch().set_alpha(0.4)


def hover2(event):
    vis = annot2.get_visible()
    if event.inaxes == ax2:
        cont, ind = sc2.contains(event)
        if cont:
            update_annot2(ind)
            annot2.set_visible(True)
            fig2.canvas.draw_idle()
        else:
            if vis:
                annot2.set_visible(False)
                fig2.canvas.draw_idle()


fig1.canvas.mpl_connect("motion_notify_event", hover1)
fig2.canvas.mpl_connect("motion_notify_event", hover2)

plt.show()
