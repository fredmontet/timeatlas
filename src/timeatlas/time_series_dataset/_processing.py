from typing import Any

from timeatlas.abstract.abstract_processing import AbstractProcessing


class Processing(AbstractProcessing):

    def resample(self, by: str) -> Any:
        """
        https://pandas.pydata.org/pandas-docs/stable/user_guide/timeseries.html#offset-aliases
        - upsampling
        - downsampling
        """
        pass

    def interpolate(self, method: str) -> Any:
        """
        "Intelligent" interpolation in function of the data unit etc.
        """
        pass

    def normalize(self, method: str) -> Any:
        """
        Normalize a dataset
        """
        pass

    def synchronize(self):
        """
        Synchronize the timestamps so that they are the same for all time
        series in the TimeSeriesDataset
        """
        pass

    def unify(self):
        """
        Put all time series in a matrix iff they all have the same length
        """
        pass
