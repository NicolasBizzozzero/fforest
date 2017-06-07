def _ajout_id(database, id: str):
    """ Ajoute dans la database un identificateur unique pour chaque exemple.
    Il aura pour nom de classe 'id'.
    """
    pass


def pretraitement(*, database, id: str):
    if not id:
        # On doit ajouter une colonne d'identification
        _ajout_id(database, "_ID")


if __name__ == '__main__':
    pass
