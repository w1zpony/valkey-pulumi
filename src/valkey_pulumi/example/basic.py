def my_fn(data: str) -> int:
    """basic fn.

    Parameters
    ----------
    data
        The str object to process.

    Returns
    -------
    Some integer value.
    """
    print("my_fn called")
    return 0


class BasicClass:
    """A basic class.

    Parameters
    ----------
    data
        The str object to process.
    """

    my_attribute: str = "Some attribute."
    my_other_attribute: int = 0

    def __init__(self, data: str):
        print("Implement a class here.")

    def my_method(self, param: int) -> int:
        """A basic method.

        Parameters
        ----------
        param
            A parameter.

        Returns
        -------
        Some integer value.
        """
        print("my_method called")
        return 0
