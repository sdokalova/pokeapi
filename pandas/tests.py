import pandas as pd
import pytest
import numpy as np
import datetime as dt


data = pd.read_csv("netflix_titles.csv", encoding='unicode_escape')
expected_columns = [
    "show_id", "type", "title", "director", "cast", "country", "date_added", "release_year", "rating",
    "duration", "listed_in", "description"
]
categories = [
    "A", "G", "NC-17", "NR", "PG", "PG-13", "R", "TV-14", "TV-G", "TV-MA", "TV-PG", "TV-Y", "TV-Y7", "TV-Y7-FV", "UR"
]


def test_schema():
    """Verify that the dataset includes all expected columns and does not contain any unexpected columns."""
    assert sorted(data.columns.values.tolist()) == sorted(expected_columns)


cleaned_data = data.dropna(how='all', axis=1).replace({np.nan: None})


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


def test_category():
    """Validate that the rating column contains only allowed rating categories."""
    print("Extra categories: ", cleaned_data["rating"][~cleaned_data["rating"].isin(categories)])
    assert cleaned_data["rating"].isin(categories).all()


def test_updates():
    """Determine if the dataset includes recently added titles."""
    filtered_df = cleaned_data["date_added"][~cleaned_data["date_added"].isna()]
    assert not filtered_df[filtered_df.str.endswith("2022")].empty


def test_ratings():
    """Ensure logical consistency in data, particularly for TV shows with mature ratings."""
    shows = cleaned_data.loc[cleaned_data["type"] == "TV Show"].loc[cleaned_data["rating"] == "TV-MA"]
    res = shows["title"].to_list()
    assert cleaned_data.loc[cleaned_data['title'].isin(res)]["title"].all()


def test_country_representation():
    """Check the geographic diversity of the dataset."""
    data = cleaned_data["country"].str.split(pat=", ").to_list()
    countries = []
    for entity in data:
        if entity:
            if type(entity) == list:
                for country in entity:
                    countries.append(country)
            else:
                countries.append(entity)

    assert len(set(countries)) > 5
