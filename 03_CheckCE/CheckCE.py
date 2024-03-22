#%% CE
import pandas as pd

df = pd.read_csv('/Users/med-snt/PopGenApp/AADR_Annotation.tsv', sep='\t')

# Extract columns 9 and 27 from the DataFrame
subset_df = df.iloc[:, [8, 10, 26]]

# Write the subset DataFrame to a new TSV file
subset_df.to_csv('checkCE.tsv', sep='\t', index=False)


#%%
import pandas as pd

# Read the file into a DataFrame
df = pd.read_csv('checkCE.tsv', sep='\t')

# Filter the rows where the second column contains 'CE' but not 'BCE'
df = df[df.iloc[:, 1].str.contains('CE') & ~df.iloc[:, 1].str.contains('BCE')]

# Write the filtered DataFrame to a new file, including the header
df.to_csv('CEonly.tsv', sep='\t', header=True, index=False)

#%%
import pandas as pd

df = pd.read_csv('CEonly.tsv', sep='\t')

# Extract columns 9 and 27 from the DataFrame
subset_df = df.iloc[:, [0, 2]]

# Write the subset DataFrame to a new TSV file
subset_df.to_csv('CEonlysubset.tsv', sep='\t', index=False)


#%%
import pandas as pd

# Read the TSV file into a DataFrame
df = pd.read_csv('CEonlysubset.tsv', sep='\t')

# Initialize an empty dictionary to hold the date means
date_means = {}

# Open the outfile.txt file and read it line by line
with open('outfile.txt', 'r') as file:
    for line in file:
        # Split the line into haplogroups
        haplogroups = line.strip().split(' -> ')
        
        # Check each haplogroup in the line
        for haplogroup in haplogroups:
            # If the haplogroup is in the DataFrame, fetch the smallest date mean and store it in the dictionary
            if haplogroup in df['Y haplogroup (manual curation in ISOGG format)'].values:
                date_mean = df[df['Y haplogroup (manual curation in ISOGG format)'] == haplogroup]['Date mean in BP in years before 1950 CE [OxCal mu for a direct radiocarbon date, and average of range for a contextual date]'].min()
                date_means[haplogroup] = date_mean

# Convert the dictionary to a DataFrame
date_means_df = pd.DataFrame(list(date_means.items()), columns=['Haplogroup', 'Date Mean'])

# Write the DataFrame to a new TSV file
date_means_df.to_csv('CEonlyHaplo.tsv', sep='\t', index=False)

#%% BCE
import pandas as pd

# Read the file into a DataFrame
df = pd.read_csv('checkCE.tsv', sep='\t', header=None)

# Filter the rows where the second column contains 'calBCE' or 'BCE' but not 'CE' alone
df = df[(df[1].str.contains('calBCE') | df[1].str.contains('BCE')) & ~df[1].str.contains(r'\bCE\b')]

# Write the filtered DataFrame to a new file
df.to_csv('BCEonly.tsv', sep='\t', header=False, index=False)

#%%
import pandas as pd

df = pd.read_csv('BCEonly.tsv', sep='\t')

# Extract columns 9 and 27 from the DataFrame
subset_df = df.iloc[:, [0, 2]]

# Write the subset DataFrame to a new TSV file
subset_df.to_csv('BCEonlysubset.tsv', sep='\t', index=False)


#%%
import pandas as pd

# Read the TSV file into a DataFrame
df = pd.read_csv('BCEonlysubset.tsv', sep='\t')

# Initialize an empty dictionary to hold the date means
date_means = {}

# Open the outfile.txt file and read it line by line
with open('outfile.txt', 'r') as file:
    for line in file:
        # Split the line into haplogroups
        haplogroups = line.strip().split(' -> ')
        
        # Check each haplogroup in the line
        for haplogroup in haplogroups:
            # If the haplogroup is in the DataFrame, fetch the smallest date mean and store it in the dictionary
            if haplogroup in df['Y haplogroup (manual curation in ISOGG format)'].values:
                date_mean = df[df['Y haplogroup (manual curation in ISOGG format)'] == haplogroup]['Date mean in BP in years before 1950 CE [OxCal mu for a direct radiocarbon date, and average of range for a contextual date]'].max()
                date_means[haplogroup] = date_mean

# Add the root haplogroup to the dictionary
date_means['Root'] = 200000

# Convert the dictionary to a DataFrame
date_means_df = pd.DataFrame(list(date_means.items()), columns=['Haplogroup', 'Date Mean'])

# Write the DataFrame to a new TSV file
date_means_df.to_csv('BCEonlyHaplo.tsv', sep='\t', index=False)

#%% Concatenate the two DataFrames
import pandas as pd

# Read the TSV files into DataFrames
df1 = pd.read_csv('BCEonlyHaplo.tsv', sep='\t')
df2 = pd.read_csv('CEonlyHaplo.tsv', sep='\t')

# Concatenate the DataFrames
df = pd.concat([df1, df2])

# Write the DataFrame to a new TSV file
df.to_csv('MergedHaplo.tsv', sep='\t', index=False)


#%% Calculate the date means in years before 1950 CE
import pandas as pd

# Read the data from the file
df = pd.read_csv('MergedHaplo.tsv', sep='\t')

# Perform the calculation
df['Date Mean'] = 1950 - df['Date Mean']

# Write the result to a new file
df.to_csv('MergedHaploCal.tsv', sep='\t', index=False)

#%%
# Sort unique haplogroups and remove the duplicates value which has the positive date mean
import pandas as pd

# Read the TSV file
df = pd.read_csv('MergedHaploCal.tsv', sep='\t', header=0)

# Convert the 'Date Mean' column to numeric type
df['Date Mean'] = pd.to_numeric(df['Date Mean'], errors='coerce')

# Sort by the 'Date Mean' column
df = df.sort_values(by=['Date Mean'])

# Drop duplicates in the 'Haplogroup' column, keeping the first occurrence
df = df.drop_duplicates(subset=['Haplogroup'], keep='first')

# Write back to a new TSV file
df.to_csv('FinalMergedHaplo.tsv', sep='\t', index=False)
