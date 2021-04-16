import pandas as pd
import glob
import numpy as np

# locate downloads folder
from pathlib import Path
downloads_path = str(Path.home() / "Downloads")
path1 = downloads_path
# import csv from downloads folder
allFiles = glob.glob(path1 + "/*.csv")
# create dataframe from csv
data_df = pd.DataFrame()
for file_ in allFiles:
    data_df = pd.read_csv(file_, sep=",", error_bad_lines=False, index_col=False, dtype='unicode')

# transfer override values to Portfolio Static URL
data_df['Portfolio Static URL'] = np.where(data_df['Portfolio Static URL'].isnull(),
                                           data_df['Portfolio Static URL (override)'], data_df['Portfolio Static URL'])

# adjust URLs
data_df['Portfolio Static URL'] = data_df['Portfolio Static URL'].replace({'jkey=https://': ''}, regex=True)
data_df['Portfolio Static URL'] = data_df['Portfolio Static URL'].replace({'jkey=http://': ''}, regex=True)
data_df['Portfolio Static URL'] = data_df['Portfolio Static URL'].replace({'/': ''}, regex=True)

duplicateRowsDF = data_df[data_df.duplicated(['Portfolio Static URL', 'MMS Id'], keep=False)]

# output to xlsx
duplicateRowsDF.to_excel(path1 + "/duplicates.xlsx", index=False)
