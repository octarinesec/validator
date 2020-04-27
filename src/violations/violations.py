class Violations():

    @property
    def exclude_fields(self):
        return self._exclude_fields

    @exclude_fields.setter
    def exclude_fields(self, value):
        if not value in self._exclude_fields:
            self._exclude_fields.append(value)
