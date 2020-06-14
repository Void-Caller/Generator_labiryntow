class ToLargeError(ValueError):
    """Podnoszona, gdy labirynt jest za duży."""
    pass


class ToSmallError(ValueError):
    """Podnoszona, gdy labirynt jest za mały."""
    pass


class NotOnEdgeError(Exception):
    """Podnoszona, gdy entry lub exit nie znajduje się na krawędzi labiryntu"""


class ToCloseError(Exception):
    """Podnoszona, gdy wejście i wyjście są za blisko siebie."""
    pass
