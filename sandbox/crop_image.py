from PIL import Image

image = Image.open("scripts/2.png")

x = 756.217_608_449_493_6
y = 456.338_142_498_715_06
width = 117.585_160_772_077_15
height = 64.169_112_625_045_43


box = (x, y, x + width, y + height)
cropped_image = image.crop(box)
