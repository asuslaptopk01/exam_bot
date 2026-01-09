from dataclasses import dataclass
from database.settings import CRUD


@dataclass
class User(CRUD):
    id : int = None
    name : str = None
    username : str = None
    phone_number : str = None

@dataclass
class Categories(CRUD):
    id : int = None
    name : str = None
    username : str = None
    phone_number : str = None

@dataclass
class Foods(CRUD):
    id : int = None
    category_id : int = None
    name : str = None
    photo : str = None
    description : str = None
    quantity : int = None
    price : float = None
    status : str = None