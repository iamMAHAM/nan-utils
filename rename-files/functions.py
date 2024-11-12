from pathlib import Path
from typing import List, Union
import shutil
import re


def define_courses_path() -> str:
    """
    define the courses path
    """
    course = input('Entrer le chemin des cours : ')
    if (course == ''):
        print("veuillez entrer un chemin valide")
        return define_courses_path()
    return course


def get_folder_files(path: Union[str, Path]) -> List[Path]:
    """
    get the files in a folder
    """
    if (isinstance(path, str)):
        path = Path(path)
    return list(filter(lambda x: x.is_file(), path.iterdir()))


def scan_dirs(path: Union[str, Path], **kwargs: dict[str, str]) -> List[Path]:
    """
    get the courses Generator Path inside path
    """

    path = Path(path)
    courses = list(filter(lambda c: c.is_dir(), path.iterdir()))

    if (kwargs.get('keep_file', False)):
        courses = list(filter(lambda c: c.is_dir()
                       or c.is_file(), path.iterdir()))
    return courses


def copy_files(path: Union[str, Path], destination: Union[str, Path]) -> None:
    """
    copy files from path to destination
    """
    if (isinstance(path, str)):
        path = Path(path)
    if (isinstance(destination, str)):
        destination = Path(destination)
    shutil.copy(path, destination)


def sort_by_rank(strings: List[Path]) -> List[Path]:
    def key_func(string: Path):
        # Utiliser une expression régulière pour trouver le premier nombre au début de la chaîne
        match = re.search(r'\d+', string.stem)
        if match:
            # Si un nombre est trouvé, le convertir en entier et l'utiliser comme clé de tri
            return int(match.group())
        else:
            # Si aucun nombre n'est trouvé, utiliser une valeur élevée pour placer ces chaînes à la fin
            return float('inf')

    # Utiliser la fonction de clé personnalisée pour trier les chaînes
    sorted_strings = sorted(strings, key=key_func)
    return sorted_strings


def only_dirs(path: Union[str, Path]) -> List[Path]:
    """
    get only the directories in a path
    """
    if (isinstance(path, str)):
        path = Path(path)
    return list(filter(lambda c: c.is_dir(), path.iterdir()))
