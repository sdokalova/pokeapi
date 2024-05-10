import pandas as pd
import pytest

data = pd.read_csv("netflix_titles.csv", encoding='unicode_escape')
expected_columns = [
    "show_id", "type", "title", "director", "cast", "country", "date_added", "release_year", "rating",
    "duration", "listed_in", "description"
]


def test_schema():
    assert sorted(data.columns.values.tolist()) == sorted(expected_columns)


cleaned_data = data[expected_columns]


@pytest.mark.parametrize("column", ["show_id", "title", "release_year"])
def test_not_null(column):
    assert not cleaned_data.isnull().any()[column]

def test_duplicates():
    print(cleaned_data[""].is_unique)
