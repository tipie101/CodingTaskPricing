# pandas two approaches: table with redundant info (easier to plot) versus merged rows

# grafics: try bib: seaborn
# hardcodierter preissegmente median und teilmedian raussuchen???
# todo: gesamten datenflow automatisieren mit parse_args

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

amazon_path = './dummy_data/amazon.csv'
toysff_path = './dummy_data/toysforfun.csv'


def main():
    amazon_data = pd.read_csv(amazon_path, header=None, sep=';', names=['article_nr', 'subbrand', 'amazon_price', 'amazon_name'], encoding='utf-16')
    toys_data = pd.read_csv(toysff_path, header=None, sep=';', names=['article_nr', 'subbrand', 'toysff_price', 'toysff_amazon_name'], encoding='utf-16')
    # produce two tables: 1. merged rows table, 2. combined table 
    df = amazon_data.merge(toys_data, how='inner')
    df['diff_abs'] = df['toysff_price'] - df['amazon_price'] 
    df['diff_%'] = 100 * df['diff_abs'] / df['toysff_price']
    # compare prices - output: #articles, abs diff, avg diff, diff%, avg diff%
    avg_diff = df['diff_abs'].mean()
    avg_diff_percent = df['diff_%'].mean()
    diff_percent = (df['toysff_price'].sum() - df['amazon_price'].sum()) / df['toysff_price'].sum()


    # add types for merging / use the base data again?
    amazon_data = amazon_data.iloc[:, :-1][amazon_data['article_nr'].isin(df['article_nr'])]
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


if __name__ == '__main__':
    main()
