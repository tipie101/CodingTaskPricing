import pandas as pd
import pickle

# betterto convert it into csv here and then hand it to price analysis via pickle
scraped_data = pickle.load(open('./data/toysff.p', 'rb'))
df = pd.DataFrame(scraped_data)
print(df)
