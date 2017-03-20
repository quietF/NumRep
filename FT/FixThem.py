from Image import *

#fn = str(input("File : "))
fn = "desync1.pgm"

im = Image(fn)

#im.show_image()

#im.get_threshold()

#im.plot_maximums_difference()

im.shift()
im.shift()

#im.shift_image(1.2)
im.show_image()

#im.clean_up(10)
#im.show_image()