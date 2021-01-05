# le jeu de taquin

on se propose d'écrire un *solver* pour le jeu de taquin - connu en anglais sous le nom de
*8-puzzle*

## règle du jeu

peut-être y avez-vous joué dans votre enfance, il s'agit d'un jeu où les pièces couvrent
presque toute la surface du jeu, sauf pour un unique trou, dans lequel on peut faire
glisser une des pièces voisines

ainsi une séquence possible pour le jeu est représentée ci-dessous

```console
 1 2 3        1 2 3        1 2 3        1 2 3        1 2 3
 4 8 5   =>   4 8 5   =>   4 - 5   =>   4 5 -   =>   4 5 6
 7 6 -        7 - 6        7 8 6        7 8 6        7 8 -

départ                                                but
```

### vocabulaire et conventions

* on appellera *board* une configuration du jeu

* dans la suite on représente le trou indifféremment, selon les cas, par `-` ou `.` ou
  `0`.

* la position d'arrivée est celle montrée sur l'exemple ci-dessus, c'est-à-dire

```console
the target board is

1 2 3
4 5 6
7 8 .
```

* on appelle *solver* un algorithme permettant de trouver la chaine de coups
  permettant de résoudre le puzzle pour un *board*, c'est-à-dire permettant de
  reconstituer le *board* cible

## comment s'y prendre

pour résoudre le puzzle, vous avez le choix de la méthode; une technique communément
utilisée - mais pas la seule - est connue sous le nom de ***A**** :

### l'algorithme ***A****

on définit un 'état' du jeu comme la juxtaposition de

* un *board*,
* le nombre de mouvements pour en arriver là,
* la configuration précédente;

on va ranger des états dans une *priority queue*; elle est initialisée avec l'état de
départ (nombre de mouvements = 0, configuration précédente = aucune)

on répète ensuite ceci :

1. prendre dans la queue le - ou un - état qui a la priorité la plus faible
1. s'il s'agit de la configuration cible, c'est terminé
1. sinon, l'enlever de la queue
1. et ajouter dans la queue tous les états accessibles (en un coup) à partir de cet état

### les priorités

on peut définir de plusieurs façons la priorité utilisée pour orienter l'algorithme dans
l'espace des états; en voici deux classiques

dans les deux cas :

* on définit d'abord une **distance** entre les *boards*,
* et on définit la priorité comme étant la somme
  * de la distance entre le *board* voisin et la configuration cible,
  * et du nombre de coups qu'il a fallu pour en arriver à l'état courant

#### distance de Hamming

la distance de Hamming correspond au nombre de tuiles qui ne sont pas à leur place

```console
entre      et

8 1 4    1 2 3      1 2 3 4 5 6 7 8 0
7 5 6    4 5 6      -----------------      hamming = 7
2 0 3    7 8 0      1 1 1 1 0 0 1 1 1
```

#### distance de Manhattan

la distance de Manhattan est définie comme la somme des distances (la somme des distances
horizontale et verticale) entre chaque tuile et sa position cible

```console
entre      et

8 1 4    1 2 3      1 2 3 4 5 6 7 8 0
7 5 6    4 5 6      -----------------      manhattan = 14
2 0 3    7 8 0      1 3 2 3 0 0 1 3 1
```

### anti-loop

si vous choisissez d'adopter l'algorithme ***A****, vous remarquerez que rien n'empêche
d'ajouter dans la queue les configurations sur lesquelles on est déjà passé

c'est pourquoi on recommande d'envisager une optimisation selon laquelle on ne remet pas
dans la queue un état qui créerait un demi-tour, c'est-à-dire par exemple

```console
  8  1  3      8  1  3     8  1  3
  4  2  5      4  2  -     4  2  5
  7  6  -      7  6  5     7  6  -

 précédent      état       ignorer
```

## solvabilité

il est très important de réaliser que toutes les configurations ne sont pas atteignables

surtout si vous utilisez un algorithme un peu rustique, comme celui qui est suggéré ici
(et qui, à nouveau n'est pas le seul et pas forcément le meilleur); en effet cet
algorithme va mettre **très longtemps** à ne **pas arriver** à résoudre un problème
insoluble

du coup vous êtes invités à caractériser les configurations qui sont atteignables, et à
implémenter un code qui détermine si une configuration est atteignable/solvable

**indice** parmi les 9! configurations possibles, la moitié d'entre elles sont
atteignables

## ce qu'il faut faire exactement

### fonctionnement

* le point d'entrée doit se trouver dans `puzzle8/cli.py`
* on doit pouvoir l'invoquer en lui passant en argument deux noms de fichiers
  * le premier, lu par votre programme, et qui contient une configuration cible (au format
    textuel simple qu'on a utilisé jusqu'ici, dans lequel le trou est matérialisé par `0`
    ou `-` ou `.`)
  * le second, écrit par votre programme, contient le résultat (voir plus bas)

  voyez par exemple le fichier fourni `simple/simple.txt`

  on doit pouvoir invoquer votre programme comme ceci

  ```shell
  python puzzle8/cli.py samples/simple.txt samples/simple.chain
  ```

  ce qui doit avoir pour effet de créer ou d'écraser le second fichier avec votre
  résultat

### format de sortie

selon les cas :

* si la configuration de départ est atteignable, vous devez produire quelque chose comme
  ceci, avec les étapes pour passer de la configuration de départ (qui apparait en
  premier) à la configuration cible, qui doit apparaitre en dernier; cet exemple
  est dans `samples/simple.chain`

```console
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
---
{"reachable": true, "iterations": 5, "duration": 0.00013780593872070312, "priority": "manhattan", "nb_moves": 4}
```

* si la configuration n'est pas atteignable, votre fichier de sortie devra ressembler
à ceci; cet exemple est dans `samples/unreachable.chain` :

```console
2 1 3
4 8 5
7 6 -
---
{"reachable": false, "iterations": 0, "duration": 6.9141387939453125e-06, "priority": "manhattan", "nb_moves": 0}
```

### ligne de synthèse

comme vous le voyez dans les deux cas le fichier doit se terminer par une ligne qui
contient, exposé au format JSON, un dictionnaire

ce qui est requis (et vérifié par les tests automatiques), ce sont :

* la clé `reachable` qui indique si la configuration est atteignable ou pas
* la clé `nb_moves` qui donne le nombre de mouvements dans la chaine solution

vous pouvez, comme dans l'exemple, ajouter d'autres clés à ce dictionnaire, si vous êtes
par exemple intéressés à faire des statistiques sur la performance de votre algorithme

### performances

toutes les configurations de départ ne présentent pas, bien sûr, la même complexité, mais
dans le cas le pire votre algorithme ne doit **pas mettre plus de 5 secondes** pour
converger vers une réponse; ce point est pris en compte par les tests automatiques

de la même façon on impose que toutes les solutions se composent de **moins de 36 coups**
pour reconstituer la grille de départ (`nb_moves <= 36`)

## barême

on s'efforcera de produire un code qui puisse être facilement réutilisable
dans d'autres contextes

### la note est sur 20

* *fonctionnalité*: **10 points** sont donnés au prorata des tests qui passent avec succès
* *lisibilité* **5 points** sont donnés sur des critères de lisibilité et de présentation du
  code, et notamment
  * le respect de la norme de présentation pep008
  * la présence de docstrings pour les classes, principales méthodes, et fonctions
  * la présence de commentaires aux endroits épineux
  * le choix des noms de variables, fonctions et classes
* *conception* et enfin **5 points** sont donnés sur les choix de conception, c'est-à-dire
  * le bon usage des concepts du langage - notamment en ce qui concerne les classes et
  fonctions, et les différents types de base à votre disposition (y compris les tableaux
  numpy)
  * et de la réutilisabilité qui en découle;

### bonus

vous êtes encouragés à rédiger un court document (1 à 2 pages max) intitulé `FEEDBACK.md`
dans lequel vous partagez les points qui vous semblent intéressants dans la démarche que
vous avez adoptée, en abordant par exemple :

* les voies que vous avez suivies et qui n'ont pas débouché
* les autres voies que vous auriez pu suivre
* une preuve de votre critère de solvabilité
* une appréciation critique sur les priorités utilisées
* ce qui dans votre code est essentiel et ce qui est accessoire
* une estimation du comportement de votre algorithme en moyenne, en termes par exemple de
  rapidité, de complexité, des éventuelles bonnes propriétés - ou pas - de la solution trouvée,

ou de manière générale toute réflexion un peu critique sur cet exercice

un bonus de jusqu'à 3 points pourra être attribué en regard de cette partie optionnelle

## modalités

### date du rendu

les copies seront récoltées le **dimanche 31 janvier**

### discourse

ce n'est pas parce qu'il s'agit d'une évaluation que vous ne pouvez pas utiliser discourse
pour poser des questions sur le sujet, si certains points ne sont pas clairs ou si vous
rencontrez des difficultés de mise en oeuvre; n'hésitez pas à le faire, en prenant soin
simplement de ne pas spoiler le sujet

### github classrooms

les rendus se feront au travers de github classrooms - que certains d'entre vous ont déjà
eu l'occasion d'expérimenter - ce qui procure plusieurs avantages

* la notation concernant les 10 points de fonctionnalité est automatique (les tests sont
  relancés à chacun de vos commits)
* vous pouvez exécuter de votre coté ces tests pour savoir combien vous allez obtenir
  (les détails seront fournis avec le dépôt de rendu)
* enfin vous pourrez avoir accès au code annoté par le professeur qui corrige

dans l'immédiat, nous sommes en train de finaliser ce mode de rendu, nous vous fournirons
ultérieurement l'URL et les détails pratiques, et notamment les instructions pour lancer
les tests localement sur votre ordinateur; ce qui ne vous empêche pas de commencer à y
travailler dès à présent.

### divers

* on vous demande de fournir un code original, entièrement écrit par vous; vous avez le
  droit de consulter Internet pour vous renseigner sur **les concepts** ou les résultats
  généraux (solvabilité; caractéristiques de l'espace des solutions comme le diamètre du
  graphe; etc..), mais vous n'êtes pas autorisés par contre à **recopier du code**
* pensez à évaluer les mérites respectifs des deux distances
* vous pouvez utiliser la librairie numpy si vous le jugez utile, mais si vous voulez
  utiliser une autre librairie, demandez l'autorisation de le faire
