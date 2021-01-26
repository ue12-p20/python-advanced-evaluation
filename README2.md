---
jupytext:
  cell_metadata_filter: all,-hidden,-heading_collapsed,-run_control
  encoding: '# -*- coding: utf-8 -*-'
  notebook_metadata_filter: all,-language_info,-toc,-jupytext.text_representation.jupytext_version,-jupytext.text_representation.format_version
  text_representation:
    extension: .md
    format_name: myst
kernelspec:
  display_name: Python 3
  language: python
  name: python3
notebookname: imports et organisation du code
---

# rendus Python avancé - addendum

quelques ajouts/précisions par rapport à l'[énoncé original](https://github.com/ue12/python-advanced-evaluation)

## vidéo

Daniel Garnier-Moiroux vous montre en live [dans une
vidéo sur youtube](https://youtu.be/o2C4D_soTv0) l'utilisation de github classrooms pour le rendu

## spécifications

* on demande que le code dans `puzzle8/` soit composé de plusieurs fichiers; la présence
  de `cli.py` est imposée par l'énoncé, on vous impose de découper le code de façon à
  importer au moins une fois votre propre code; on pourrait imaginer par exemple un code
  qui serait découpé en trois fichiers `cli.py`, `board.py` et `solver.py`

## autograding

* les tests automatiques sont constitués de 10 tests; donc 1 point par test réussi

* parmi les 10 points de fonctionalité :
  * 2 points vérifient votre code pour les configurations impossibles (*unreachable*)
  * 4 points testent votre code sur des grilles de complexité croissante
  * 4 points sont attribués en fonction de la rapidité de votre code;  
    ça fonctionne comme ceci :
    * pour résoudre 10 configurations prises au hasard dans la classe des
    configurations 'dures',
    * on se donne un délai qui décroit: 30s, 25s, 20s, 15s;
    si vous résolvez les configurations dans ce délai, vous avez un point.


## `pytest`

pour utiliser `pytest` lorsque vous lancez les tests localement, voyez la documentation
de `pytest` et notamment
  * `pytest --collect-only` (ou juste `--co`)

    pour afficher la liste des tests disponibles

  *  `pytest -v`

     pour avoir plus de détails - par exemple voir le nom des tests au fur et à mesure
  *  `pytest --capture=sys`

     pour voir les messages affichés par `print()`(qui sinon sont
     attrapés/cachés par `pytest`)
  *  `pytest puzzle8/tests/test_all.py::test_unreachable_0`

     pour ne lancer qu'un seul test

  * `pytest -k unreach`

     pour n'exécuter que les tests dont le nom contient `unreach`


 ([voir aussi ceci pour plus de détails](https://docs.pytest.org/en/reorganize-docs/new-docs/user/commandlineuseful.html))
