import pandas as pd
import pytest
import re
import numpy as np

data = pd.read_csv("netflix_titles.csv", encoding='unicode_escape')
expected_columns = [
    "show_id", "type", "title", "director", "cast", "country", "date_added", "release_year", "rating",
    "duration", "listed_in", "description"
]


def test_schema():
    """Verify that the dataset includes all expected columns and does not contain any unexpected columns."""
    assert sorted(data.columns.values.tolist()) == sorted(expected_columns)


cleaned_data = data[expected_columns]


@pytest.mark.parametrize("column", ["show_id", "title", "release_year"])
def test_not_null(column):
    """Ensure there are no missing values in critical columns that are essential for analysis."""
    assert not cleaned_data.isnull().any()[column]


def test_duplicates():
    """Ensure that there are no duplicate records in the dataset."""
    assert cleaned_data["show_id"].is_unique


def test_types():
    """Confirm that data types for each column are consistent with their expected types."""
    assert pd.api.types.is_signed_integer_dtype(cleaned_data["release_year"])
    assert pd.api.types.is_string_dtype(cleaned_data["title"])


def test_year_range():
    """Ensure the release_year falls within a reasonable and expected historical range."""
    assert cleaned_data["release_year"].min() >= 1900
    assert cleaned_data["release_year"].max() <= 2024


def test_duration():
    print(cleaned_data["duration"])
    duration = cleaned_data["duration"]
    # res = cleaned_data["duration"].str.contains("^[0-100]Season")
    assert duration.str.contains(r'^[0-9]\s\bSeason\b') or duration.str.contains(r'^[0-9]\s\bSeasons\b') or duration.str.contains(r'\d+\s\bmin\b')