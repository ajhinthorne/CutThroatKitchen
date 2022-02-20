####Importing Datasets
# %%
from audioop import avg
from statistics import mean
import pandas as pd
import math as m
import numpy as np
import matplotlib.pyplot as plt


###Importing CSV from Github
# %%
comp_by_round = pd.read_csv("https://raw.githubusercontent.com/ajhinthorne/CutThroatKitchen/master/Cutthroat%20Kitchen%20Data%20-%20DataOutput.csv")
comp_by_round.head(5)


###Make sure the names are all lower case
###comp_by_round.rename(columns={'Gender':'gender','Choice Binary':'choice_binary'},inplace = True)

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




### Competitor aggregation: Below is the code that will create a summary of each competitor from our dataset

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
comp_by_round[['competitor_id','auction_money_spent','auctions_won','total_sabotages_received','fines']].groupby('competitor_id').agg(
    total_auction_money_spent = pd.NamedAgg(column='auction_money_spent',aggfunc = sum),
    total_sabotages_given = pd.NamedAgg(column='auctions_won',aggfunc = sum),
    total_sabotages_received = pd.NamedAgg(column='total_sabotages_received',aggfunc = sum),
    total_fines_paid = pd.NamedAgg(column = 'fines',aggfunc = sum)).reset_index(),
how='left',on='competitor_id')

#### checking to make sure there are not any records that don't add up to 25000
competitor_agg[(competitor_agg['ending_funds'] + competitor_agg['total_auction_money_spent'] + competitor_agg['total_fines_paid'] != 25000)]
###Should be none (make sure to add in fines)
###Check for misplaced IDs, Incorrectly assigned eliminations

###Sabotage Aggregation: Below is the code that will aggregate and summarize different sabotages

####To find a unique value use df.column.unique()
###To remove NaN use df.dropna()
###to find whether an item is in a subset of an array use df.isin()
###The rename function automatically renames dataframes without needing to reassign
###To Union all dataframes, use pd.concat()
###To get the number of rows in a dataset, use the first index of pd.shape

# %%
auction1_unique_values = comp_by_round['auction_item1_description'].dropna().unique()

auction1_sabotages = comp_by_round[comp_by_round['auction_item1_description'].isin(auction1_unique_values)][['auction_item1_type','auction_item1_description','auction_item1_winning_bid','round']]
auction1_sabotages.rename(columns={'auction_item1_type':'sabotage_type',
                                                        'auction_item1_description':'sabotage_description',
                                                        'auction_item1_winning_bid':'winning_bid'},inplace=True)


auction2_unique_values = comp_by_round['auction_item2_description'].dropna().unique()

auction2_sabotages = comp_by_round[comp_by_round['auction_item2_description'].isin(auction2_unique_values)][['auction_item2_type','auction_item2_description','auction_item2_winning_bid','round']]
auction2_sabotages.rename(columns={'auction_item2_type':'sabotage_type',
                                                        'auction_item2_description':'sabotage_description',
                                                        'auction_item2_winning_bid':'winning_bid'},inplace=True)


auction3_unique_values = comp_by_round['auction_item3_description'].dropna().unique()

auction3_sabotages = comp_by_round[comp_by_round['auction_item3_description'].isin(auction3_unique_values)][['auction_item3_type','auction_item3_description','auction_item3_winning_bid','round']]
auction3_sabotages.rename(columns={'auction_item3_type':'sabotage_type',
                                                        'auction_item3_description':'sabotage_description',
                                                        'auction_item3_winning_bid':'winning_bid'},inplace=True)

auction4_unique_values = comp_by_round['auction_item4_description'].dropna().unique()

auction4_sabotages = comp_by_round[comp_by_round['auction_item4_description'].isin(auction4_unique_values)][['auction_item4_type','auction_item4_description','auction_item4_winning_bid','round']]
auction4_sabotages.rename(columns={'auction_item4_type':'sabotage_type',
                                                        'auction_item4_description':'sabotage_description',
                                                        'auction_item4_winning_bid':'winning_bid'},inplace=True)

sabotage_raw_data = pd.concat([auction1_sabotages,auction2_sabotages,auction3_sabotages,auction4_sabotages],ignore_index=True)





### The raw data should align with the total auctions won column in comp_by_round
print(sabotage_raw_data.shape[0],comp_by_round[['auctions_won']].sum())


###Now Calculating Sabotages Aggregate Dataset
###can use the function value_counts to count how many times a value appears in a series
###converting a series to a dataframe you can use pandas.series.to_frame()
###Alternatively, use the pd.DataFrame Function
###Here's a way to count and group by values in a dataset: df.groupby(['col1', 'col2']).size().reset_index(name='counts')
# %%
sabotages_received_raw = pd.concat([pd.DataFrame(comp_by_round[['sabotage1_type','sabotage1_description']].dropna().reindex()).rename(columns = {'sabotage1_type':'sabotage_type','sabotage1_description':'sabotage_description'}),
                                pd.DataFrame(comp_by_round[['sabotage2_type','sabotage2_description']].dropna().reindex()).rename(columns = {'sabotage2_type':'sabotage_type','sabotage2_description':'sabotage_description'}),
                                pd.DataFrame(comp_by_round[['sabotage3_type','sabotage3_description']].dropna().reindex()).rename(columns = {'sabotage3_type':'sabotage_type','sabotage3_description':'sabotage_description'})],
                                ignore_index=True)

sabotages_desc_agg = sabotages_received_raw.groupby(['sabotage_description','sabotage_type']).size().reset_index(name='count_received')

sabotages_type_agg = sabotages_received_raw.groupby(['sabotage_type']).size().reset_index(name='count_received')

###Summary statistics on Sabotages
sabotages_desc_agg = sabotages_desc_agg.merge(
    sabotage_raw_data.groupby('sabotage_description').agg(
        min_winning_bid = pd.NamedAgg(column = 'winning_bid',aggfunc = min),
        max_winning_bid = pd.NamedAgg(column = 'winning_bid',aggfunc = max),
        avg_winning_bid = pd.NamedAgg(column = 'winning_bid',aggfunc = np.mean),
        med_winning_bid = pd.NamedAgg(column = 'winning_bid',aggfunc = np.median)
    ).reset_index(),
    how='left',on='sabotage_description'
)

sabotages_type_agg = sabotages_type_agg.merge(
    sabotage_raw_data.groupby('sabotage_type').agg(
        min_winning_bid = pd.NamedAgg(column = 'winning_bid',aggfunc = min),
        max_winning_bid = pd.NamedAgg(column = 'winning_bid',aggfunc = max),
        avg_winning_bid = pd.NamedAgg(column = 'winning_bid',aggfunc = np.mean),
        med_winning_bid = pd.NamedAgg(column = 'winning_bid',aggfunc = np.median)
    ).reset_index(),
    how='left',on='sabotage_type'
)

# %%
