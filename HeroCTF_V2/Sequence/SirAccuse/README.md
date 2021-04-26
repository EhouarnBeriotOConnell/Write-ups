# Sir accuse

### Catégorie

Sequence

### Description

Votre pote mathématicien se croit plus malin que vous. Prouvez-lui qu'il a tort en trouvant les 3 éléments complétant la suite suivante !

Suite : 17, 52, 26, 13, 40, 20, 10, 5, ..., ..., ...

Format : HeroCTF{x, y, z} avec x, y et z les 3 valeurs complétant la suite

Author : SoEasy

### Solution

Le titre du chall nous indique qu'il s'agit probablement de la suite de Syracuse.
 - Si le nombre est pair, on le divise par 2
 - Si le nombre est impair, on le multiplie par 3 et on rajoute 1.

Donc ici, 5 est impair, on multiplie par 3 et on rajoute 1: 5*3+1 =16
16 est pair, on divise par 2 : 16/2 = 8
8 est pair, on divise par 2 : 8/2 = 4

Les 3 nombres suivants sont donc 16, 8 et 4.


### Flag

HeroCTF{16, 8, 4}
