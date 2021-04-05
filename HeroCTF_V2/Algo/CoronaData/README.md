# CoronaData

### Catégorie

Algo

### Description

Vous êtes engagé sur un nouveau poste dans le big data. Vous devez analyser le fichier CSV ci-dessous. La réponse attendue est le nombre MAXIMUM de "cas_confirmes".

```
Exemple:
date, ville, dep, cas_confirmes
15/04/20, Rennes, 35, 50
15/04/20, Paris, 75, 100
15/04/20, Vannes, 56, 30

Réponse: 100 
Flag: Hero{100}
```

Format: Hero{nombre}

### Fichier

[corona.csv](corona.csv)

### Auteur

Enarior

### Solution

Petit script un peu moche avec le module csv.

```
$ python3 -m pip install csv
```

Script :

```import csv
cases2 = list()
with open('corona.csv', newline='') as csvfile:
    spamreader = csv.reader(csvfile, delimiter=' ', quotechar='|')
    for row in spamreader:
        cases=row[0].split(',')
        while ("" in cases):
            cases.remove("")
        try:
            cases2.append(cases[4])
        except:
            print("")
    i = 1
    new_list = list()
    while(i<len(cases2)):
        new_list.append(int(cases2[i]))
        i+=1
    new_list.sort()
    print(new_list[-1])
```

Solution :

```
$ python3 solver.py
591971
```

### Flag

Hero{591971}
