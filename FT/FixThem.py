from Image import *

fn = str(input("Input image name: "))

while(os.path.isfile(fn) == False):

    fn = str("img_in/" + fn)
    try:
        im = Image(fn)
    except IOError:
        print("File does not exist.")
        fn = str(input("Input image name: "))


im = Image(fn)
im.shift()
#im.clean_up()
im.show_image()

ask_save = str(input("Want to save image? (y/n): "))

if(ask_save == "yes" or ask_save == "y"):

    im.save_image()