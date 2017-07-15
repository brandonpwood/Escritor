# Overeview
A simple python package for graphing connections between facebook pages.
The Graphs are directed and edges represent likes between pages.
# Use
Use requires you create a facebook app and retrieve a token for the graph API, which can be done here:
https://developers.facebook.com/tools/explorer/
The keys will need to be updated periodically.

Additionally, there are included functions to save and read graph data from csv files.
It can also save images as png files and will graph the connections with the page names as labels or
the degree of each node (with a normalized color map based on the degree).

# Example graphs
## Scraped 200 pages
![](graph200.png)
![](graph200name.png)

## Scraped 50 pages
![](graph50.png)
![](graph50name.png)

## Scraped 25 pages
![](graph25.png)
![](graph25name.png)
