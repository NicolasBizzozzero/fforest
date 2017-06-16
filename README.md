# ensemble_experimentation
## TODO
* Immediatement transformer un nom de classe en index des le nettoyage des arguments. Ensuite, on pourra se dispenser du header pour Salammbo. Enregistrer ce header dans le main directory, passer en parametre l'extension du fichier de header, avec par défaut : "header"
* Implement the 'guess' option for the parameter --keep-header with the help of this code snippet : https://docs.python.org/3/library/csv.html#csv.Sniffer.has_header
* Add a verbose and silent option
* Add multiple progress bar
* Quote every parameters of all instances to protect them, with : csv.QUOTE_MINIMAL, csv.QUOTE_ALL, csv.QUOTE_NONNUMERIC
