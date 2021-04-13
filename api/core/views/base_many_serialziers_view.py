class ManySerialziersView:
    """View for get many serialzier."""

    serializer_class = None

    def get_serializer_class(self):
        """Get the serializer depending on the method we are going to use.
        Return:
            Class: serializer Classf
        """
        if self.serializer_class is None:
            raise NotImplementedError(
                'serializer_class is none, a dictionary has to be used'
            )
        if not isinstance(self.serializer_class, dict):
            raise AttributeError(
                f'A dictionary is expected not a {type(self.serializer_class)}'
            )
        return self.serializer_class.get(self.action)
