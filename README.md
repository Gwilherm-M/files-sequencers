# Fichiers Sequenceurs

Offre à l'utilisateur la possibilité d'explorer le contenu d'un dossier en concaténant visuellement toutes les versions d'un même nom de fichier entre eux.

## Example:

En entrée:

```shell
> ls
    alpha.txt
    file01_0040.rgb
    file01_0041.rgb
    file01_0042.rgb
    file01_0043.rgb
    file02_0044.rgb
    file02_0045.rgb
    file02_0046.rgb
    file02_0047.rgb
    file1.03.rgb
    file2.03.rgb
    file3.03.rgb
    file4.03.rgb
    file.info.03.rgb
```

En sortie:

```python
[
    (1, "alpha.txt", ""),
    (4, "file01_%04d.rgb", "40-43"),
    (4, "file02_%04d.rgb", "44-47"),
    (4, "file%d.03.rgb", "1-4"),
    (1, "file.info.03.rgb", ""),
]
```


## Quick Install

Un fichier Makefile est disponible, mais utilisable uniquement sur **Windows**.

| Command | Description |
|---------| ----------- |
| `make install` | Installe un environement python 3 et touts les modules. |
| `make tests` | Execute les tests unitaires. |
| `make build` | Génère un executable dans le dossier bin. |

## Usage

| Command | Description |
|---------| ----------- |
| `-p` ou `--path` | Si aucun path n'est rentré (ou ".") le path courent est automatiquement choisi. |
| `-h` ou `--help` | Visualiser l'aide des commands. |
