Evolving into a Monkey
======================

15.4.2009

Just like just about everyone else over here on the Internet, some time ago I came across [a blog post by a Roger Alsing](http://rogeralsing.com/2008/12/07/genetic-programming-evolution-of-mona-lisa/) in which he describes a simple genetic programming experiment with image processing. And just like many programmers who stumbled onto the post, I too wanted to try it myself.


The experiment, as described in the post by Alsing, was to see if slight mutations of a “DNA” string describing a group of semi-transparent polygons could be used to produce a reproduction of another image (in Alsing’s case, the Mona Lisa). The program generates a random DNA string to represent the initial polygons. The program then starts a the evolution process and perform simple mutations on the DNA string. The mutations consist of changing the color of a polygon, adding or removing polygons, and changing the points of polygons. After mutating the DNA string, the image generated from the DNA is compared to the target image to see how closely it represents the target. If the mutation is an improvement over the original DNA string, the mutated DNA then becomes the base for the next iteration of mutations.

I think the idea is simple and pretty cool, but by itself it probably wouldn’t be enough to get many people that interested in it. What made it so interesting were the results Alsing got from the experiment. The images of the process at various points can be seen in the original post and show how impressive the technique is. So impressive that I couldn’t wait to find the time to try it out myself.

After a few weeks of research and programming in my spare time, I now have something ready enough that I don’t feel completely uncomfortable with writing about it. I did take a cursory glance at Alsings source code before I got started, but I didn’t really get much out of it at that time. Probably now that I have some experience with what the difficult parts have been for me, I might enjoy seeing how he’s solved them. I started out with using [wxPython](http://www.wxpython.org/) to draw the polygons, but eventually, when performance started to become an issue, I switched to [PIL](http://www.pythonware.com/products/pil/) and [aggdraw](http://effbot.org/zone/aggdraw-index.htm). For pixel comparisons I use [NumPy](http://numpy.scipy.org/). I still use wxPython to display the images I generate.

After getting the basic system up and running, most of my time has been spent tweaking the mutation process. Early on I realized the mutations can’t be completely random, but instead randomly generated small changes. I place constraints on how much colors can change, how much points in a polygon can move, and where new points can be created in a single mutation step. Another change I am playing with is increasing the population size from just two to six, with the three worst specimens replaced at each step.

The program I wrote gets up to a very crude, but recognizable mess of polygons pretty quickly, but even after running for a whole five days, the generated image is nowhere near the quality of the images Alsing was able to create.

![](https://lh5.googleusercontent.com/-Pp3JIWAC6Vk/SeXZUBdrphI/AAAAAAAAAyc/IALOjHf0JVs/s640/evomonkey5.png)

You can download the current source from here. To run it you need to have [wxPython](http://www.wxpython.org/), [PIL](http://www.pythonware.com/products/pil/), [aggdraw](http://effbot.org/zone/aggdraw-index.htm) and [NumPy](http://numpy.scipy.org/) installed. To start it up, just call:

    python genui.py <target image file>

Any questions, comments or improvements? Please let me know.
