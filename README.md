<a name="readme-top"></a>
<!-- TABLE OF CONTENTS -->
<details>
  <summary>Table of Contents</summary>
  <ol>
    <li>
      <a href="#emtools">EMTools</a>
      <ul>
        <li><a href="#makekmz">MakeKMZ</a></li>
      </ul>
    </li>
    <li><a href="#license">License</a></li>
    <li><a href="#contact">Contact</a></li>
  </ol>
</details>

<br>

<!-- ABOUT THE PROJECT -->
# EMTools

The EMTools consists of several programs useful for geosciences.

## makeKMZ
Python class to create a KMZ file to plot colored circle icons in Google Earth by using the lists of longitudes, latitudes and values.

### Requirements
- Python 3.9.15
- matplotlib 3.6.3
- numpy 1.23.5
- pillow 9.4.0

### Usage
Just import `MakeKMZ` and call the `make_kmz` function.
```python
import makeKMZ
makeKMZ.make_kmz(kmzname, lon, lat, values, list_label)
```
where parameters are

    kmzname (str): Name of the output KMZ file.
    lon ([float]): Array of longitudes.
    lat ([float]): Array of latitudes.
    values ([float]): Array of values used for the color scale.
    list_label ([str]): List of labels of icons.

### Demo
See `example/earthquakes.py`, which creates a map of the [20 largest earthquakes](https://www.usgs.gov/programs/earthquake-hazards/science/20-largest-earthquakes-world) listed on the USGS website.

The screenshot of the output kmz file opened in Google Earth is 
![Product Name Screen Shot](example/earthquakes_google_earth.png)

<p align="right">(<a href="#readme-top">back to top</a>)</p>


<!-- LICENSE -->
## License

Distributed under the MIT License. See `LICENSE` for more information.

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- CONTACT -->
## Contact

Kentaro Emoto - emoto.kentaro.430@m.kyushu-u.ac.jp

Project Link: [https://github.com/KentaroEmoto/EMTools](https://github.com/KentaroEmoto/EMTools)

<p align="right">(<a href="#readme-top">back to top</a>)</p>



