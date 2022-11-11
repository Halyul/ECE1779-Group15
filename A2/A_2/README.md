# Assigment 2

This is the source code for ECE1779 2022 Fall Assignment 2

## CLOC
```bash
$ cloc ./ --exclude-dir=__pycache__,.vscode,db,dist,node_modules,yarn.lock,uploads,public,pnpm-lock.yaml
      99 text files.
      88 unique files.                              
      18 files ignored.

github.com/AlDanial/cloc v 1.94  T=0.05 s (1666.1 files/s, 110096.9 lines/s)
-------------------------------------------------------------------------------
Language                     files          blank        comment           code
-------------------------------------------------------------------------------
Python                          46            383            291           1995
JSX                             17             68             47           1894
Markdown                         8             50              0            392
JavaScript                       4             14             18            269
HTML                             6             16              0            153
JSON                             2              0              0             57
SVG                              1             44              1             44
YAML                             2              6              1             44
Text                             1              0              0             20
CSS                              1              1              0              7
-------------------------------------------------------------------------------
SUM:                            88            582            358           4875
-------------------------------------------------------------------------------
```

## Flask

### Install Pipenv

```bash
$ pip install --user pipenv
```

### Install Environment

```bash
$ pipenv install
```

### Run

```bash
$ ../start.sh
```

## Frontend

### Install Dependencies

```bash
$ pnpm install
```

### Run Development Server

```bash
$ pnpm run dev
```

### Generate Static Files

```bash
$ pnpm run build
```
