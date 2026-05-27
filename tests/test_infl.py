import pandas as pd
import ons


class TestGetCpih:
    def test_returns_series(self):
        result = ons.get_cpih()
        assert isinstance(result, pd.Series)

    def test_index_is_datetime(self):
        result = ons.get_cpih()
        assert isinstance(result.index, pd.DatetimeIndex)

    def test_values_are_float(self):
        result = ons.get_cpih()
        assert result.dtype == float

    def test_sorted_ascending(self):
        result = ons.get_cpih()
        assert result.index.is_monotonic_increasing

    def test_has_recent_data(self):
        result = ons.get_cpih()
        assert result.index[-1] >= pd.Timestamp("2026-02-01")

    def test_no_missing_values(self):
        result = ons.get_cpih()
        assert not result.isna().any()


class TestGetInflationCpih:
    def test_returns_series(self):
        result = ons.get_inflation_cpih()
        assert isinstance(result, pd.Series)

    def test_no_missing_values(self):
        result = ons.get_inflation_cpih()
        assert not result.isna().any()

    def test_values_are_rates(self):
        result = ons.get_inflation_cpih()
        assert (result.abs() < 1).all()
