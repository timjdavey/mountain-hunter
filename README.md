# Mountain Peak finder

It turns out there's no standard definition as to what defines a mountain. As you'd imagine, local cultures take huge pride in what is a mountain, so there's plenty of rule bending. [Wikipedia](https://en.wikipedia.org/wiki/Mountain) as usual does the best job of summarising.

There is however a few standard rules

* Height of peak, absolute from sea level in metres
* [Prominence of peak](https://en.wikipedia.org/wiki/Topographic_prominence), as there's a lot of debate what's a sub peak and part of the main mountain vs what's an independant peak on it's own
* Slope of peak, as short squat peaks don't count but short sharp ones do

## Virgin mountains

If, like me, you want to climb a beautiful pristine unmounted hump then there's a few tactics to employ. And before you switch off and assume this is a fruitless case of intellectual masturbation, there's more unclimbed mountains in this world than climbed ones. So there's plenty left to explore, time to get on it!

#### Go small
It's not about the size, it's about what you do with it that counts. All the big peaks have been climbed, it's a status thing among professionals. So go for the smaller ones. The catch is, not all the small ones (esp northern russia) have been named or identified, so you need to find them with a script like this.

#### Sub-peaks
In the shadow of a monster, is usually hiding a gem. When climbing a peak, the rush and feeling you get is about being at the top (and the ego thing). Who wants to climb the mountain next to Everest, only to get to the top and look over and see Everest looming over you. Not many people. So, look for mountains which could be thought of as just lumps on a larger mountain but have enough topigraphical prominence to classify as being their own mountain.

## Data

Best data source I could find was topographical information from the [NASA Shuttle Radar Topography Mission](http://vterrain.org/Elevation/SRTM/). It's stored in a dense raw format, details of which can be found [here](www2.jpl.nasa.gov/srtm/faq.html). And the data itself can be found [hosted on this independant site](http://www.viewfinderpanoramas.org/dem3.html#nasa).

I've only included a single file in the project as an example because each segment is 2.9mb.

## Peaks
The script `sort_filter.py` finds all the peaks. You can see an illustration, where it's placed a small x at each independant peak. It does a good job in this example of removing a ridge, using the prominence feature below.

![mountains_peaks](https://cloud.githubusercontent.com/assets/13322/21580696/98f33e10-d003-11e6-88ce-050d05703305.png)

## Prominence
The [prominence of peak](https://en.wikipedia.org/wiki/Topographic_prominence) is the height of the peak’s summit above the lowest contour line encircling it but containing no higher summit within it. This prominence must be a certain height for it to be classified as an independant peak (again this varies based on locale).

![mountain prom illustration](https://upload.wikimedia.org/wikipedia/commons/thumb/3/3e/Prominence_definition.svg/250px-Prominence_definition.svg.png)

The file `circles.py` does a quick verification to find the contour of a peak and see if there's any peaks within. Contour illustrated below.

![mountains_prominence](https://cloud.githubusercontent.com/assets/13322/21580695/98d54126-d003-11e6-87b4-fdbdb25433cc.png)
