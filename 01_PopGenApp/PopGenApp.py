def find_path(tree, leaf, path=[]):
    path.append(leaf)
    
    if leaf not in tree:
        return path
    
    return find_path(tree, tree[leaf], path)

# Initialize an empty dictionary to hold the tree
tree = {}

# Open the file and read it line by line
with open('chrY_hGrpTree_isogg2016.txt', 'r') as file:
    for line in file:
        # Split each line into leaf and root
        leaf, root = line.strip().split('\t')
        
        # Add the leaf and root to the tree
        tree[leaf] = root
      

# Open the output file
with open('outfile.txt', 'w') as outfile:
    # Find the path from each leaf to the root
    for leaf in tree.keys():
        path = find_path(tree, leaf, [])
        path.reverse()  # Reverse the path so it starts with the root
        outfile.write(' -> '.join(path) + '\n')

#%%

import pandas as pd

# Read the Excel file
df = pd.read_excel('AADR Annotation.xlsx')

# Write to a TSV file
df.to_csv('AADR_Annotation.tsv', sep='\t', index=False)

#%%
import pandas as pd

df = pd.read_csv('AADR_Annotation.tsv', sep='\t')

# Extract columns 9 and 27 from the DataFrame
subset_df = df.iloc[:, [8, 26]]

# Write the subset DataFrame to a new TSV file
subset_df.to_csv('AADRsubset.tsv', sep='\t', index=False)



#%%

import pandas as pd

# Read the TSV file into a DataFrame
df = pd.read_csv('AADRsubset.tsv', sep='\t')

# Initialize an empty dictionary to hold the date means
date_means = {}

# Open the outfile.txt file and read it line by line
with open('outfile.txt', 'r') as file:
    for line in file:
        # Split the line into haplogroups
        haplogroups = line.strip().split(' -> ')
        
        # Check each haplogroup in the line
        for haplogroup in haplogroups:
            # If the haplogroup is in the DataFrame, fetch the date mean and store it in the dictionary
            if haplogroup in df['Y haplogroup (manual curation in ISOGG format)'].values:
                date_mean = df[df['Y haplogroup (manual curation in ISOGG format)'] == haplogroup]['Date mean in BP in years before 1950 CE [OxCal mu for a direct radiocarbon date, and average of range for a contextual date]'].values[0]
                date_means[haplogroup] = date_mean

# Add the root haplogroup to the dictionary
date_means['Root'] = 200000

# Convert the dictionary to a DataFrame
date_means_df = pd.DataFrame(list(date_means.items()), columns=['Haplogroup', 'Date Mean'])

# Write the DataFrame to a new TSV file
date_means_df.to_csv('HaplogroupBPE.tsv', sep='\t', index=False)


#%%
import pandas as pd

# Read the data from the file
df = pd.read_csv('HaplogroupBPE.tsv', sep='\t')

# Perform the calculation
df['Date Mean'] = 1950 - df['Date Mean']

# Write the result to a new file
df.to_csv('RootHaplogroupBPE.tsv', sep='\t', index=False)
