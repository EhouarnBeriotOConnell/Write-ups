from pwn import remote
import base64
import pytesseract
from PIL import Image, ImageOps
import os

prices = {}
ids = {}
total = 0
with open("market.txt") as market:
    lines = market.read().split("\n")[:-1]
    for line in lines:
        code,article,price = line.split(":")
        prices[code] = (article, int(price))
with open("ids.txt") as idsFile:
    lines = idsFile.read().split("\n")[:-1]
    for line in lines:
        imgstring, id = line.split(":")
        ids[imgstring] = id

def generate_barcode_image(imgstring):
    data = base64.b64decode(imgstring)
    image = 'barcode.png'
    with open(image, 'wb') as f:
        f.write(data)

def get_id_from_image(path):
    image = Image.open(path).convert('RGB')
    image = ImageOps.autocontrast(image)

    filename = "{}.png".format(os.getpid())
    image.save(filename)

    text = pytesseract.image_to_string(Image.open(filename))
    return text

def write_id(imgstring, id):
    with open("ids.txt", 'a') as ids:
        ids.write(f"{imgstring}:{id}\n")

r = remote("chall0.heroctf.fr", 7005)

payload = r.recvuntil("Do you want to try?(y/n)")
print(payload.decode())
r.sendline("y")

while(True):
    payload = r.recvline()
    print(payload.decode())

    if ("embarrassing") in payload.decode():
        r.interactive()

    imagestring = (str(payload).split(": ")[1][:-5])    #retirer \b\r

    if imagestring in list(ids.keys()): #No need to generate image, we already have id for that image
        id = ids[imagestring]
        print("id already in database")
    else:
        generate_barcode_image(imagestring)
        id = get_id_from_image("barcode.png")[:-2]
        ids[imagestring] = id
        write_id(imagestring, id)

    print(id)
    price = prices[id][1]
    total += price
    r.sendline(str(price))
    print(f"[+]Sending {price}    TOTAL : {total}")
    line = r.recvline()
    print(line.decode())

r.close()
