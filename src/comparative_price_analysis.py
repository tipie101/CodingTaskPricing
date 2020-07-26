import amazon_crawler
import argparse
import pandas as pd
import pickle
import lego_pricing_crawler
import matplotlib.pyplot as plt
import seaborn as sns


price_segments_borders = [0, 40, 80, 120]

def price_seg(price_added):
    for x in reversed(range(len(price_segments_borders))):
        if price_added >= price_segments_borders[x]:
            return x
    # Error: negative price
    return -1

def basic_compare(path1, path2, prefix1, prefix2):
    price1 = prefix1 + '_price' 
    price2 = prefix2 + '_price'
    scraped_data_1 = pickle.load(open(path1, 'rb'))
    df1 = pd.DataFrame(scraped_data_1).rename(columns={'price': price1, 'name': prefix1 + '_name'})

    scraped_data_2 = pickle.load(open(path2, 'rb'))
    df2 = pd.DataFrame(scraped_data_2).rename(columns={'price': price2, 'name': prefix2 + '_name'})
    
    df = df1.merge(df2, how='inner')
    # Some articles appear several time within the amazon-store
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

def output_diff_by_category(data, category, diff_type, csv=False):
    print(diff_type + ' (toysff - amazon)')
    diff = data[[category, diff_type]].groupby([category])[diff_type].agg(['mean', 'count'])
    print(diff)
    diff = diff.reset_index()
    if csv:
        output_as_csv(diff, './output/' + category + '_' + diff_type + '.csv')

def main(args):

    df, info = basic_compare('./data/toysff.p', './data/amazon.p', 'toysff', 'amazon')
    output_as_csv(df, './output/price_differences.csv')
 
    # prepare data for bar plot 
    df = df.rename(columns={'toysff_name': 'name'})
    df_amazon = df.drop(['amazon_name', 'toysff_price'], 1).rename(columns={'amazon_price': 'price'})
    df_toysff = df.drop(['amazon_name', 'amazon_price'], 1).rename(columns={'toysff_price': 'price'})
    df_amazon['src'] = ['amazon'] * df_amazon['article_nr'].count()
    df_toysff['src'] = ['toys for fun'] * df_toysff['article_nr'].count()
    result = pd.concat([df_amazon, df_toysff])
    print(result)
    pickle.dump(result, open('./data/comparison_amazon_toysff', 'wb'))
    if args.csv:
        output_as_csv(result, './output/comparison_amazon_toysff.csv')

    # data for subbrand plot
    subbrand_data = result[['subbrand', 'src', 'price']]
    subbrand_aggregated = subbrand_data.groupby(['subbrand', 'src'])['price'].agg(['sum', 'count', 'mean'])
    subbrand_aggregated = subbrand_aggregated.reset_index()
    
    # data for price segment plot
    segment_data = result[['price_segment', 'src', 'price']]
    segment_aggregated = segment_data.groupby(['price_segment', 'src'])['price'].agg(['sum', 'count', 'mean'])
    segment_aggregated = segment_aggregated.reset_index()

    # for the correct count- and sum-aggregation we need to drop duplicates
    # all values below are the same for 'src=amazon' and 'src=toysff'
    result_single = result[['article_nr', 'subbrand', 'price_segment', 'diff_abs', 'diff_%']].drop_duplicates()
    
    # Output on console and to csv if set true
    output_diff_by_category(result_single, 'subbrand', 'diff_abs', args.csv)
    output_diff_by_category(result_single, 'subbrand', 'diff_%', args.csv)
    output_diff_by_category(result_single, 'price_segment', 'diff_abs', args.csv)
    output_diff_by_category(result_single, 'price_segment', 'diff_%', args.csv)

    if args.plot:
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

    print('Main Statistics: ')
    print(info)


parser = argparse.ArgumentParser(description='Comparison of Lego Pricing (Amazon vs. ToysForFun)')
parser.add_argument('--csv', default=False, dest='csv', action='store_true', help='output the price comparisons as csv')
parser.add_argument('--no-plot', default=True, dest='plot', action='store_false', help='skip the plots')


if __name__ == '__main__':
    main(parser.parse_args())
