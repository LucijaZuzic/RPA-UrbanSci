import matplotlib.pyplot as plt
from matplotlib.transforms import offset_copy
import numpy as np
import cartopy.crs as ccrs
import cartopy.io.img_tiles as cimgt
from cartopy.io.img_tiles import GoogleTiles

class ShadedReliefESRI(GoogleTiles):
    # shaded relief
    def _image_url(self, tile):
        x, y, z = tile
        url = ("https://server.arcgisonline.com/ArcGIS/rest/services/World_Street_Map/MapServer/tile/{z}/{y}/{x}.jpg").format(z = z, y = y, x = x)
        return url

x, y = 131.1327361, -12.8437111
x1, x2, y1, y2 = 20, 20, 20, 20

fig = plt.figure(figsize = (16, 16), dpi = 300)
ax = plt.axes(projection = ShadedReliefESRI().crs)
ax.set_extent([x - x1, x + x2, y - y1, y + y2])
ax.gridlines(draw_labels = True)
ax.coastlines()
ax.add_image(ShadedReliefESRI(), 5)
plt.title("The position of the Darwin, Northern Territory, Australia IGS reference station")
plt.xlabel("Longitude")
plt.ylabel("Latitude")

# Add a marker for the Darwin, Northern Territory, Australia station.
ax.plot(x, y, marker = "o", color = "red", markersize = 12, alpha = 0.7, transform = ccrs.Geodetic(), label = "The position of the IGS reference station")
plt.legend()

# Use the cartopy interface to create a matplotlib transform object
# for the Geodetic coordinate system. We will use this along with
# matplotlib"s offset_copy function to define a coordinate system which
# translates the text by 25 pixels to the left.
geodetic_transform = ccrs.Geodetic()._as_mpl_transform(ax)

# Add text 25 pixels to the left of the station.
text_transform = offset_copy(geodetic_transform, units = "dots", x = -25)
ax.text(x, y, u"Darwin, Northern Territory, Australia", verticalalignment = "center", horizontalalignment = "right", transform = text_transform, bbox = dict(facecolor = "sandybrown", alpha = 0.5, boxstyle = "round"))

x3, y3, rl1, rl2 = 15, 15, 2, 3
xs, ys = x + x3, y + y3

angle_and_marker_list = {0: "E", 90: "N", 180: "W", 270: "S"}
repeat_divide = 2
for i in range(repeat_divide):
    angles_sorted = sorted(list(angle_and_marker_list))
    for ix in range(len(angles_sorted)):
        a1 = angles_sorted[ix]
        m1 = angle_and_marker_list[a1]
        if ix + 1 < len(angles_sorted):
            a2 = angles_sorted[ix + 1]
            m2 = angle_and_marker_list[a2]
        else:
            a2 = 360
            m2 = angle_and_marker_list[0]
        a3 = (a1 + a2) / 2
        if len(m1) < len(m2) or (len(m1) == len(m2) and m1 in ["N", "S"]):
            m3 = m1 + m2
        else:
            m3 = m2 + m1
        angle_and_marker_list[a3] = m3
print(angle_and_marker_list)

for angle in angle_and_marker_list:
    angle_radians = angle / 180 * np.pi
    xa, ya = np.cos(angle_radians) * rl1, np.sin(angle_radians) * rl1
    xt, yt = xs + np.cos(angle_radians) * rl2, ys + np.sin(angle_radians) * rl2
    plt.annotate("", xy = (xs, ys), xytext = (xs + xa, ys + ya), xycoords = text_transform, arrowprops = dict(arrowstyle = "<-"))
    ax.text(xt, yt, angle_and_marker_list[angle], verticalalignment = "center", horizontalalignment = "center", transform = text_transform)
    
ax.text(x, y - y1 - rl2, "Longitude", horizontalalignment = "center", transform = text_transform)
ax.text(x - x1 - rl1, y, "Latitude", verticalalignment = "center", rotation = "vertical", transform = text_transform)

plt.savefig("world_map.eps", bbox_inches = "tight")
plt.savefig("world_map.png", bbox_inches = "tight")
plt.savefig("world_map.svg", bbox_inches = "tight")
plt.savefig("world_map.pdf", bbox_inches = "tight")
plt.close()