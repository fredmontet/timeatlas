from unittest import TestCase
import os

from pandas import DataFrame

import timeatlas as ta
from timeatlas import TimeSeries, Metadata, TimeSeriesDataset
from timeatlas.utils import ensure_dir
from timeatlas.config.constants import COMPONENT_VALUES


class TestReadWrite(TestCase):

    def setUp(self) -> None:
        self.root = os.path.dirname(os.path.abspath(__file__))
        self.target_dir = self.root + "/../data/test-import"

    def test__ReadWrite__read_text_without_metadata(self):
        wo = "{}/{}".format(self.target_dir, "to_text_without_metadata")
        ts = ta.read_text(wo)
        self.assertIsNone(ts.metadata)
        self.assertIsInstance(ts._data, DataFrame)
        self.assertIsInstance(ts, TimeSeries)

    def test__ReadWrite__read_text_with_metadata(self):
        w = "{}/{}".format(self.target_dir, "to_text_with_metadata")
        ts = ta.read_text(w)
        self.assertIsInstance(ts.metadata, Metadata)
        self.assertIsInstance(ts._data, DataFrame)
        self.assertIsInstance(ts, TimeSeries)

    def test__ReadWrite__read_tsd_without_metadata(self):
        wo = "{}/{}".format(self.target_dir, "read_tsd_without_metadata")

        # setup data
        ts_wo = TimeSeries.create("01-01-1990", "01-03-1990", "1D")
        ts_wo._data[COMPONENT_VALUES] = [0, 1, 2]
        tsd_wo = TimeSeriesDataset([ts_wo, ts_wo, ts_wo])
        tsd_wo.to_text(wo)

        # load data
        tsd = ta.read_tsd(wo)

        # test that all TS both TSDs are equal
        check = True
        for i, ts in enumerate(tsd):
            check &= ts._data.equals(tsd_wo[i]._data)

        # assertions
        self.assertTrue(check)
        self.assertIsInstance(tsd, TimeSeriesDataset)

    def test__ReadWrite__read_tsd_with_metadata(self):
        w = "{}/{}".format(self.target_dir, "read_tsd_with_metadata")

        # setup data
        ts_w = TimeSeries.create("01-01-1990", "01-03-1990", "1D")
        ts_w._data[COMPONENT_VALUES] = [0, 1, 2]
        ts_w._data["label_test"] = [0, None, 2]
        tsd_w = TimeSeriesDataset([ts_w, ts_w, ts_w])
        tsd_w.to_text(w)

        # load data
        tsd = ta.read_tsd(w)

        # test that all TS both TSDs are equal
        check = True
        for i, ts in enumerate(tsd):
            check &= ts._data.equals(tsd_w[i]._data)
            check &= (ts.class_label == tsd_w[i].class_label)

        # assertions
        self.assertTrue(check)
        self.assertIsInstance(tsd, TimeSeriesDataset)

    def test__ReadWrite__csv_to_tsd(self):
        w = "{}/{}/".format(self.target_dir, "csv-to-tsd")
        ensure_dir(w)
        # setup data
        ts_w = TimeSeries.create("01-01-1990", "01-03-1990", "1D")
        ts_w._data[COMPONENT_VALUES] = [0, 1, 2]
        ts_w._data["label_test"] = [0, None, 2]
        tsd_w = TimeSeriesDataset([ts_w, ts_w, ts_w])
        df_tsd = tsd_w.to_df()
        # save tsd as csv
        df_tsd.to_csv(f'{w}/tsd.csv')

        # load data
        tsd = ta.csv_to_tsd(f'{w}/tsd.csv')
        self.assertIsInstance(tsd, TimeSeriesDataset)

        check = True
        for i, ts in enumerate(tsd):
            check &= ts._data.equals(tsd_w[i]._data)
            check &= (ts.class_label == tsd_w[i].class_label)

        self.assertTrue(check)
