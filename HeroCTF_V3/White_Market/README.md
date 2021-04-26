# White Market

### Catégorie

Programming

### Description

Welcome to the year 2080, you have just finished shopping and you set yourself a challenge.

A robot scans barcodes at a phenomenal speed, you tell yourself that with a little programming, you can beat it.

Calculate the price of your shopping before the robot does!

Challenge : nc chall0.heroctf.fr 7005

Format : Hero{}

Author : Worty

[market.txt](market.txt)


### Solution

We start by connecting to the challenge with netcat : nc chall0.heroctf.fr 7005
We receive the following message:
```
 Welcome to Hero's Market !
            I know what you want because I'm a super AI !

            I will scan barcodes for you and give you the total.

            If you want you can test me, and try to calculate the finale price before me !
    
Do you want to try?(y/n)
```

We answer yes(y), and we receive a big chunk of data that looks like this:

```
iVBORw0KGgoAAAANSUhEUgAAAgsAAAEYCAIAAABdlyIxAAAOLElEQVR4nO3caWyUZbvA8bt0E2WvoiJGgy[...]
```

And then the server sends us "Beeeeeeeeeeep too late! Your total is 5635$ !"

Data look like base 64, so we can try translating it into ascii:
https://base64.guru/converter/decode/ascii
A lot of it is not ascii, but we can see that it contains "PNG", so data is an image. Let's try to see what it looks like :
https://base64-to-image.com
So, it is a barcode image with an id on it. We can check in the market.txt file, the id is associated to a price.

Now we know what we have to do for each data chunk we receive: generate image from data, retreive id from it, get the corresponding price and send it back.
I will use Python with the pwn module to communicate with the server, base64 to translate base 64, PIL to handle images and pytesseract to retrieve id.

We have one more thing though: we have a time limit and writing an image+pytesseract is kinda slow.
So we will run the program a couple times first to store id corresponding to each b64 chunk. We will do it this way:

When receiving data:
if we already have id ==> just get the associated price
if not ==> Generate image, run pytesseract to retrieve id, store id, then get the associated price

This way, each time we run the program it will be faster, until we get enough/all ids and it gets fast enough.


### Script

```python
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

```


### Execution:
```
[x] Opening connection to chall0.heroctf.fr on port 7005
[x] Opening connection to chall0.heroctf.fr on port 7005: Trying 35.246.46.180
[+] Opening connection to chall0.heroctf.fr on port 7005: Done

            Welcome to Hero's Market !
            I know what you want because I'm a super AI !

            I will scan barcodes for you and give you the total.

            If you want you can test me, and try to calculate the finale price before me !
    
Do you want to try?(y/n)
Here is the barcode of the current article: [...base64...]

id already in database
3113929658096
[+]Sending 84    TOTAL : 84
Correct ! The price for plate is 84$ !

Here is the barcode of the current article: [...base64...]

id already in database
1194538623592
[+]Sending 73    TOTAL : 157
Correct ! The price for cake is 73$ !

[...]

Ooooh... It's a little embarrassing, you're done calculating before me.

[*] Switching to interactive mode
WELL DONE ! You deserve a reward, take it: Hero{u_4r3_b3tt3r_th4n_4_r0b0t_!!}
```

### TLDR

Global idea:
	
- use pwn to communicate.
- for each data chunk received: generate image, get id(pytesseract), send back price

Speed optimization:
I run the script a couple times to store id corresponding to each data, this way no need to generate image + run pytesseract every time.

When receiving data:
if we already have id ==> just get the associated price.

if not ==> Generate image, run pytesseract to retrieve id, store id, then get the associated price

### Links

pytesseract : https://pypi.org/project/pytesseract/

pwn: https://python3-pwntools.readthedocs.io/en/latest/about.html#module-pwn
