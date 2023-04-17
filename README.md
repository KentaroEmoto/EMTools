<a name="readme-top"></a>
<!-- TABLE OF CONTENTS -->
<details>
  <summary>Table of Contents</summary>
  <ol>
    <li>
      <a href="#about-the-project">About The Project</a>
      <ul>
        <li><a href="#built-with">Built With</a></li>
      </ul>
    </li>
    <li>
      <a href="#getting-started">Getting Started</a>
      <ul>
        <li><a href="#prerequisites">Prerequisites</a></li>
        <li><a href="#installation">Installation</a></li>
      </ul>
    </li>
    <li><a href="#usage">Usage</a></li>
    <li><a href="#roadmap">Roadmap</a></li>
    <li><a href="#contributing">Contributing</a></li>
    <li><a href="#license">License</a></li>
    <li><a href="#contact">Contact</a></li>
    <li><a href="#acknowledgments">Acknowledgments</a></li>
  </ol>
</details>

<br>

<!-- ABOUT THE PROJECT -->
# EMTools

The EMTools consists of several programs useful for geosciences.

## makeKMZ
Python class to create a KMZ file to plot colored circle icons in Google Earth by using the lists of longitudes, latitudes and values.
### Usage
Just import `MakeKMZ` and call the `make_kmz` function.
```python
import makeKMZ
makeKMZ.make_kmz(kmzname, lon, lat, values, list_label)
```
where

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



