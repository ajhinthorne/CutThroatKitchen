####Importing Datasets
# %%
import pandas as pd
import math as m
import numpy as np
import matplotlib.pyplot as plt


###Importing CSV from Github
# %%
comp_by_round = pd.read_csv("https://raw.githubusercontent.com/ajhinthorne/CutThroatKitchen/master/Cutthroat%20Kitchen%20Data%20-%20DataOutput.csv")
comp_by_round.head(5)


####Plan for data manipulation
##Need a dataset for sabotages to analyze sabotage type
##Need a winners dataset to analyze winners


### Generating the winners dataset
##one record per winner, 
# %%
winner_ids = comp_by_round[(comp_by_round.winner_binary == True)]['competitor_id']
winner_by_round = comp_by_round[(comp_by_round['competitor_id'].isin(winner_ids))]

winner_agg = comp_by_round[['season',
'episode',
'competitor_id',
'competitor',
'gender','ending_funds']].loc[(comp_by_round['winner_binary'] == True)]

winner_agg['money_spent'] = 25000 - winner_agg['ending_funds']



print(winner_by_round.shape,winner_agg.shape)


# %%
