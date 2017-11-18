plotTree.py and plotTree_backbone.py have been forked and modified from @katholt repository (https://github.com/katholt/plotTree)
For more information on usage, visit their repo and website (https://holtlab.net/2016/10/12/global-picture-typhoid/). 

Dependencies: ete2 (ETE Toolkit 2), pyqt4

------------------------------------------------

In this repo, I modified their script to suit the particular needs of my anaysis.

## plotTree.py - 
It has added functionalities such as ```delete_branches``` in order to hide certain branches without modiying the resulting topology, and styling decisions. 

Example usage 1: 
> python ./plotTree.py --tree tree.nwk --info info.csv --outpdf outfile.pdf

Example usage 2 (full): 
> xvfb-run python ./plotTree.py --tree RAxML_bipartitions.BestTree.tre --info ./genotypes.csv --output test.png --width 750 --font_size 18 --fan --tags --labels Spoligotype Continent Cluster2_10_1 Cluster2_10_2 RD1009519_1010918 RD1209296_1210923 --outgroup SRR1792164 --colour_tags Cluster2_10_1 --branch_thickness 11 --line_width 2 --show_leaf_names --delete_branches SRR1173725 SRR1173284 --colour_backgrounds_by Cluster2_10_1 --print_colour_dict --colour_dict '{"NA":"White", "SB0145": "Gold", "SB0130":"MediumTurquoise", "SB0274":"Sienna", "SB1072":"LightSkyBlue", "SB0140":"Indigo","Not_found":"White", "SB1041": "OliveDrab","SB0265":"LimeGreen", "SB0673":"Orange", "SB1499":"Tan", "SB0121":"LightCoral", "SB1750":"Violet", "SB1040":"Red", "SB1757":"Coral", "SB0307":"Teal","SB0986":"DarkBlue", "SB1812":"#78c679", "SB0943":"#31a354", "SB1071":"#006837", "SB1033":"#fe9929", "SB2020":"#c2e699", "SB1308":"#ce1256", "SB0971":"#31a354", "SB1345":"#a1dab4", "SB0327":"#b2e2e2", "SB0484":"#238b45", "SB0292":"#fbb4b9", "SB1751":"#feebe2", "SB1758":"#ae017e", "SB1502":"#bae4bc", "SB2014":"#88419d", "SB1745":"#8c96c6", "SB0271":"#b3cde3", "SB1216":"#edf8fb","SB0815":"#fef0d9", "SB1069":"#ffffcc", "SB1348":"#cccccc", "SB2011":"#fed98e", "SB0267":"#fdae61", "SB2007":"#2b83ba", "SB1039":"#c2a5cf", "SB0120":"#7b3294", "SB2100":"#b8e186", "SB1031":"#d01c8b", "SB1504":"#dfc27d", "SB1446":"#a6611a", "SB0273":"#80cdc1", "SB0980":"#018571""}'

For the automatic (and random) assertion of colours to attributes from the metadata file (set in the --info parameter), you can use parseString.py and/or numberedPrefix_toColor.py 

## plotTree_backbone.py - 
Simplified version for the attainment of a rectangular, pruned tree. Hardcoded at it's best to fit my own data. Therefore, for flexibility, you should use plotTree.py


## parseString.py - 
Parse string to output a dictionary of random colours that adjust to plotTree.py colour format. Separator: space.

Usage: ```parseString.py [-h] str```

positional arguments:
  * str - String space-separated

Example:
```python ./parseString.py "uno dos"```

Output:
> {"uno": "#FFC81D", "dos": "#3A7BB4"}

## numberedPrefix_toColor.py - 
Given a prefix and an int, appends the prefix to the int from 0 to int and assigns each a random colour, to output a dictionary that adjust to plotTree.py format. Separator: space

usage: ```python ./numberedPrefix_toColor.py [-h] m p```

positional arguments:
  * m - Max num of items
  * p - Desired prefix

Example:
> python ./numberedPrefix_toColor.py 8 prefix

Output:
> {"prefix 1": "MediumTurquoise", "prefix 2": "OliveDrab", "prefix 3": "Teal", "prefix 4": "#E41A1C", "prefix 5": "#3A85A8", "prefix 6": "#FFDD25", "prefix 7": "Violet", "prefix 8": "MediumTurquoise"}
