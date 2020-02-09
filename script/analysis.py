import pandas as pd

# Paths to csv
newegg_csv_path = './csv_files/newegg_GPU_2020-02-07.csv'
# import collected data from websites
newegg_GPU_df = pd.read_csv(newegg_csv_path)

