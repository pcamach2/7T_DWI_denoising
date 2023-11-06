import pandas as pd
import seaborn as sns
import os
import sys
import matplotlib.pyplot as plt

bundles_path = sys.argv[1]

def plot_distribution(filepath, column='dti_fa', bundles_path=bundles_path):
    """
    Plots the distribution of a given column in a CSV file.

    Args:
        filepath (str): The path to the CSV file.
        column (str, optional): The column to plot the distribution of. Defaults to 'dti_fa'.
        bundles_path (str, optional): The path to save the output plots. Defaults to bundles_path.

    Returns:
        None
    """
def plot_distribution(filepath, column='dti_fa', bundles_path=bundles_path):
    # Read in data
    df = pd.read_csv(filepath)

    # Create four groups based on unique values of 'method'
    groups = df['method'].unique()

    # Create a color palette for the groups
    palette = sns.color_palette('husl', len(groups))

    # get bundle name
    bundle = df['bundle_name'].unique()[0]

    # change subject_id to a column of integers
    df['subject_id'] = df['subject_id'].str.replace('sub-CUPS', '').astype(int)

    # make a separate dataframe for subject_id values less than 40
    df1 = df[df['subject_id'] < 40]
    # make a separate dataframe for subject_id values greater than 40
    df2 = df[df['subject_id'] > 40]
    # clean text for bundle name, column name, and method name to capitalize first letter, replace underscores with spaces
    bundle_txt = bundle.replace('_', ' ').capitalize()
    # if bundle name ends in _L or _R or one of these with an integer, change to ' Left' or ' Right' and the integer
    if bundle_txt.endswith(' l') or bundle_txt.endswith(' r'):
        bundle_txt = bundle_txt[:-2] + ' ' + bundle_txt[-1].upper()
    elif bundle_txt.endswith(' l1') or bundle_txt.endswith(' r1'):
        bundle_txt = bundle_txt[:-3] + ' ' + bundle_txt[-2].upper() + bundle_txt[-1]
    elif bundle_txt.endswith(' l2') or bundle_txt.endswith(' r2'):
        bundle_txt = bundle_txt[:-3] + ' ' + bundle_txt[-2].upper() + bundle_txt[-1]
    elif bundle_txt.endswith(' l3') or bundle_txt.endswith(' r3'):
        bundle_txt = bundle_txt[:-3] + ' ' + bundle_txt[-2].upper() + bundle_txt[-1]
    elif bundle_txt.endswith(' l4') or bundle_txt.endswith(' r4'):
        bundle_txt = bundle_txt[:-3] + ' ' + bundle_txt[-2].upper() + bundle_txt[-1]
    column_txt = column.replace('_', ' ').capitalize()
    if column in ['dti_fa', 'md', 'ad', 'rd']:
        column_txt = column_txt.upper()
    # create a Method column with the method name in all caps
    df1['Method'] = df1['method'].str.upper()
    df2['Method'] = df2['method'].str.upper()
    # unless it is 'p2s' which should be 'Patch2Self'
    df1.loc[df1['Method'] == 'P2S', 'Method'] = 'Patch2Self'
    df2.loc[df2['Method'] == 'P2S', 'Method'] = 'Patch2Self'
    # set plot size to 10 inches wide and 8 inches tall
    plt.figure(figsize=(10, 8))
    # set font size to 15
    plt.rcParams.update({'font.size': 12})
    # Create a distribution plot with color labeled distributions of values of the given column and save to file
    sns.displot(data=df1, x=column, hue='Method', kind='kde', palette=palette)
    # change x-axis label to value in column_txt
    plt.xlabel(column_txt)
    # add title to plot with bundle name and column
    plt.title(f'{bundle_txt} {column_txt}: 30d/shell data', pad=20)
    plt.savefig(f'{bundles_path}/{bundle}_{column}_distribution_60d.png', bbox_inches='tight')
    plt.clf()
    # set plot size to 10 inches wide and 8 inches tall
    plt.figure(figsize=(10, 8))
    # set font size to 15
    plt.rcParams.update({'font.size': 12})
    sns.displot(data=df2, x=column, hue='Method', kind='kde', palette=palette)
    # change x-axis label to value in column_txt
    plt.xlabel(column_txt)
    # add title to plot with bundle name and column
    plt.title(f'{bundle_txt} {column_txt}: 64d/shell data', pad=20)
    plt.savefig(f'{bundles_path}/{bundle}_{column}_distribution_128d.png', bbox_inches='tight')
    plt.clf()

# Get a list of all csv files in the directory
csv_files = [f for f in os.listdir(bundles_path) if f.endswith('.csv')]

# Loop through each csv file and call plot_distribution for each column
for csv_file in csv_files:
    filepath = os.path.join(bundles_path, csv_file)
    plot_distribution(filepath, column='dti_fa', bundles_path=bundles_path)
    plot_distribution(filepath, column='curl', bundles_path=bundles_path)
    plot_distribution(filepath, column='mean_length_mm', bundles_path=bundles_path)
    plot_distribution(filepath, column='diameter_mm', bundles_path=bundles_path)
    plot_distribution(filepath, column='md', bundles_path=bundles_path)
    plot_distribution(filepath, column='rd', bundles_path=bundles_path)
    plot_distribution(filepath, column='ad', bundles_path=bundles_path)
