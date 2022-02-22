####Importing Packages
# %%
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


#### Making a box plot of auction_data
# %%

auction_data.groupby('sabotage_type').agg(
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

# %%
