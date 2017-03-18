from Image import *

fn = str(input("File : "))

im = Image(fn)
im.show_image()

im.get_threshold()

#im.plot_maximums_difference()

#im.shift_image(0.)
im.show_image()

#im.clean_up(10)
#im.show_image()