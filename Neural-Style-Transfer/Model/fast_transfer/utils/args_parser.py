import argparse


parser = argparse.ArgumentParser()


parser.add_argument("content_image", help = "Relative path to the image to be styled" , type = str)
parser.add_argument("style_image", help = "Relative path to the image with the intended style" , type = str)
parser.add_argument("-v", "--verbose", help = "Verbose logging" , action = "store_true")
parser.add_argument("-d", "--debug", help = "Debug level logging" , action = "store_true")

