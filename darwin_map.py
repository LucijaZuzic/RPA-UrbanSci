import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import cartopy.io.img_tiles as cimgt

fig = plt.figure(figsize = (16, 16), dpi = 300)
plt.rcParams.update({'font.size': 22})
plt.gca().set_aspect('equal') 
plt.title("Darwin, New Territory, Australia")
plt.xlabel("Longitude")
plt.ylabel("Latitude")
proj = ccrs.PlateCarree()

fig = plt.figure(figsize = (16, 16), dpi = 300) 
plt.rcParams.update({'font.size': 22})
x, y = 131.1327361, -12.8437111
main_ax = fig.add_subplot(1, 1, 1, projection = proj)
x1, x2, y1, y2 = 20, 20, 20, 20
main_ax.set_extent([x - x1, x + x2, y - y1, y + y2], crs = proj)
main_ax.gridlines(draw_labels = True)
main_ax.coastlines()

request = cimgt.OSM()
main_ax.add_image(request, 12)

cm = 1/2.54  # centimeters in inches
plt.figure(figsize=(16, 16), dpi = 300)
ax = plt.axes(projection=ccrs.PlateCarree())
ax.coastlines()
plt.title("Darwin, New Territory, Australia")

plt.scatter([x], [y], color = "r", zorder = 2, s = 200)
plt.scatter([x + x1], [y + y1], color = "r", zorder = 2, s = 200, alpha = 0)
plt.scatter([x + x1], [y - y1], color = "r", zorder = 2, s = 200, alpha = 0)
plt.scatter([x - x1], [y + y1], color = "r", zorder = 2, s = 200, alpha = 0)
plt.scatter([x - x1], [y - y1], color = "r", zorder = 2, s = 200, alpha = 0)

plt.savefig("world_map.eps", bbox_inches = "tight")
plt.savefig("world_map.png", bbox_inches = "tight")
plt.savefig("world_map.svg", bbox_inches = "tight")
plt.savefig("world_map.pdf", bbox_inches = "tight")
plt.close()