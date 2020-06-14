class TooLargeError(ValueError):
    """Podnoszona, gdy labirynt jest za duży."""
    pass


class TooSmallError(ValueError):
    """Podnoszona, gdy labirynt jest za mały."""
    pass


class NotOnEdgeError(Exception):
    """Podnoszona, gdy entry lub exit nie znajduje się na krawędzi labiryntu"""


class TooCloseError(Exception):
    """Podnoszona, gdy wejście i wyjście są za blisko siebie."""
    pass
