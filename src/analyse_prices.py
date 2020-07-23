# grafics: try bib: seaborn
# hardcodierter preissegmente median und teilmedian raussuchen???

import pandas as pd

amazon_path = './dummy_data/amazon.csv'
toysff_path = './dummy_data/toysforfun.csv'


def main():
    amazon_data = pd.read_csv(amazon_path, header=None, sep=';', names=['article_nr', 'subbrand', 'amazon_price', 'amazon_name'], encoding='utf-16')
    toys_data = pd.read_csv(toysff_path, header=None, sep=';', names=['article_nr', 'subbrand', 'toysff_price', 'toysff_amazon_name'], encoding='utf-16')
    comparable_data = pd.merge(amazon_data, toys_data, how='inner')
    print(comparable_data)


if __name__ == '__main__':
    main()
