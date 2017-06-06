from ensemble_experimentation.src.arg_parser import parse_args
from ensemble_experimentation.src import pretraitement
import ensemble_experimentation.src.get_default_value as gdv
import sys


def _check_add_id(args: dict) -> bool:
    """ Vérifie si l'utilisateur a spécifiquement demandé d'utiliser le nom de
    classe '_ID' comme identificateur d'exemples.
    Si oui, alors il ne faut pas le remplacer dans la BDD. Sinon c'est que
    docopt l'a ajouté par défaut, on doit alors l'ajouter.
    """
    id_name = gdv.id()
    if args["--id"] == id_name:
        # On regarde si l'option --id a été utilisée
        for option in sys.argv:
            if len(option) > 4 and option[:4] == "--id":
                # L'utilisateur a donc demandé l'identificateur "_ID"
                return False
        return True
    return False


def _load_database(filepath: str, format, encoding: str):
    pass


def main_ensemble_experimentation():
    print("Hello main_ensemble_experimentation")
    args = parse_args()

    if _check_add_id(args):
        # On doit ajouter une colonne d'identification
        args["--id"] = None

    database = _load_database(args["filepath"], args["format"],
                              args["encoding"])
    pretraitement(database)


def main_ensemble_foret_classique():
    print("Hello main_ensemble_foret_classique")
    pass


def main_ensemble_foret_reduction():
    print("Hello main_ensemble_foret_reduction")
    pass


if __name__ == "__main__":
    pass
