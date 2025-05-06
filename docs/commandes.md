# Documentation des Commandes pour DeputeCommand

## Commandes Disponibles

### `debugd`

**Description :** Commande de débogage pour afficher toutes les informations de débogage concernant un député.

**Utilisation :**

```discord
!debugd <last_name>
!debugd <last_name> <first_name>
```

**Paramètres :**

- `last_name` (str) : Nom de famille du député.
- `first_name` (str) : Prénom de famille du député.

**Exemple :**

```discord
!debugd Panot Mathilde
!debugd Panot
```

### `debugs`

**Description :** Commande de débogage pour afficher toutes les informations de débogage concernant un scrutin.

**Utilisation :**

```discord
!debugs <code_ref>
```

**Paramètres :**

- `code_ref` (str) : Code de référence du scrutin.

**Exemple :**

```discord
!debugs 3
```

### `debugn`

**Description :** Commande de débogage pour afficher les députés suivis par un utilisateur.

**Utilisation :**

```discord
!debugs <user_name>
```

**Paramètres :**

- `user_name` (discord.User) : Nom d'un utilisateur discord.

**Exemple :**

```discord
!debugn @zizabot
```

### `nom`

**Description :** Affiche les informations d'un député en fonction de son nom.

**Utilisation :**

```discord
!nom <last_name>
!nom <last_name> <first_name>
```

**Paramètres :**

- `last_name` (str) : Nom de famille du député.
- `first_name` (str) : Prénom de famille du député.

**Exemple :**

```discord
!nom Leaument Antoine
!nom Leaument
```

### `circo`

**Description :** Affiche les informations du député associé à une circonscription.

**Utilisation :**

```discord
!circo <code_dep> <code_circo>
```

**Paramètres :**

- `code_dep` (str) : Code du département.
- `code_circo` (str) : Code de la circonscription.

**Exemple :**

```discord
!circo 93 10
```

### `dep`

**Description :** Affiche la liste des députés dans un département.

**Utilisation :**

```discord
!dep <code_dep>
```

**Paramètres :**

- `code_dep` (str) : Code du département.

**Exemple :**

```discord
!dep 12
```

### `vote`

**Description :** Affiche le vote d'un député pour un scrutin donné.

**Utilisation :**

```discord
!vote <code_ref> <last_name>
!vote <code_ref> <last_name> <first_name>
```

**Paramètres :**

- `code_ref` (str) : Code de référence du scrutin.
- `last_name` (str) : Nom de famille du député.
- `first_name` (str) : Prénom de famille du député.

**Exemple :**

```discord
!vote 150 Guiraud David
!vote 150 Guiraud
```

### `stat`

**Description :** Affiche les statistiques de vote d'un député.

**Utilisation :**

```discord
!stat <last_name>
!stat <last_name> <first_name>
```

**Paramètres :**

- `last_name` (str) : Nom de famille du député.
- `first_name` (str) : Prénom de famille du député.

**Exemple :**

```discord
!stat Coquerel Éric
```

### `scr`

**Description :** Affiche les informations d'un scrutin en fonction de son code de référence.

**Utilisation :**

```discord
!scr <code_ref>
```

**Paramètres :**

- `code_ref` (str) : Code de référence du scrutin.

**Exemple :**

```discord
!scr 95
```

### `last`

**Description :** Affiche la date du dernier scrutin en date.

**Utilisation :**

```discord
!last
```

**Exemple :**

```discord
!last
```

### `sub`

**Description :** S'inscrit pour suivre les prochains votes d'un député.

**Utilisation :**

```discord
!sub <last_name>
!sub <last_name> <first_name>
```

**Paramètres :**

- `last_name` (str) : Nom de famille du député.
- `first_name` (str) : Prénom de famille du député.

**Exemple :**

```discord
!sub panot
```

### `unsub`

**Description :** Se désinscrit concernant les prochains votes d'un député.

**Utilisation :**

```discord
!unsub                          # pour se désincrire de tous les députés
!unsub <last_name>              # pour se désincrire d'un député en particulier
!unsub <last_name> <first_name> # pour se désincrire d'un député en particulier
```

**Paramètres :**

- `last_name` (str) : Nom de famille du député.
- `first_name` (str) : Prénom de famille du député.

**Exemple :**

```discord
!unsub panot
```

### `rcv`

**Description :** Affiche les votes de la dernière journée de scrutin des députés suivis.

**Utilisation :**

```discord
!rcv
```

**Exemple :**

```discord
!rcv
```

## Notes

- Les commandes `debugd`, `debugs` et `debugn` sont des commandes de débogage et seront potentiellement supprimées.
