class RenderException(Exception):
    """
    Error while rendering menu
    """

    def __init__(self, message: str):
        super().__init__(message)
