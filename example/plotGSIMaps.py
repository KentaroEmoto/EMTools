import sys
sys.path.append("../src")
import getGSIMaps
import pygmt

lon1 = 130.098381
lat1 = 32.576906
lon2 = 130.455437
lat2 = 32.892849
zoom = 12
map_type = 'seamlessphoto'
figure_size = 10
img_gsimap = 'tmp_gsimap.png'

getGSIMaps.create_image(img_gsimap, lon1, lat1, lon2, lat2, map_type=map_type, zoom=zoom)

projection='M'+str(figure_size)
image_position = 'g'+str(lon1)+'/'+str(lon2) + '+w' + str(figure_size)
region = [lon1, lon2, lat1, lat2]

fig = pygmt.Figure()
pygmt.config(FORMAT_GEO_MAP='ddd.xx', MAP_TICK_LENGTH='-0.1c', MAP_FRAME_WIDTH='1p')
fig.image(imagefile=img_gsimap, projection=projection, region=region, position=image_position)
fig.basemap(frame=['nSeW', 'xya0.05'])
fig.savefig('./demo_gsimaps.png')