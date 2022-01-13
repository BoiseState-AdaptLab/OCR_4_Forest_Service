#!/usr/bin/env python

from PIL import Image

black = 5

img = Image.open("fields/field_14.jpg")
pixels = img.load() # create the pixel map

  
y_coord = int(img.size[1])
# while ( y_coord >= (img.size[1] - 1) ):
for x in range(img.size[0]):
    for y in range(y_coord -2, y_coord):
        if pixels[x,y] <= (100, 130, 140):
            black += 1
            if black > 5:
                #img.putpixel((x,y),(255, 0, 0))
                img.putpixel((x,y), (152, 190, 162))
        else:
            black == 0
    # y_coord -= 1


img.show()
