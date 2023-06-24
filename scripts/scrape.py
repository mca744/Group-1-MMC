import tabula
import pandas as pd

# Path to your pdf file
file = "/Users/matanlevy/Desktop/CIS 4400/Group-1-MMC/Data/pdfdata/tsa-total-throughput-data-june-11-2023-to-june-17-2023.pdf"

# Read PDF into list of DataFrame
dfs = tabula.read_pdf(file, pages='all')

# Concatenate all dataframes into a single one
combined_df = pd.concat(dfs, ignore_index=True)

# Convert combined DataFrame to JSON, orient by index for better structure
json = combined_df.to_json(orient='index')

# Write the JSON to a file
with open("/Users/matanlevy/Desktop/CIS 4400/Group-1-MMC/Data/jsondata/1.json", "w") as f:
    f.write(json)

print("done")