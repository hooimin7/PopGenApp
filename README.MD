# Load packages (Run in en environment 'biopython' loaded with all these packages)
pandas                    2.1.4           
numpy                     1.26.4          
python                    3.12.2               
openpyxl                  3.0.10          
networkx                  3.2.1                    
pyvis                     0.3.2                    
streamlit                 1.31.1                   
pyvis-timeline            0.0.8                    
streamlit-vis-timeline    0.3.0                    
pip install networkx

# 01_PopGenApp
This Python script is doing two main tasks:

1. **Building a tree from a text file and writing the paths from each leaf to the root to an output file:**

   The script first defines a recursive function `find_path` that, given a tree (represented as a dictionary), a leaf node, and a path (initially empty), appends the leaf to the path, checks if the leaf is in the tree, and if so, recursively calls itself with the parent of the leaf. The function returns the path when the leaf is not in the tree, which means it has reached the root of the tree.

   The script then initializes an empty dictionary to represent the tree. It opens a file (`chrY_hGrpTree_isogg2016.txt`), reads it line by line, and for each line, it splits the line into a leaf and a root and adds them to the tree.
   *`chrY_hGrpTree_isogg2016.txt` extracted by Eran Elhaik and obtained from https://isogg.org/tree/*

   After building the tree, the script opens an output file (`outfile.txt`), and for each leaf in the tree, it finds the path from the leaf to the root using the `find_path` function, reverses the path so it starts with the root, and writes the path to the output file.

2. **Reading an Excel file into a pandas DataFrame, writing the DataFrame to a TSV file, and printing the third column of the DataFrame:**

   The script imports the pandas library, reads an Excel file (`AADR Annotation.xlsx`) into a DataFrame 'df', and writes 'df' to a TSV file (`AADR_Annotation.tsv`).
   *`AADR Annotation.xlsx` extracted by Eran Elhaik and obtained from*
   *https://reich.hms.harvard.edu/allen-ancient-dna-resource-aadr-downloadable-genotypes-present-day-and-ancient-dna-data*
   
3. **Reading a TSV file into a DataFrame:**

The script reads a TSV file (`AADR_Annotation.tsv `) into a pandas DataFrame df. The pd.read_csv function is used with the sep='\t' argument to specify that the file is tab-separated.

Extracting specific columns from the DataFrame: The script creates a new DataFrame subset_df that includes only the 9th and 27th columns of df. This is done using the df.iloc function, which is used for indexing by integer location. The : symbol means "all rows", and [8, 26] specifies the 9th and 27th columns (Python uses 0-based indexing, so these are at indices 8 and 26).

Writing the subset DataFrame to a new TSV file: Finally, the script writes subset_df to a new TSV file named `AADRsubset.tsv `. The DataFrame.to_csv method is used with the sep='\t' argument to specify that the file should be tab-separated, and the index=False argument is used to prevent pandas from writing row indices to the TSV file.

4. **Performing data extraction and transformation on a tab-separated values (TSV) file**
This Python script is  using the pandas library. The script then reads a TSV file `AADRsubset.tsv ` into a pandas DataFrame. An empty dictionary 'date_means' is initialized to store the mean dates associated with each haplogroup. The script opens and reads a file named `outfile.txt ` line by line. Each line is split into haplogroups based on the ' -> ' delimiter. For each haplogroup in the line, the script checks if the haplogroup is present in the DataFrame's 'Y haplogroup (manual curation in ISOGG format)' column. If it is, the corresponding date mean is fetched and stored in the 'date_means' dictionary with the haplogroup as the key. This code will take the first 'date mean' of the matched haplogroup from the `AADRsubset.tsv ` file. After going through all the lines in `outfile.txt `, the script adds a root haplogroup to the 'date_means' dictionary with a date mean of 200000. The 'date_means' dictionary is converted into a DataFrame 'date_means_df' with 'Haplogroup' and 'Date Mean' as column names. Finally, the 'date_means_df' DataFrame is written to a new TSV file named `HaplogroupBPE.tsv `. The 'index=False' argument in the 'to_csv' function means that the DataFrame's index will not be written into the file.

5. **Performs a calculation on the column named 'Date mean in BP in years before 1950 CE [OxCal mu for a direct radiocarbon date, and average of range for a contextual date]'**

The script reads a TSV file `HaplogroupBPE.tsv ` into a pandas DataFrame. It subtracts the values in this column from 1950. This is a way to convert the dates from years before 1950 CE to years after 1950 CE. Finally, the script writes the DataFrame, which now includes the calculated column, back to a new TSV file named `RootHaplogroupBPE.tsv `. The 'index=False' argument in the 'to_csv' function means that the DataFrame's index will not be written into the file.

# 02_Plot (Test model)

1.  **Importing Libraries and Reading Data**

The script begins by importing the necessary libraries: pandas for data manipulation, networkx for creating and manipulating complex networks, and pyvis for interactive network visualization. It then reads data from a TSV file named `RootHaplogroupBPE.tsv ` into a pandas DataFrame.

2. **Creating a Directed Graph and Adding Nodes**

The script creates a directed graph using the networkx library. It then iterates over the DataFrame, adding each haplogroup as a node in the graph.

3. **Reading Data from a Text File and Adding Edges**

The script opens a text file named `outfile.txt ` and reads it line by line. Each line is split into haplogroups, and edges are added to the graph based on this information.

4. **User Input and Validation**

The script prompts the user to enter two haplogroups. It checks if these haplogroups are present in the graph. If they are not, it prints a message and ends the execution.

5. **Finding Paths and Creating a Subgraph**

If the haplogroups are present in the graph, the script finds all paths from the root to the leaves for the two haplogroups. It then flattens the list of paths and removes duplicate nodes. Using these nodes, it creates a subgraph.

6. **Visualizing the Graph**

The script then converts the networkx graph to a pyvis graph for visualization. It sets various options for the graph, such as disabling physics and enabling node dragging. It also sets the layout to a non-hierarchical layout. The graph is then displayed in an HTML file named `graph.html `.

# 03_CheckCE (Filtering CE or BCE for selecting the oldest Date Mean for each haplogroup)

1. **Data Extraction and Transformation (For CE dataset)**

This script imports the pandas library and reads a TSV file `AADR_Annotation.tsv ` into a pandas DataFrame. It then extracts columns 9, 11, and 27 from the DataFrame and writes this subset DataFrame to a new TSV file named `checkCE.tsv `.

2. **Data Filtering**

The script reads `checkCE.tsv ` into a DataFrame and filters the rows where the second column contains 'CE' but not 'BCE'. The filtered DataFrame is then written to a new TSV file named `CEonly.tsv `.
 
 *Check the CE* 
```awk
awk -F'\t' '$2 ~ /CE[^a-zA-Z]/ && $2 !~ /BCE/' checkCE.tsv
```
3. **Further Data Extraction**

The script reads `CEonly.tsv ` into a DataFrame, extracts columns 1 and 3, and writes this subset DataFrame to a new TSV file named `CEonlysubset.tsv`.

4. **Data Analysis CE**

The script reads `CEonlysubset.tsv` into a DataFrame and initializes an empty dictionary 'date_means' to store the *smallest date mean* associated with each haplogroup. The script opens and reads a file named `outfile.txt ` line by line. Each line is split into haplogroups based on the ' -> ' delimiter.
For each haplogroup in the line, the script checks if the haplogroup is present in the DataFrame's 'Y haplogroup (manual curation in ISOGG format)' column. If it is, the *smallest* corresponding date mean is fetched and stored in the 'date_means' dictionary with the haplogroup as the key. The 'date_means' dictionary is then converted into a DataFrame 'date_means_df' with 'Haplogroup' and 'Date Mean' as column names. Finally, the 'date_means_df' DataFrame is written to a new TSV file named `CEonlyHaplo.tsv`. The 'index=False' argument in the 'to_csv' function means that the DataFrame's index will not be written into the file.

5. **Data Analysis BCE, same procedures as CE (1-3) the last analysis differs**
The script reads `BCEonlysubset.tsv` into a DataFrame and initializes an empty dictionary 'date_means' to store the *largest date mean* associated with each haplogroup. The script opens and reads a file named `outfile.txt ` line by line. Each line is split into haplogroups based on the ' -> ' delimiter.
For each haplogroup in the line, the script checks if the haplogroup is present in the DataFrame's 'Y haplogroup (manual curation in ISOGG format)' column. If it is, the *largest* corresponding date mean is fetched and stored in the 'date_means' dictionary with the haplogroup as the key. The 'date_means' dictionary is then converted into a DataFrame 'date_means_df' with 'Haplogroup' and 'Date Mean' as column names. Finally, the 'date_means_df' DataFrame is written to a new TSV file named `BCEonlyHaplo.tsv`. The 'index=False' argument in the 'to_csv' function means that the DataFrame's index will not be written into the file.

6. **Concatenating DataFrames**

The script begins by importing the pandas library. It then reads two TSV files, `BCEonlyHaplo.tsv ` and `CEonlyHaplo.tsv `, into two separate pandas DataFrames. These two DataFrames are then concatenated, or joined together, into a single DataFrame. This combined DataFrame is then written to a new TSV file named `MergedHaplo.tsv `.

7. **Calculating Date Means**

Next, the script reads the data from the `MergedHaplo.tsv ` file into a DataFrame. It then performs a calculation on the 'Date Mean' column of the DataFrame, subtracting each value in the column from 1950. This effectively converts the date means into years before 1950 CE. The DataFrame, with the updated 'Date Mean' column, is then written to a new TSV file named `MergedHaploCal.tsv `.

8. **Sorting and Removing Duplicates**

Finally, the script reads the `MergedHaploCal.tsv ` file into a DataFrame. It converts the 'Date Mean' column to a numeric type to ensure that the values can be sorted correctly. The DataFrame is then sorted by the 'Date Mean' column. 

The script then removes duplicate values in the 'Haplogroup' column, keeping only the first occurrence of each duplicate by removing the duplicates value which has the positive date mean (the modern haplogroup). This is done to ensure that each haplogroup is represented only once in the final data. 

The cleaned and sorted DataFrame is then written to a new TSV file named `FinalMergedHaplo.tsv `.

# 04_GUI (Grahphical User Interspace)

*Run on terminal in 04_GUI directory*
```bash
streamlit run /Users/med-snt/PopGenApp/04_GUI/GUI.py
```
*Example of haplogroups: A1b1b2b1 and R2a1b1a*

1. **Importing Libraries**

The script starts by importing necessary libraries. These include streamlit for creating the web app, pandas for data manipulation, networkx for creating and manipulating complex networks, pyvis for interactive network visualization, numpy for numerical operations, and time for controlling the flow of the script.

2. **Defining Text Strings**

Two text strings are defined, `_Ancient_connection` and `_Have_you`, which contain introductory text about the app.

3. **Defining the Stream Data Function**

The `stream_data` function is defined. This function yields one word at a time from the `_Have_you` string, waits for 0.02 seconds, reads data from an Excel file into a DataFrame, yields the DataFrame, waits for another 0.02 seconds, and then yields one word at a time from the `_Ancient_connection` string.

4. **Displaying the Introduction**

If the "Introduction" button is clicked in the Streamlit app, the `stream_data` function is called and its output is written to the app.

5. **Reading Data and Creating a Graph**

The script reads data from a TSV file named `RootHaplogroupBPE.tsv `or `FinalMergedHaplo.tsv   into a DataFrame. It then creates a directed graph and adds each haplogroup from the DataFrame as a node in the graph.

6. **Adding Edges to the Graph**

The script opens a text file named `outfile.txt ` and reads it line by line. Each line is split into haplogroups, and edges are added to the graph based on this information.

7. **Creating the Streamlit App**

The script sets the title of the Streamlit app to `Ancient Connections `. It then creates two text input fields for the user to enter haplogroups.

8. **Checking User Input and Creating a Subgraph**

If the "Submit" button is clicked, the script checks if the entered haplogroups are in the graph. If they are not, it displays a message. If they are, it finds all paths from the root to the leaves for the two haplogroups, flattens the list of paths, removes duplicate nodes, and creates a subgraph with these nodes.

9. **Visualizing the Graph**

The script converts the networkx graph to a pyvis graph for visualization. It sets various options for the graph, such as enabling configuration, setting the edge color, enabling physics, enabling node dragging, and disabling the hierarchical layout. It then saves the graph as an HTML file.

10. **Displaying the Graph**

The script reads the HTML file and displays it in the Streamlit app.





*Useful tutorial*
**Pyvis, Networkx**
https://pyvis.readthedocs.io/en/latest/tutorial.html
https://networkx.org/documentation/stable/reference/classes/digraph.html

**Streamlit** 
https://docs.streamlit.io/library/api-reference/write-magic/st.write_stream
