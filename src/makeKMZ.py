import numpy as np
import matplotlib
import matplotlib.cm as cm
import matplotlib.colors as mcolors
import matplotlib.pyplot as plt
import zipfile
from PIL import Image
import os

#-------------------------
# update: 2022.01.14 Added icon edge option.
#-------------------------

def __make_cmap(color_name='jet', n_colors=10):
    """Generate discrete color list.

    Args:
        color_name (str, optional): Name of the colormap (see https://matplotlib.org/stable/gallery/color/colormap_reference.html). Defaults to 'jet'.
        n_colors (int, optional): Number of discretization. Defaults to 10.

    Returns:
        [str]: List of hex strings of discretized colors. The order is ABGR.
    """
    cmap = cm.get_cmap(color_name, n_colors)
    clist = []
    for i in range(cmap.N):
        rgb_hex = mcolors.rgb2hex(cmap(i))
        cstr = 'ff'+rgb_hex[5:7]+rgb_hex[3:5]+rgb_hex[1:3]
        clist.append(cstr)
    return clist

def __write_kml(kmlname, color_list, icon_size, color_index, list_label, lon, lat):
    """Write KML file.

    Args:
        kmlname (str): Name of the output KML file.
        color_list ([str]): List of the hex strings of the color map.
        icon_size (float or [float]): Scalar or array. Size of the icon. Both for the normal and hilight.
        color_index ([int]): List of indices of color_list.
        list_label ([str]): List of labels of icons.
        lon ([float]): Array of longitudes.
        lat ([float]): Array of Latitude.
    """
    #icon = 'http://www.gstatic.com/mapspro/images/stock/959-wht-circle-blank.png'
    icon = 'icon_circle.png'
    lines = []
    lines.append('<?xml version="1.0" encoding="UTF-8"?>')
    lines.append('<kml xmlns="http://www.opengis.net/kml/2.2">')
    lines.append('  <Document>')
    lines.append('    <name>untitled</name>')
    for i in range(len(color_list)):
        lines.append('    <Style id="icon-'+str(i)+'-normal">')
        lines.append('      <IconStyle>')
        lines.append('        <color>'+color_list[i]+'</color>')
        if(np.isscalar(icon_size)):
            lines.append('        <scale>'+str(icon_size)+'</scale>')
        lines.append('        <Icon>')
        lines.append('          <href>'+icon+'</href>')
        lines.append('        </Icon>')
        lines.append('      </IconStyle>')
        lines.append('      <LabelStyle>')
        lines.append('        <scale>0</scale>')
        lines.append('      </LabelStyle>')
        lines.append('      <BalloonStyle>')
        lines.append('        <text><![CDATA[<h3>$[name]</h3>]]></text>')
        lines.append('      </BalloonStyle>')
        lines.append('    </Style>')
        lines.append('    <Style id="icon-'+str(i)+'-highlight">')
        lines.append('      <IconStyle>')
        lines.append('        <color>'+color_list[i]+'</color>')
        if(np.isscalar(icon_size)):
            lines.append('        <scale>+'+str(icon_size)+'</scale>')
        lines.append('        <Icon>')
        lines.append('          <href>'+icon+'</href>')
        lines.append('        </Icon>')
        lines.append('      </IconStyle>')
        lines.append('      <LabelStyle>')
        lines.append('        <scale>1</scale>')
        lines.append('      </LabelStyle>')
        lines.append('      <BalloonStyle>')
        lines.append('        <text><![CDATA[<h3>$[name]</h3>]]></text>')
        lines.append('      </BalloonStyle>')
        lines.append('    </Style>')
        lines.append('    <StyleMap id="icon-'+str(i)+'">')
        lines.append('      <Pair>')
        lines.append('        <key>normal</key>')
        lines.append('        <styleUrl>#icon-'+str(i)+'-normal</styleUrl>')
        lines.append('      </Pair>')
        lines.append('      <Pair>')
        lines.append('        <key>highlight</key>')
        lines.append('        <styleUrl>#icon-'+str(i)+'-highlight</styleUrl>')
        lines.append('      </Pair>')
        lines.append('    </StyleMap>')
        lines.append('')
        lines.append('')
    for j in range(len(color_index)):
        lines.append('    <Placemark>')
        lines.append('      <name>'+str(list_label[j])+'</name>')
        lines.append('      <styleUrl>#icon-' +
                     str(color_index[j])+'</styleUrl>')
        if(not np.isscalar(icon_size)):
            lines.append('      <Style>')
            lines.append('        <IconStyle>')
            lines.append('          <scale>'+str(icon_size[j])+'</scale>')
            lines.append('        </IconStyle>')
            lines.append('      </Style>')
        lines.append('      <Point>')
        lines.append('        <coordinates>')
        lines.append('          '+str(lon[j]) + ','+str(lat[j])+',0')
        lines.append('        </coordinates>')
        lines.append('      </Point>')
        lines.append('    </Placemark>')
        lines.append('')
    lines.append('    <ScreenOverlay>')
    lines.append('      <name>Legend</name>')
    lines.append('      <Icon>')
    lines.append('        <href> colorbar.png </href>')
    lines.append('      </Icon>')
    lines.append('      <overlayXY x="0" y="0" xunits="fraction" yunits="fraction"/>')
    lines.append('      <screenXY x="25" y="95" xunits="pixels" yunits="pixels"/>')
    lines.append('      <size x="0" y="0" xunits="pixels" yunits="pixels"/>')
    lines.append('    </ScreenOverlay>')
    lines.append('  </Document>')
    lines.append('</kml>')
    with open(kmlname, 'w') as f:
        for line in lines:
            f.write(line + '\n')

def __make_colorbar(vmin, vmax, color_name, n_colors, log_scale=False):
    """Create color bar image.

    Args:
        vmin (float): Minimum value of the color scale.
        vmax (float): Maximum value of the color scale.
        color_name (str): Name of the colormap (see https://matplotlib.org/stable/gallery/color/colormap_reference.html).
        n_colors (int): Number of discretization.
        log_scale (bool, optional): Create log-scale color bar. Defaults to False.
    """
    plt.rcParams['ytick.direction'] = 'in'
    fig, ax = plt.subplots(figsize=(0.2, 3))
    cmap = cm.get_cmap(color_name, n_colors)
    if(log_scale):
        norm = matplotlib.colors.LogNorm(vmin=vmin, vmax=vmax)
    else:
        norm = matplotlib.colors.Normalize(vmin=vmin, vmax=vmax)
    cbar = matplotlib.colorbar.ColorbarBase(
        ax=ax,
        cmap=cmap,
        norm=norm,
        orientation="vertical",
    )
    plt.savefig("colorbar.png", bbox_inches="tight")
    plt.close()

def __make_icon(edge=True):
    """Create icon image.

    Args:
        edge (bool, optional): Draw edge with the black color. Defaults to True.
    """
    fig = plt.figure(dpi=400, figsize=(0.065,0.065), frameon=False)
    ax = fig.add_subplot(1,1,1)
    edgecolor = 'black' if edge else 'white'
    ax.scatter(0, 0, 12, color='white', linewidth=0.2, edgecolor=edgecolor)
    ax.axis('off')
    fig.savefig('icon_circle.png')
    plt.close()
    im = Image.open('icon_circle.png')
    im2 = im.crop(im.getbbox())
    im2.save('icon_circle.png')

def make_kmz(kmzname, lon, lat, values, list_label, colormap_name='jet', n_colors=10, vmin=None, vmax=None, log_scale=False, icon_size=0.5, icon_edge=True):
    """Create KMZ file which includes icons with different colors corresponding to "values".

    Args:
        kmzname (str): Name of the output KMZ file.
        lon (float): Array of longitudes.
        lat (float): Array of latitudes.
        values (float): Array of values used for the color scale.
        list_label ([str]): List of labels of icons.
        colormap_name (str, optional): Name of the colormap (see https://matplotlib.org/stable/gallery/color/colormap_reference.html). Defaults to 'jet'.
        n_colors (int, optional): Number of discretization. Defaults to 10.
        vmin (float, optional): Minimum value of the color scale. Defaults to np.min(values).
        vmax (float, optional): Maximum value of the color scale. Defaults to np.max(values).
        log_scale (bool, optional): Create log-scale color bar. Defaults to False.
        icon_size (float or [float], optional): Scalar or array of the icon size. Defaults to 0.5.
        icon_edge (bool, optional): Draw edge with the black color. Defaults to True.
    """
    if(vmin is None):
        vmin = np.min(values)
    if(vmax is None):
        vmax = np.max(values)
    if(log_scale): 
        dvalue = (np.log10(vmax)-np.log10(vmin))/n_colors
    else:
        dvalue = (vmax-vmin)/n_colors
    color_list = __make_cmap(colormap_name, n_colors)
    color_index = np.zeros(len(lon), dtype=np.int)
    for i in range(len(lon)):
        if(log_scale):
            index = int((np.log10(values[i])-np.log10(vmin))/dvalue)
        else:
            index = int((values[i]-vmin)/dvalue)
        if(index < 0):
            index = 0
        if(index > (n_colors-1)):
            index = n_colors-1
        color_index[i] = index
    __write_kml('tmp.kml', color_list, icon_size, color_index, list_label, lon, lat)
    __make_colorbar(vmin, vmax, colormap_name, n_colors, log_scale=log_scale)
    __make_icon(icon_edge)
    with zipfile.ZipFile(kmzname, 'w', compression=zipfile.ZIP_DEFLATED) as zp:
        zp.write('tmp.kml')
        zp.write('colorbar.png')
        zp.write('icon_circle.png')
    os.remove('tmp.kml')
    os.remove('colorbar.png')
    os.remove('icon_circle.png')




