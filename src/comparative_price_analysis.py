# pandas two approaches: table with redundant info (easier to plot) versus merged rows

# grafics: try bib: seaborn
# hardcodierter preissegmente median und teilmedian raussuchen???
# todo: gesamten datenflow automatisieren mit parse_args
import pandas as pd
import pickle
import matplotlib.pyplot as plt
import seaborn as sns


price_segments_borders = [0, 40, 80, 120]

def price_seg(price_added):
    for x in reversed(range(len(price_segments_borders))):
        if price_added >= price_segments_borders[x]:
            return x
    # Error: negative price
    return -1

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
    
    df = df1.merge(df2, how='inner')
    df = df.drop_duplicates(subset=df.columns.difference([prefix2 + '_name']))
    
    df['diff_abs'] = df[price1] - df[price2] 
    # price diff percent in relation to price1
    df['diff_%'] = 100 * df['diff_abs'] / df[price1]
    df['price_segment'] = (df[price1] + df[price2]).apply(price_seg)

    diff = df['diff_abs'].sum()
    avg_diff = df['diff_abs'].mean()
    avg_diff_percent = df['diff_%'].mean()
    diff_percent = (df[price1].sum() - df[price2].sum()) / df[price1].sum()

    return df, {
        'total difference ' + prefix1 + '-' + prefix2: diff, 
        'total differance percent': diff_percent,
        'average diff: ': avg_diff, 
        'average diff percent': avg_diff_percent
    }

def output_as_csv(df, name):
    df.to_csv(name, index = False)

def main():
    df, info = basic_compare('./data/toysff.p', './data/amazon.p', 'toysff', 'amazon')
    output_as_csv(df, './output/price_differences.csv')
    print(info)
 
    # prepare data for bar plot 
    df = df.rename(columns={'toysff_name': 'name'})
    df_amazon = df.drop(['amazon_name', 'toysff_price'], 1).rename(columns={'amazon_price': 'price'})
    df_toysff = df.drop(['amazon_name', 'amazon_price'], 1).rename(columns={'toysff_price': 'price'})
    df_amazon['src'] = ['amazon'] * df_amazon['article_nr'].count()
    df_toysff['src'] = ['toys for fun'] * df_toysff['article_nr'].count()
    result = pd.concat([df_amazon, df_toysff])
    # print(result)
    # pickle.dump(result, open('./data/comparison_amazon_toysff', 'wb'))
    # output_as_csv(result, './output/comparison_amazon_toysff.csv')

    # data for subbrand plot
    subbrand_data = result[['subbrand', 'src', 'price']]
    subbrand_aggregated = subbrand_data.groupby(['subbrand', 'src'])['price'].agg(['sum', 'count', 'mean'])
    subbrand_aggregated = subbrand_aggregated.reset_index()
    
    # data for price segment plot
    segment_data = result[['price_segment', 'src', 'price']]
    segment_aggregated = segment_data.groupby(['price_segment', 'src'])['price'].agg(['sum', 'count', 'mean'])
    segment_aggregated = segment_aggregated.reset_index()

    print(subbrand_aggregated)
    print('absoult difference (toysff - amazon)')
    print(result[['subbrand', 'diff_abs']].drop_duplicates().groupby(['subbrand'])['diff_abs'].agg(['mean', 'count', 'sum']))
    print('percentual difference (toysff - amazon) where 100% ~ toysff')
    print(result[['subbrand', 'diff_%']].drop_duplicates().groupby(['subbrand'])['diff_%'].agg(['mean', 'count', 'sum']))

    # pickle.dump(subbrand_aggregated, open('./data/comparison_amazon_toysff_subbrands', 'wb'))
    # output_as_csv(subbrand_aggregated, './output/comparison_amazon_toysff_subbrands.csv')

    # visualisation subbrands
    sns.set(style="whitegrid")
    sns.catplot(y='subbrand', x='mean', orient='h', height=8, hue='src', kind='bar', data=subbrand_aggregated, aspect=.8)
    plt.title('Subbrands: Average Prices in €')
    plt.tight_layout(pad=1.08, h_pad=None, w_pad=None, rect=None)
    # visualation price_segments
    sns.set(style="whitegrid")
    sns.catplot(y='price_segment', x='mean', orient='h', height=8, hue='src', kind='bar', data=segment_aggregated, aspect=.8)
    plt.title('Price Segments: Average Prices €')
    plt.tight_layout(pad=1.08, h_pad=None, w_pad=None, rect=None)
    
    plt.show()

    # TODO: 
    # develop an entry_point for the tool
    # arg_parser mit params wie --crawl, --export_csv, --analyse_diff, --plot 

if __name__ == '__main__':
    main()
