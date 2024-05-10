import pandas as pd
from ydata_profiling import ProfileReport

data = pd.read_csv("pandas/netflix_titles.csv", encoding='unicode_escape')

profile = ProfileReport(data, title="Profiling Report")
profile.to_file("report.html")