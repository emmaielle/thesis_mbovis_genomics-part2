plotTree.py and plotTree.py have been forked and modifyed from @katholt repository (https://github.com/katholt/plotTree)
For more information on usage, visit their repo and website (https://holtlab.net/2016/10/12/global-picture-typhoid/). 

Dependencies: ete2 (ETE Toolkit 2), pyqt4

------------------------------------------------

In this repo, I modified their script to suit the particular needs of my anaysis.

## plotTree.py - 
It has added functionalities such as ```delete_branches``` in order to hide certain branches without modiying the resulting topology, and styling decisions. 

Example usage 1: ```python /vlsci/VR0082/shared/code/holtlab/plotTree.py --tree tree.nwk --info info.csv --outpdf outfile.pdf```

Example usage 2 (full): ```xvfb-run python ./plotTree.py --tree RAxML_bipartitions.BestTree.tre --info ./genotypes.csv --output test.png --width 750 --font_size 18 --fan --tags --labels Spoligotype Continent Cluster2_10_1 Cluster2_10_2 RD1009519_1010918 RD1209296_1210923 RD1312977_1314689 RD1319619_1324412 RD1330942_1332977 RD1531687_1543730 RD1764647_1772242 RD1764652_1772888 RD1766212_1773484 RD1769369_1773874 RD1770306_1771404 RD1771720_1773818 RD1772660_1773872 RD1863310_1869952 RD1864575_1865888 RD2128199_2129301 RD2176783_2181823 RD2317445_2319067 RD3379943_3386666 RD3404007_3407778 RD3663899_3668653 RD3688270_3689325 RD3890969_3894019 RD4233584_4238604 RD485420_486460 RD681589_695668 --outgroup SRR1792164 --colour_tags Cluster2_10_1 --branch_thickness 11 --line_width 2 --show_leaf_names --delete_branches SRR1173725 SRR1173284 --colour_backgrounds_by Cluster2_10_1 --print_colour_dict --colour_dict '{"NA":"White", "SB0145": "Gold", "SB0130":"MediumTurquoise", "SB0274":"Sienna", "SB1072":"LightSkyBlue", "SB0140":"Indigo","Not_found":"White", "SB1041": "OliveDrab","SB0265":"LimeGreen", "SB0673":"Orange", "SB1499":"Tan", "SB0121":"LightCoral", "SB1750":"Violet", "SB1040":"Red", "SB1757":"Coral", "SB0307":"Teal","SB0986":"DarkBlue", "SB1812":"#78c679", "SB0943":"#31a354", "SB1071":"#006837", "SB1033":"#fe9929", "SB2020":"#c2e699", "SB1308":"#ce1256", "SB0971":"#31a354", "SB1345":"#a1dab4", "SB0327":"#b2e2e2", "SB0484":"#238b45", "SB0292":"#fbb4b9", "SB1751":"#feebe2", "SB1758":"#ae017e", "SB1502":"#bae4bc", "SB2014":"#88419d", "SB1745":"#8c96c6", "SB0271":"#b3cde3", "SB1216":"#edf8fb","SB0815":"#fef0d9", "SB1069":"#ffffcc", "SB1348":"#cccccc", "SB2011":"#fed98e", "SB0267":"#fdae61", "SB2007":"#2b83ba", "SB1039":"#c2a5cf", "SB0120":"#7b3294", "SB2100":"#b8e186", "SB1031":"#d01c8b", "SB1504":"#dfc27d", "SB1446":"#a6611a", "SB0273":"#80cdc1", "SB0980":"#018571", "Lineage2 5": "#946DA3", "Lineage2 4": "#540D6E","Lineage2 7": "#6F5196", "Lineage2 6": "#8D80AD", "Lineage2 1": "#d7191c",  "Lineage2 3": "#F49CBB", "Lineage2 2": "#EE4266", "Lineage2 9": "#6D9DC5", "Lineage2 8":"#53599A", "Lineage2 11": "#46ACC2", "Lineage2 10": "#496DDB", "Lineage2 13": "#679436", "Lineage2 12": "#5FAD41", "Lineage2 15": "#aecf8e", "Lineage2 14": "#8ecf8f", "Lineage2 17": "#E2EB98", "Lineage2 16": "#95BF74", "Lineage2 19": "#EE964B", "Lineage2 18": "#FFD23F", "Lineage 4": "#5FAD41", "Lineage 5": "#FFD23F", "Lineage 2": "#6F5196", "Lineage 3": "#496DDB", "Lineage 1": "#d7191c", "NA":"White", "Latin America":"Indigo", "Europe":"LightSkyBlue", "Africa":"OliveDrab", "North America":"Red", "Asia":"Gold", "UNKNOWN":"White", "Oceania":"Teal", "RD1009519_1010918": "#3A7BB4", "RD1209296_1210923": "Tan", "RD1312977_1314689": "LimeGreen", "RD1319619_1324412": "#FFF12D", "RD1330942_1332977": "#FF9E0C", "RD1531687_1543730": "#566B9B", "RD1764647_1772242": "#FFC81D", "RD1764652_1772888": "Coral", "RD1766212_1773484": "Red", "RD1769369_1773874": "#8F4A68", "RD1770306_1771404": "DarkBlue", "RD1771720_1773818": "MediumTurquoise", "RD1772660_1773872": "Violet", "RD1863310_1869952": "#F9F432", "RD1864575_1865888": "#FFB314", "RD2128199_2129301": "Teal", "RD2176783_2181823": "LightSkyBlue", "RD2317445_2319067": "Indigo", "RD3379943_3386666": "#3A85A8", "RD3404007_3407778": "#735B81", "RD3663899_3668653": "#FF8904", "RD3688270_3689325": "Gold", "RD3890969_3894019": "Sienna", "RD4233584_4238604": "#E41A1C", "RD485420_486460": "#AB3A4E", "RD681589_695668": "#419584"}'```

For the automatic (and random) assertion of colours to attributes from the metadata file (set in the --info parameter), you can use parseString.py and/or numberedPrefix_toColor.py 

## plotTree_backbone.py - 
Simplified version for the attainment of a rectangular, pruned tree. Hardcoded at it's best to fit my own data. Therefore, for flexibility, you should use plotTree.py


## parseString.py - 


## numberedPrefix_toColor.py - 