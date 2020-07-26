# pandas two approaches: table with redundant info (easier to plot) versus merged rows

# grafics: try bib: seaborn
# hardcodierter preissegmente median und teilmedian raussuchen???
# todo: gesamten datenflow automatisieren mit parse_args

import pandas as pd
import pickle
import matplotlib.pyplot as plt
import seaborn as sns

def basic_compare(path1, path2, prefix1, prefix2, filter=None):
    price1 = prefix1 + '_price' 
    price2 = prefix2 + '_price'
    scraped_data_1 = pickle.load(open(path1, 'rb'))
    df1 = pd.DataFrame(scraped_data_1).rename(columns={'price': price1, 'name': prefix1 + '_name'})
    if filter:
        # filter by subbrand and/or price_segment
        df1 = filter(df1)

    scraped_data_2 = pickle.load(open(path2, 'rb'))
    df2 = pd.DataFrame(scraped_data_2).rename(columns={'price': price2, 'name': prefix2 + '_name'})
    
    # produce two tables: 1. merged rows table, 2. combined table 
    # reconstruct the subbrands!!!
    df = df1.merge(df2, how='inner')
    df['diff_abs'] = df[price1] - df[price2] 
    df['diff_%'] = 100 * df['diff_abs'] / df[price1]

    # compare prices - output: #articles, abs diff, avg diff, diff%, avg diff%
    avg_diff = df['diff_abs'].mean()
    avg_diff_percent = df['diff_%'].mean()
    diff_percent = (df[price1].sum() - df[price2].sum()) / df[price1].sum()

    print(avg_diff, avg_diff_percent, diff_percent)
    print(len(df.article_nr.unique()))

    return df.drop_duplicates(subset=df.columns.difference([prefix2 + '_name']))

def output_as_csv(df, name):
    df.to_csv(name, index = False)

def main():
    df = basic_compare('./data/toysff.p', './data/amazon.p', 'toysff', 'amazon')
    output_as_csv(df, './output/price_differences.csv')
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
