# le jeu de taquin

on se propose d'écrire un *solver* pour le jeu de taquin - connu en anglais sous le nom de
*8-puzzle*

## règle du jeu

peut-être y avez-vous joué dans votre enfance, il s'agit d'un jeu où les pièces couvrent
presque toute la surface du jeu, sauf pour un unique trou, dans lequel on peut faire
glisser une des pièces voisines

ainsi une séquence possible pour le jeu est représentée ci-dessous

```
 1 2 3        1 2 3        1 2 3        1 2 3        1 2 3
 4 8 5   =>   4 8 5   =>   4 - 5   =>   4 5 -   =>   4 5 6
 7 6 -        7 - 6        7 8 6        7 8 6        7 8 -

départ                                                but
```

## conventions

dans la suite on représente le trou indifféremment, selon les cas, par `-` ou `.` ou `0`.

la position d'arrivée est celle montrée sur l'exemple ci-dessus, c'est-à-dire

```
BINGO!

1 2 3
4 5 6
7 8 .
```

## comment s'y prendre

pour résoudre le puzzle, vous avez le choix de la méthode; une technique communément
utilisée - mais pas la seule - est connue sous le nom de ***A**** :

### l'algorithme ***A****

on définit un 'état' du jeu comme la juxtaposition de
* la configuration du jeu,
* le nombre de mouvements pour en arriver là,
* la configuration précédente;

on va ranger des états dans une 'queue'; elle est initialisée avec l'état de départ
(nombre de mouvements = 0, configuration précédente = aucune)

on répète ensuite ceci :
1. prendre dans la queue le - ou un - état qui a la priorité la plus faible
1. s'il s'agit de la configuration cible c'est terminé
1. sinon, l'enlever de la queue
1. et ajouter dans la queue tous les états accessibles (en un coup) à partir de cet état

### les priorités

on peut définir de plusieurs façons la priorité utilisée pour orienter l'algorithme dans
l'espace des états; en voici deux classiques

#### priorité de Hamming

le nombre de tuiles qui ne sont pas à leur place, plus le nombre de mouvements pour en
arriver là

```
entre      et

8 1 4    1 2 3      1 2 3 4 5 6 7 8 0
7 5 6    4 5 6      -----------------      hamming = 7
2 0 3    7 8 0      1 1 1 1 0 0 1 1 1
```

#### priorité de Manhattan

la somme des distances (la somme des distances horizontale et verticale) entre chaque
tuile et sa position cible, plus, ici encore, le nombre de mouvements pour en arriver là

```
entre      et

8 1 4    1 2 3      1 2 3 4 5 6 7 8 0
7 5 6    4 5 6      -----------------      hamming = 14
2 0 3    7 8 0      1 3 2 3 0 0 1 3 1
```

### anti-loop

si vous choisissez d'adopter l'algorithme ***A****, vous remarquerez que rien n'empêche
d'ajouter dans la queue les configurations sur lesquelles on est déjà passé

c'est pourquoi on recommande d'envisager une optimisation selon laquelle on ne remet pas
dans la queue un état qui créerait un demi-tour, c'est-à-dire par exemple

```
  8  1  3      8  1  3     8  1  3
  4  2  5      4  2  -     4  2  5
  7  6  -      7  6  5     7  6  -

 précédent      état       ignorer
```

## solvabilité

il est très important de réaliser que toutes les configurations ne sont pas atteignables

surtout si vous utilisez un algorithme un peu rustique, comme celui qui est suggéré ici
(et qui, à nouveau n'est pas le seul et pas forcément le meilleur); en effet cet
algorithme va mettre **très longtemps** à ne pas arriver à résoudre un problème insoluble

du coup vous êtes invités à caractériser les configurations qui sont atteignables, et à
implémenter un code qui détermine si une configuration est atteignable/solvable

**indice** parmi les 9! configurations possibles, la moitié d'entre elles sont
atteignables

## ce qu'il faut faire exactement

### fonctionnement

* le point d'entrée doit se trouver dans `puzzle/solver.py`
* on doit pouvoir l'invoquer en lui passant en argument deux noms de fichiers
  * le premier, lu par votre programme, et qui contient une configuration cible (au format
    textuel simple qu'on a utilisé jusqu'ici, dans lequel le trou est matérialisé par `0` ou `-` ou `.`)
  * le second, écrit par votre programme, contient le résultat

  voyez par exemple le fichier fourni `puzzle/tests/simple.txt`

  on doit pouvoir invoquer votre programme comme ceci

  ```shell
  $ python puzzle/solver.py puzzle/tests/simple.txt puzzle/tests/simple-chain.txt
  ```

  ce qui doit avoir pour effet de créer ou d'écraser le second fichier avec votre
  résultat

### format de sortie

selon les cas :

* si la configuration de départ est atteignable, vous devez produire quelque chose comme
  ceci, avec les étapes pour passer de la configuration de départ (qui apparait en
  premier) à la configuration cible, qui doit apparaitre en dernier; voyez un exemple 
  dans `puzzle/tests/simple-chain.txt`

```
1 2 3
4 8 5
7 6 -

1 2 3
4 8 5
7 - 6

1 2 3
4 - 5
7 8 6

1 2 3
4 5 -
7 8 6

1 2 3
4 5 6
7 8 -
```

* si la configuration n'est pas atteignable, votre fichier de sortie devra ressembler 
à ceci :

```
1 2 3
4 5 6
8 7 -
unreachable
```

## barême

on s'efforcera de produire un code qui puisse être facilement réutilisable
dans d'autres contextes

la note est sur 20

* **fonctionnalité**: 10 points sont donnés lorsque votre programme passe tous les tests
  (voir modalités)
* **lisibilité** 5 points sont donnés sur des critères de lisibilité et de présentation du
  code, et notamment
  * le respect de la norme de présentation pep008
  * la présence de docstrings pour les classes, principales méthodes, et fonctions
  * la présence de commentaires aux endroits épineux
  * le choix des noms de variables, fonctions et classes
* **conception** et enfin 5 points sont donnés sur les choix de conception, c'est-à-dire
  * le bon usage des concepts du langage - notamment en ce qui concerne les classes et
  fonctions, et les différents types de base à votre disposition (y compris les tableaux
  numpy)
  * et de la réutilisabilité qui en découle;

## modalités

les rendus se font sur github au travers de github classrooms;
ce qui procure plusieurs avantages

* la notation concernant les 10 points de fonctionnalité est automatique, et vous pouvez
  exécuter de votre coté ces tests pour savoir combien vous allez obtenir;
* le professeur qui corrige pourra annoter votre copie pour vous faire un retour sur votre
  code
