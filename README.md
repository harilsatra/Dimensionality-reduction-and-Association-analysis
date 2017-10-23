PCA (Dimensionality Reduction)
-------------

**TO GENERATE THE REDUCED DIMENSION DATAPOINTS:**
	1. Store the input file in the same folder as the folder which contains the file 'pca.py'
	2. Run the 'pca.py'
	3. It will prompt you to enter a file name. Here enter the input file name which you stored in the same folder as pca.py'.
	4. Once you enter the filename it will generate three files of the following format:
> - pca_(no. of input file).csv --> This file contains the data points of the reduced dimension along with the mapping of the corresponding disease name using the PCA algorithm.
> - tsne_(no. of input file).csv --> This file contains the data points of the reduced dimension along with the mapping of the corresponding disease name using the TSNE algorithm.
> - svd_(no. of input file).csv --> This file contains the data points of the reduced dimension along with the mapping of the corresponding disease name using the SVD algorithm

 **Note:** Enter new file if you wish to or type exit to stop.
 
**TO GENERATE SCATTER PLOT OF THE REDUCED DIMENSIONS:**
	1. Store the output files from the previous step for which you want the visualization in the same folder as 'plot.r'
	2. Run the 'plot.r' script
	3. It will prompt you to enter a file name. Here enter the csv file name which you stored in the same folder as 'plot.r'.
	4. Once you enter the file name the scatter plot for the corresponding file will be displayed
Apriori (Association Analysis)
-------------
**TO GENERATE THE REDUCED ASSOCIATION RULES:**
1. Store the input file which you want to read in the same folder as 'apriori.py'
2. If the file is other than 'associationruletestdata.txt' then change the filename on line 14 in 'apriori.py'
3. Run the file 'apriori.py'
4. The following information will be displayed for minimum support= (30%,40%,50%,60%,70%) and minimum confidence= 70%:
	
> - Number of frequent itemsets for varying length from 1 till the number is not 0
> - Number of all length frequent itemset
> - Result of all the sample template queries provided.

**Note:** If the minimum confidence is something other than 70% change the variable 'minconf' on line 189 to the desired value (percentage/100). 