Quelques précisions, en vrac, sur le sujet de Python avancé, au vu de questions reçues en
point à point mais qui peuvent profiter à tout le monde.

# signature d'une permutation

Il y a un truc qui s’appelle [la parité - ou signature - d'une
permutation](https://fr.wikipedia.org/wiki/Signature_d%27une_permutation) dont on pensait
qu'il était acquis à votre niveau, mais apparemment pas par toute la promotion. En deux
mots ça donne ceci :

Dans le monde des permutations, une 'transposition' c'est un simple échange de deux
valeurs

Et la signature d'une permutation, c'est un invariant qui est lié au nombre de
transpositions nécessaire pour fabriquer la permutation; du coup pour calculer si une
permutation est paire ou impaire, on peut compter le nombre d’échanges pour y
parvenir. Il n’y a bien sûr pas unicité, mais ce n’est pas important, la parité du nombre
de transpositions est bien un invariant

Et donc pour revenir au problème, il peut aussi être utile d'imaginer que le jeu de taquin
est peint en deux couleurs comme un damier...

# *priority queue*

L'énoncé n'est pas suffisamment clair sur l'usage des librairies; on parlait de demander une
autorisation pour utiliser une librairie mais cela s'applique uniquement aux librairies
qui nécessitent une installation séparée : **vous pouvez sans
réserve utiliser intégralement toute la librairie standard**

Notamment pour l'implémentation d'une *priority queue* il existe un module spécialisé
`heapq` dans la librairie standard, et son usage est totalement autorisé.

# les tests

Si certains tests ne fonctionnent qu'en local, pensez à vider votre cache:

```bash
rm samples/u*.chain samples/r*.chain
```

Imaginez:
* vous écrivez un code qui marche, vous le testez, ça produit des `.chain` corrects
* vous modifiez votre code, vous le cassez au point que les `.chain` ne sont pas récrits
* dans ce cas de figure les tests vont dire que c'est OK, alors qu'en fait votre code est très très cassé
* en nettoyant les `.chain` de votre répertoire `samples` vous éliminez ce faux positif

Sur github on repart toujours d'un dépôt vierge, et donc on n'a pas ce phénomène de faux
positifs

# les tests de performance

Si vous avez des problèmes de timeout que vous ne comprenez pas, exécutez les tests 1 par
1 en local, la durée d'exécution est marquée. Pour info pour chaque test on fait tourner
votre solver 10 fois, avec des configurations relativement dures.

# `numpy`

L'énoncé autorise l'utilisation de `numpy` mais dans le cas présent ce n'est pas forcément
une super idée...

# la vidéo

Certains d'entre vous ont remarqué qu'en suivant exactement le fil de la vidéo on n'obtenait pas le même résultat

En fait les échantillons dans `samples/` contiennent tous une ligne vide en trop à la fin du fichier; du coup pour obtenir le même comportement que dans la vidéo il faut utiliser le code suivant; remarquez le `input.read()[:-1]` qui enlève ce saut de ligne surnuméraire :

```python
import sys
source, dest = sys.argv[1:3]
with open(source) as input, open(dest, 'w') as output:
    content = input.read()[:-1]  # le -1 sert à enlever le dernier \n en trop
    output.write(content)
    output.write('---\n')
    output.write('{"reachable": false, "nb_moves": 0}\n')
```
