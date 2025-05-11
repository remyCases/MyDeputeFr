# Copyright (C) 2025 Rémy Cases
# See LICENSE file for extended copyright information.
# This file is part of MyDeputeFr project from https://github.com/remyCases/MyDeputeFr.

# ERROR
SCRUTIN_DEPUTE_NOT_FOUND_TITLE = "Député et scrutin non trouvé"
SCRUTIN_DEPUTE_NOT_FOUND_DESCRIPTION = "Je n'ai trouvé ni le député {full_name}, ni le scrutin {code_ref}."

CIRCO_DEPUTE_NOT_FOUND_DESCRIPTION = "Je n'ai pas trouvé de député dans le {code_dep}-{code_circo}."
DEPARTEMENT_DEPUTE_NOT_FOUND_DESCRIPTION = "Je n'ai pas trouvé de députés dans le département {code_dep}."

SCRUTIN_NOT_FOUND_TITLE = "Scrutin non trouvé"
SCRUTIN_NOT_FOUND_DESCRIPTION = "Je n'ai pas trouvé le scrutin {code_ref}."

DEPUTE_NOT_FOUND_TITLE = "Député non trouvé"
DEPUTE_NOT_FOUND_DESCRIPTION = "Je n'ai pas trouvé le député {full_name}."

# DEPUTE
DEPUTE_EMBED_TITLE = ":bust_in_silhouette: {first_name} {last_name}"
DEPUTE_EMBED_DESCRIPTION = (":round_pushpin: **Circoncription** : {dep}-{circo} ({dep_name})\n"
                            ":classical_building: **Groupe** : {gp}")

# DEPARTEMENT
DEPARTEMENT_TITLE = ":pushpin: Département {dep} ({dep_name})"
DEPARTEMENT_DEPUTE_DESCRIPTION = (":bust_in_silhouette: [{first_name} {last_name}]({url}) — "
                                  ":round_pushpin: **Circoncription** : {dep}-{circo} | "
                                  ":classical_building: **Groupe** : {gp}")

# SCRUTIN
SCRUTIN_EMBED_TITLE = ":ballot_box: Scrutin nº{ref}"
SCRUTIN_EMBED_DESCRIPTION = (":calendar: **Date**: {date_scrutin}\n"
                             ":page_with_curl: **Texte**: {text}\n"
                             ":bar_chart: **Résultat**: {result}\n ")

SCRUTIN_EMOJI_ADOPTE = ":green_circle:"
SCRUTIN_EMOJI_REJETE = ":red_circle:"

SCRUTIN_VALUE_ADOPTE = "Adopté"
SCRUTIN_VALUE_REJETE = "Rejeté"

SCRUTIN_PARTICIPATION_NAME = "Participations"
SCRUTIN_PARTICIPATION_VALUE = (":ballot_box: Nombre de votants: {nombreVotants}\n"
                               ":exclamation: Non votants: {nonVotant}\n"
                               ":no_entry_sign: Non votants volontaires: {nonVotantsVolontaire}")

SCRUTIN_RESULTS_NAME = "Résultats"
SCRUTIN_RESULTS_VALUE = (":green_circle: Pour: {pour}\n"
                         ":red_circle: Contre: {contre}\n"
                         ":white_circle: Abstentions: {abstention}")

# VOTE
VOTE_TITLE = "Vote"
VOTE_DESCRIPTION = (":bust_in_silhouette: **Député** : {depute_first_name} {depute_last_name}\n"
                    ":round_pushpin: **Circoncription** : {depute_dep}-{depute_circo} ({depute_dep_name})\n"
                    ":classical_building: **Groupe** : {depute_gp}\n"
                    ":bar_chart: **Position** : {position_name} {position_name_emoji} \n")

VOTE_EMOJI_POUR = ":green_circle:"
VOTE_EMOJI_CONTRE = ":red_circle:"
VOTE_EMOJI_NON_VOTANT = "exclamation:"
VOTE_EMOJI_ABSENT = ":orange_circle:"
VOTE_EMOJI_ABSTENTION = ":white_circle:"

VOTE_VALUE_POUR = "Pour"
VOTE_VALUE_CONTRE = "Contre"
VOTE_VALUE_ABSTENTION = "Abstention"
VOTE_VALUE_NON_VOTANT = "Non Votant"
VOTE_VALUE_ABSENT = "Absent"

# STAT
STATISTICS_FIELD_NAME = "Statistiques de vote"
