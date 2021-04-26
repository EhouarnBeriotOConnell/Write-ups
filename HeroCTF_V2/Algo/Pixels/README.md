# Pixels

### Catégorie

Algo

### Description

Vous devez compter le nombre de pixels NON noir.

Format: Hero{nombre}

Author : xanhacks

### Fichier

[image.png](image.png)


### Solution

Un script avec le module pillow. ça pourrait se faire en une ligne, mais ~~je suis mauvais~~ c'est plus clair comme ça.

```python
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
```


Solution :

```
$ python3 solver.py
41229
```

### Flag

Hero{41229}
