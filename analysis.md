# Part 2 Analysis

## Scripting
The majority of the script was already completed with a few bugs that prevented the script from running to completion. However, studying the code gave me a better understanding of the similarities and differences between Pandas and Polars. While reading the code, I referred to the Polars documentation online to understand what specific functions did.

Similar to Pandas, the operations on Polars DataFrames seem to follow a .operation() format. However, the lazy query appears to essentially let me group series of operations together using .pipe() without defining an individual Python function for each of those groups. Based on my understanding of Polars from lecture and from reading documentation about it, Polars is then able to help streamline these groupings of operations to make them more efficient on the extremely large dataset that `generate_large_health_data.py` created.

## Debugging
There were a couple of lines where the code was running into errors. The first is when using .cut() to divide the data into groups based on BMI grouping. 10 and 60 were included as breaks in the list, which caused an error because there were 5 breaks specified and 4 group labels. Because the data had previously already been filtered to include only data where the BMI is between 10 and 60, I removed 10 and 60 from the list of breaks because:
- they would not functionally do anything since no data would fall outside the 10 to 60 range, so all data would fall on only one side of breaks at 10 and 60
- the syntax of the operation required the number of labels to be one more than the number of breaks

The second change was a correction from .groupby() to .group_by().