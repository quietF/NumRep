from Image import *


fn = str("img_in/" + input("Input image name: "))

im = Image(fn)

im.shift()

#im.clean_up()
im.show_image()
im.save_image()