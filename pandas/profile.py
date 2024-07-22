import pandas as pd
from ydata_profiling import ProfileReport
import numpy as np

data = pd.read_csv("pandas/netflix_titles.csv", encoding='unicode_escape').replace({np.nan: None})

profile = ProfileReport(data, title="Profiling Report")
profile.to_file("report.html")