# Documentation des Commandes pour DeputeCommand

## Commandes Disponibles

### `debugd`

**Description :** Commande de débogage pour afficher toutes les informations de débogage concernant un député.

**Utilisation :**
```
/debugd <last_name>
/debugd <last_name> <first_name>
```


**Paramètres :**
- `last_name` (str) : Nom de famille du député.
- `first_name` (str) : Prénom de famille du député.

**Exemple :**
```
/debugd Panot Mathilde
/debugd Panot
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
/nom <last_name>
/nom <last_name> <first_name>
```

**Paramètres :**
- `last_name` (str) : Nom de famille du député.
- `first_name` (str) : Prénom de famille du député.

**Exemple :**
```
/nom Leaument Antoine
/nom Leaument
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
/vote <last_name> <code_ref>
/vote <last_name> <first_name> <code_ref>
```

**Paramètres :**
- `last_name` (str) : Nom de famille du député.
- `first_name` (str) : Prénom de famille du député.
- `code_ref` (str) : Code de référence du scrutin.

**Exemple :**
```
/vote Guiraud David 150
/vote Guiraud 150
```

### `stat`

**Description :** Affiche les statistiques de vote d'un député.

**Utilisation :**
```
/stat <last_name>
/stat <last_name> <first_name>
```

**Paramètres :**
- `last_name` (str) : Nom de famille du député.
- `first_name` (str) : Prénom de famille du député.


**Exemple :**
```
/stat Coquerel Éric
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