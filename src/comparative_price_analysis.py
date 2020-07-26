# pandas two approaches: table with redundant info (easier to plot) versus merged rows

# grafics: try bib: seaborn
# hardcodierter preissegmente median und teilmedian raussuchen???
# todo: gesamten datenflow automatisieren mit parse_args

import pandas as pd
import pickle
import matplotlib.pyplot as plt
import seaborn as sns


def main():  
    # TODO: In Methode auslagern
    scraped_data_toysff = pickle.load(open('./data/toysff.p', 'rb'))
    toys_data = pd.DataFrame(scraped_data_toysff).rename(columns={'price': 'toysff_price', 'name': 'toysff_name'})

    scraped_data_amazon = pickle.load(open('./data/amazon.p', 'rb'))
    amazon_data = pd.DataFrame(scraped_data_amazon).rename(columns={'price': 'amazon_price', 'name': 'amazon_ifo'})
    
    # produce two tables: 1. merged rows table, 2. combined table 
    # reconstruct the subbrands!!!
    df = amazon_data.merge(toys_data, how='inner')
    df['diff_abs'] = df['toysff_price'] - df['amazon_price'] 
    df['diff_%'] = 100 * df['diff_abs'] / df['toysff_price']
    # compare prices - output: #articles, abs diff, avg diff, diff%, avg diff%
    avg_diff = df['diff_abs'].mean()
    avg_diff_percent = df['diff_%'].mean()
    diff_percent = (df['toysff_price'].sum() - df['amazon_price'].sum()) / df['toysff_price'].sum()
    print(avg_diff, avg_diff_percent, diff_percent)
    print(df)  # TODO: CSV-EXPORT
    print(len(df.article_nr.unique()))
    return
    
    # TODO: 
    # Methode schreiben: 
    # match_dfs() calls 1. filter_pairs(), 2. add_subbrand   





    # add types for merging / use the base data again?
    amazon_data = amazon_data.iloc[:, :-1][amazon_data['article_nr'].isin(df['article_nr'])]

    print('Amazon')
    print(amazon_data)
    return

    toys_data = toys_data.iloc[:, :-1][toys_data['article_nr'].isin(df['article_nr'])]
    amazon_data = amazon_data.rename(columns={'amazon_price': 'price'})
    toys_data = toys_data.rename(columns={'toysff_price': 'price'})
    
    
    amazon_data['src'] = ['amazon'] * amazon_data['article_nr'].count()
    toys_data['src'] = ['toys for fun'] * toys_data['article_nr'].count()

    # print(toys_data)

    result = pd.concat([amazon_data, toys_data])
    print(result)

    g = sns.catplot(x='article_nr', y='price', hue='src', kind='bar', data=result)
    
    plt.show()

    # Idee: die prozentual gesehen stärksten Ausreißer aufführen
    # 1. hübsches feature 
    # 2. hilft dabei fehler zu finden


if __name__ == '__main__':
    main()
