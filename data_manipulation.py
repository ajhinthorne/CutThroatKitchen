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

winner_by_round[['competitor_id','total_sabotages_received']].groupby(['competitor_id']).sum()

print(winner_by_round.shape,winner_agg.shape)


###To Filter use the format df[df['column'] == logic]['target_columns']
###To join datasets use the merge function - merge(adf,bdf,how='left',on='foreign_key')
###To rename columns - df.rename(columns={'target_column':'target_column_new_name'},inplace=True)
###Use the agg function to aggregate multiple things in the groupby 

# %%
competitor_agg = comp_by_round[['competitor_id','round']].groupby(['competitor_id']).count()
competitor_agg = competitor_agg.reset_index()

### Summary Statistics on Winners
competitor_info = comp_by_round[comp_by_round['round'] == 1 ][['competitor_id','competitor','season','episode','gender']]
competitor_info['winner'] = np.where(competitor_info['competitor_id'].isin(winner_ids),True,False)

competitor_agg = competitor_info.merge(competitor_agg,how='left',on='competitor_id')
competitor_agg.rename(columns={'round':'number_of_rounds'},inplace=True)

### Summary Statistics on Ending Funds
competitor_agg = competitor_agg.merge(
comp_by_round[(comp_by_round['eliminated'] == True) | (comp_by_round['winner_binary'] == True) ][['competitor_id','ending_funds']],
how = 'left',
on = 'competitor_id')

### Summary statistics on Auctions
competitor_agg = competitor_agg.merge(
comp_by_round[['competitor_id','auction_money_spent','auctions_won','total_sabotages_received']].groupby('competitor_id').agg(
    total_auction_money_spent = pd.NamedAgg(column='auction_money_spent',aggfunc = sum),
    total_sabotages_given = pd.NamedAgg(column='auctions_won',aggfunc = sum),
    total_sabotages_received = pd.NamedAgg(column='total_sabotages_received',aggfunc = sum)).reset_index(),
how='left',on='competitor_id')

#### checking to make sure there are not any records that don't add up to 25000
competitor_agg[(competitor_agg['ending_funds'] + competitor_agg['total_auction_money_spent'] != 25000)]

# %%
