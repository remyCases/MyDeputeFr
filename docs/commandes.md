# Documentation des Commandes pour DeputeCommand

## Commandes Disponibles

### `debugd`

**Description :** Commande de débogage pour afficher toutes les informations de débogage concernant un député.

**Utilisation :**
```
/debugd <name>
```

**Paramètres :**
- `name` (str) : Nom du député.

**Exemple :**
```
/debugd Mathilde Panot
```

### `debugs`

**Description :** Commande de débogage pour afficher toutes les informations de débogage concernant un scrutin.

**Utilisation :**
```
/debugs <code_ref>
```

**Paramètres :**
- `code_ref` (str) : Code de référence du scrutin.

**Exemple :**
```
/debugs 3
```

### `nom`

**Description :** Affiche les informations d'un député en fonction de son nom.

**Utilisation :**
```
/nom <name>
```

**Paramètres :**
- `name` (str) : Nom du député.

**Exemple :**
```
/nom Antoine Leaument
```

### `circo`

**Description :** Affiche les informations du député associé à une circonscription.

**Utilisation :**
```
/circo <code_dep> <code_circo>
```

**Paramètres :**
- `code_dep` (str) : Code du département.
- `code_circo` (str) : Code de la circonscription.

**Exemple :**
```
/circo 93 10
```

### `dep`

**Description :** Affiche la liste des députés dans un département.

**Utilisation :**
```
/dep <code_dep>
```

**Paramètres :**
- `code_dep` (str) : Code du département.

**Exemple :**
```
/dep 12
```

### `vote`

**Description :** Affiche le vote d'un député pour un scrutin donné.

**Utilisation :**
```
/vote <name> <code_ref>
```

**Paramètres :**
- `name` (str) : Nom du député.
- `code_ref` (str) : Code de référence du scrutin.

**Exemple :**
```
/vote David Guiraud 150
```

### `stat`

**Description :** Affiche les statistiques de vote d'un député.

**Utilisation :**
```
/stat <name>
```

**Paramètres :**
- `name` (str) : Nom du député.

**Exemple :**
```
/stat Éric Coquerel
```

### `scr`

**Description :** Affiche les informations d'un scrutin en fonction de son code de référence.

**Utilisation :**
```
/scr <code_ref>
```

**Paramètres :**
- `code_ref` (str) : Code de référence du scrutin.

**Exemple :**
```
/scr 95
```

## Notes

- Les commandes `debugd` et `debugs` sont des commandes de débogage et seront potentiellement supprimées.