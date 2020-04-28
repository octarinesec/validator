class AttributeFilter():
    def __init__(self):
        self._exclude_attributes = []

    @property
    def exclude_attributes(self):
        return self._exclude_attributes

    @exclude_attributes.setter
    def exclude_attributes(self, value):
        if not value in self._exclude_attributes:
            self._exclude_attributes.append(value)

    def add_attribute(self, value):
        exclude_attributes(value)
