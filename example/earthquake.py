import sys
sys.path.append("../src")
import makeKMZ

filename = './usgs_largest_earthquakes.txt'
lon = []
lat = []
mag = []
dep = []
label = []
with open(filename, mode='r') as f:
    lines = f.readlines()
    for line in lines:
        elements = line.split(',')
        lat.append(float(elements[0]))
        lon.append(float(elements[1]))
        mag.append((float(elements[2])-8)*5)
        dep.append(float(elements[3]))
        label1 = elements[4] + ', ' + elements[5]
        label.append(label1)

makeKMZ.make_kmz('earthquakes.kmz', lon, lat, dep, label, icon_size=mag, vmin=0, vmax=40)



