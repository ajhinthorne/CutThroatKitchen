####Importing Packages
# %%
from itertools import count
import pandas as pd
import math as m
import numpy as np
import matplotlib.pyplot as plt



###Importing Datasets
comp_by_round = pd.read_csv('C:/Users/Adam Hinthorne/Documents/CutThroatKitchenLocal/CutThroatKitchen/Competitor By Round.csv')
competitor_agg = pd.read_csv('C:/Users/Adam Hinthorne/Documents/CutThroatKitchenLocal/CutThroatKitchen/Competitor Agg.csv')
sabotages_desc_agg = pd.read_csv('C:/Users/Adam Hinthorne/Documents/CutThroatKitchenLocal/CutThroatKitchen/Sabotage Desc Agg.csv')
sabotages_type_agg = pd.read_csv('C:/Users/Adam Hinthorne/Documents/CutThroatKitchenLocal/CutThroatKitchen/Sabotage Type Agg.csv')
auction_data = pd.read_csv('C:/Users/Adam Hinthorne/Documents/CutThroatKitchenLocal/CutThroatKitchen/Auction Data.csv')
sabotage_data = pd.read_csv('C:/Users/Adam Hinthorne/Documents/CutThroatKitchenLocal/CutThroatKitchen/sabotage_data.csv')

### How many sabotages does it take to be eliminated?
# %%
comp_by_round.groupby(['eliminated','round']).agg(
    money_spent = pd.NamedAgg(column = 'auction_money_spent', aggfunc = np.mean),
    auctions_won = pd.NamedAgg(column = 'auctions_won', aggfunc = np.mean),
    sabotages_received = pd.NamedAgg(column = 'total_sabotages_received', aggfunc = np.mean)
)

comp_by_round.groupby(['round','total_sabotages_received','eliminated']).agg(
    elimination = pd.NamedAgg(column = 'competitor_id', aggfunc = 'count')
)

#### Making a box plot of auction_data
# %%

auction_data.groupby('sabotage_type').agg(
    avg_winning_bid = pd.NamedAgg(column='winning_bid', aggfunc = np.mean),
    min_winning_bid = pd.NamedAgg(column='winning_bid', aggfunc = min),
    max_winning_bid = pd.NamedAgg(column='winning_bid', aggfunc = max)
)

auction_data.groupby(['sabotage_type','round']).agg(   
    count_winning_bid = pd.NamedAgg(column = 'winning_bid', aggfunc = 'count'),
    avg_winning_bid = pd.NamedAgg(column='winning_bid', aggfunc = np.mean),
    min_winning_bid = pd.NamedAgg(column='winning_bid', aggfunc = min),
    max_winning_bid = pd.NamedAgg(column='winning_bid', aggfunc = max)
)

# %%

auction_data.groupby('round').agg(
    avg_winning_bid = pd.NamedAgg(column='winning_bid', aggfunc = np.mean),
    min_winning_bid = pd.NamedAgg(column='winning_bid', aggfunc = min),
    max_winning_bid = pd.NamedAgg(column='winning_bid', aggfunc = max)
)



auction_data_by_round = [auction_data[auction_data['round'] == 1]['winning_bid'],auction_data[auction_data['round'] == 2]['winning_bid'],auction_data[auction_data['round'] == 3]['winning_bid']]





# %%
