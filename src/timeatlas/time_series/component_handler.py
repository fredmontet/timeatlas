from typing import List, Union
from copy import deepcopy, copy

import pandas as pd

from .component import Component
from timeatlas.config.constants import TIME_SERIES_VALUES


class ComponentHandler:

    def __init__(self, components: Union[List[Component], Component] = None):
        if isinstance(components, Component):
            components = list(components)
        self.components = components if components is not None else []

    def __getitem__(self, item):
        return ComponentHandler(self.components[item])

    def append(self, component: Component):
        self.components.append(component)

    def get_component_columns(self, i):
        cols = []
        print(self.components)
        for k, v in self.components[i].items():
            col_name = self.__format_value_str(i, v) \
                if k == TIME_SERIES_VALUES \
                else self.__format_meta_str(i, v)
            cols.append(col_name)
        return cols

    def get_columns(self):
        cols = []
        for i, c in enumerate(self.components):
            cols += self.get_component_columns(i)
        return pd.Index(cols)

    def get_values(self):
        values = []
        for i, c in enumerate(self.components):
            values.append(self.__format_value_str(i, c[TIME_SERIES_VALUES]))
        return values

    def copy(self, deep=False) -> 'ComponentHandler':
        return deepcopy(self) if deep else copy(self)

    @staticmethod
    def __format_value_str(index, value):
        return f"{index}_{value}"

    @staticmethod
    def __format_meta_str(index, value):
        return f"{index}-{value}"
