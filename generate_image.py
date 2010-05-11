#!/usr/bin/python
#
# Generates a single large PNG image for a UK bounding box
# Tweak the lat/lon bounding box (ll) and image dimensions
# to get an image of arbitrary size.
#
# To use this script you must first have installed mapnik
# and imported a planet file into a Postgres DB using
# osm2pgsql.
#
# Note that mapnik renders data differently depending on
# the size of image. More detail appears as the image size
# increases but note that the text is rendered at a constant
# pixel size so will appear smaller on a large image.

import mapnik
import sys, os

input = sys.argv[1]
output = sys.argv[2]

if __name__ == "__main__":
    if not input.endswith(".xml"):
        input = input + ".xml"
    mapfile = input
    if not output.endswith(".png"):
        output = output + ".png"
    map_uri = output

    #---------------------------------------------------
    #  Change this to the bounding box you want
    #
    ll = (-6.5, 49.5, 2.1, 59)
    ll = (-124.1084, 40.8961, -124.0452, 40.8577) #Arcata extract
    #ll = (-122.933, 47.0634, -122.8697, 47.0272) #Olympa, WA
    ll = (-122.425984, 42.761381, -121.876216, 43.121094)
    #---------------------------------------------------

    z = 1
    imgx = 500 * z
    imgy = 1000 * z

    prj = mapnik.Projection("+proj=merc +a=6378137 +b=6378137 +lat_ts=0.0 +lon_0=0.0 +x_0=0.0 +y_0=0 +k=1.0 +units=m +nadgrids=@null +no_defs +over")
    
    #ll = (-124.049723023,40.8949830086,-124.047423336,40.8967213441)
    c0 = prj.forward(mapnik.Coord(ll[0],ll[1]))
    c1 = prj.forward(mapnik.Coord(ll[2],ll[3]))
    
    #zoom = 100
    #lat = 40.880894
    #lon = -124.092982

    #lat=40.86905
    #lon=-124.0869

    #prj = mapnik.Projection("+proj=merc +a=6378137 +b=6378137 +lat_ts=0.0 +lon_0=0.0 +x_0=0.0 +y_0=0 +k=1.0 +units=m +nadgrids=@null +no_defs +over")
    #cord = prj.forward(mapnik.Coord(lon, lat))
    #lower_left = mapnik.Coord(int(cord.x) - int(cord.x) % 256, int(cord.y) - int(cord.y) % 256)
    #upper_right = lower_left + mapnik.Coord(256,256)
    #imgx = 256
    #imgy = 256
    #c0 = lower_left
    #c1 = upper_right
    
    m = mapnik.Map(imgx,imgy)
    mapnik.load_map(m,mapfile)
    
    if hasattr(mapnik,'mapnik_version') and mapnik.mapnik_version() >= 800:
        bbox = mapnik.Box2d(c0.x,c0.y,c1.x,c1.y)
    else:
        bbox = mapnik.Envelope(c0.x,c0.y,c1.x,c1.y)
    m.zoom_to_box(bbox)
    im = mapnik.Image(imgx,imgy)
    mapnik.render(m, im)
    view = im.view(0,0,imgx,imgy) # x,y,width,height
    view.save(map_uri,'png')
