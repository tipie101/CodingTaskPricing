# grafics: try bib: seaborn
# hardcodierter preissegmente median und teilmedian raussuchen???
import pandas as pd

amazon_path = './dummy_data/amazon.csv'
toysff_path = './dummy_data/toysforfun.csv'


def main():
    amazon_data = pd.read_csv(amazon_path, header=None, sep=';', names=['article_nr', 'subbrand', 'amazon_price', 'amazon_name'], encoding='utf-16')
    toys_data = pd.read_csv(toysff_path, header=None, sep=';', names=['article_nr', 'subbrand', 'toysff_price', 'toysff_amazon_name'], encoding='utf-16')
    df = amazon_data.merge(toys_data, how='inner').set_index('article_nr')
    df['diff_abs'] = df['toysff_price'] - df['amazon_price'] 
    df['diff_%'] = 100 * df['diff_abs'] / df['toysff_price']
    # compare prices - output: #articles, abs diff, avg diff, diff%, avg diff%
    avg_diff = df['diff_abs'].mean()
    avg_diff_percent = df['diff_%'].mean()
    diff_percent = (df['toysff_price'].sum() - df['amazon_price'].sum()) / df['toysff_price'].sum()


if __name__ == '__main__':
    main()
