class InstanceError(Exception):
    def __init__(self, problems):
        """
        :param problems: The list of problems encountered which led to the exception raise
        """
        self._errors_list = problems

    @property
    def list(self):
        return self._errors_list
