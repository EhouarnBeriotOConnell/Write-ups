from PIL import Image
img = Image.open("image.png")
width, height = img.size
count = 0
for i in range(0,width):
    for j in range(0,height):
        pix=img.getpixel((i,j))
        if pix != (0,0,0):
            count += 1

print(count)
