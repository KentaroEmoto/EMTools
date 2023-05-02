import requests
import numpy as np
import sys
from typing import Tuple
from PIL import Image
from io import BytesIO

def __get_image(x: int, y: int, zoom: int, map_type: str, extension: str) -> Image.Image:
    """Download tile image.

    Args:
        x (int): x index of the tile
        y (int): y index of the tile
        zoom (int): zoom level of the tile
        map_type (str): tile id of the map type
        extension (str): extension of the tile image. It depends on the map_type. 'jpg' or 'png'

    Returns:
        Image.Image: tile image
    """
    url_key = 'https://cyberjapandata.gsi.go.jp/xyz/'+map_type+'/'+str(zoom)+'/'
    url = url_key + str(x) + '/' + str(y) + '.' + extension
    img = Image.open(BytesIO(requests.get(url).content))
    return img

def __from_lonlat_to_tile(lon: float, lat: float, zoom: int) -> Tuple[int, int, int, int]:
    """Calculate the tile index which contains the point indicated by the longitude, latitude and zoom level.

    Args:
        lon (float): Longitude in degrees
        lat (float): Latitude in degrees
        zoom (int): Zoom level of the tile

    Returns:
        Tuple[int, int, int, int]: x and y indices of the tile and x and y positions in the tile in pixels
    """
    zoom_factor = np.power(2, zoom+8)
    x = zoom_factor * (lon + 180) / 360
    y = zoom_factor * ((1 - np.log(np.tan(np.deg2rad(lat)) + 1 / np.cos(np.deg2rad(lat))) / np.pi) / 2)
    x_tile = int(x/256)
    y_tile = int(y/256)
    x_px = int(np.mod(x, 256))
    y_px = int(np.mod(y, 256))
    return x_tile, y_tile, x_px, y_px

def __set_zoom_level(lon1: float, lat1: float, lon2: float, lat2: float) -> int:
    """_summary_

    Args:
        lon1 (float): Longitude of the bottom left corner of the region
        lat1 (float): Latitude of the bottom left corner of the region
        lon2 (float): Longitude of the top right corner of the region
        lat2 (float): Latitude of the top right corner of the region

    Returns:
        int: Zoom level of the tile
    """
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    delta = max(dlon, dlat)
    zoom = int(np.log2(720) - np.log2(delta)) + 1
    if(zoom > 18):
        zoom = 18
    if(zoom < 1):
        zoom = 1
    return zoom


def create_image(out_image_name: str, lon1: float, lat1: float, lon2: float, lat2: float, zoom: int = None, map_type: str = 'std'):
    """Download tiles within the region and save them as an image.

    Args:
        out_image_name (str): Output image name
        lon1 (float): Longitude of the bottom left corner of the region
        lat1 (float): Latitude of the bottom left corner of the region
        lon2 (float): Longitude of the top right corner of the region
        lat2 (float): Latitude of the top right corner of the region
        zoom (int, optional): Zoom level of the tile. 1:global to 18:local. Defaults to None.
        map_type (str, optional): Tile ID of the map type. 'std', 'pale', 'english', 'seamlessphoto', and etc. (See https://maps.gsi.go.jp/development/ichiran.html). Defaults to 'std'.
    """
    if zoom is None:
        zoom = __set_zoom_level(lon1, lat1, lon2, lat2)
        print('zoom level:', zoom)
    extension = 'png'
    if((map_type=='seamlessphoto') | (map_type=='ort')):
        extension = 'jpg'
    x_l, y_b, x_l_px, y_b_px = __from_lonlat_to_tile(lon1, lat1, zoom)
    _, y_t, _, y_t_px = __from_lonlat_to_tile(lon1, lat2, zoom)
    x_r, _, x_r_px, _ = __from_lonlat_to_tile(lon2, lat2, zoom)
    n_tile_x = x_r - x_l + 1
    n_tile_y = y_b - y_t + 1
    n_tile = n_tile_x * n_tile_y
    if(n_tile > 500):
        print('Too many tiles. Reduce the zoom level.')
        sys.exit(1)
    width = 256*n_tile_x - x_l_px - (256-x_r_px)
    height = 256*n_tile_y - y_t_px - (256-y_b_px)
    img_comb = Image.new('RGB', (width, height))

    x_max = 256 if n_tile_x>=2 else x_r_px
    y_max = 256 if n_tile_y>=2 else y_b_px
    x_min = 0 if n_tile_x>=2 else x_l_px
    y_min = 0 if n_tile_y>=2 else y_t_px

    # left top
    img1 = __get_image(x_l, y_t, zoom, map_type, extension).crop((x_l_px, y_t_px, x_max, y_max))
    img_comb.paste(img1, (0, 0))
    # left bottom
    img1 = __get_image(x_l, y_b, zoom, map_type, extension).crop((x_l_px, y_min, x_max, y_b_px))
    img_comb.paste(img1, (0, (n_tile_y-1)*256-y_t_px+y_min))
    # right top
    img1 = __get_image(x_r, y_t, zoom, map_type, extension).crop((x_min, y_t_px, x_r_px, y_max))
    img_comb.paste(img1, ((n_tile_x-1)*256-x_l_px+x_min, 0))
    # right bottom
    img1 = __get_image(x_r, y_b, zoom, map_type, extension).crop((x_min, y_min, x_r_px, y_b_px))
    img_comb.paste(img1, ((n_tile_x-1)*256-x_l_px+x_min, (n_tile_y-1)*256-y_t_px+y_min))

    for i in range(n_tile_x-2):
        # top
        img1 = __get_image(x_l+i+1, y_t, zoom, map_type, extension).crop((0, y_t_px, 256, y_max))
        img_comb.paste(img1, ((i+1)*256-x_l_px, 0))
        # bottom
        img1 = __get_image(x_l+i+1, y_b, zoom, map_type, extension).crop((0, y_min, 256, y_b_px))
        img_comb.paste(img1, ((i+1)*256-x_l_px, (n_tile_y-1)*256-y_t_px+y_min))
    for i in range(n_tile_y-2):
        # left
        img1 = __get_image(x_l, y_t+i+1, zoom, map_type, extension).crop((x_l_px, 0, x_max, 256))
        img_comb.paste(img1, (0, (i+1)*256-y_t_px))
        # right
        img1 = __get_image(x_r, y_t+i+1, zoom, map_type, extension).crop((x_min, 0, x_r_px, 256))
        img_comb.paste(img1, ((n_tile_x-1)*256-x_l_px+x_min, (i+1)*256-y_t_px))

    for i in range(n_tile_x-2):
        for j in range(n_tile_y-2):
            img1 = __get_image(x_l+i+1, y_t+j+1, zoom, map_type, extension)
            img_comb.paste(img1, ((i+1)*256-x_l_px, (j+1)*256-y_t_px))
    img_comb.save(out_image_name)



