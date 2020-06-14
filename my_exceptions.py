
class FormatError(Exception):
    """Podnoszona, gdy input ma zły format inputu."""
    pass

class ToLargeError(ValueError):
    """Podnoszona, gdy labirynt jest za duży."""
    pass

class ToSmallError(ValueError):
    """Podnoszona, gdy labirynt jest za mały."""
    pass

class ToCloseException(Exception):
    """Podnoszona, gdy wejście i wyjście są za blisko siebie."""
    pass