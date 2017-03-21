from Image import *

#fn = str(input("File : "))
fn = "desync2.pgm"

im = Image(fn)

#im.show_image()

#im.get_threshold()

#im.plot_maximums_difference()

im.shift()

#im.clean_up()
im.show_image()

#im.show_image()