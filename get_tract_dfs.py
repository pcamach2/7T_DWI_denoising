import os
import pandas as pd
from scipy.stats import ttest_rel
from matplotlib import pyplot as plt
import seaborn as sns
from scipy import stats

def run_tract_diffs(autotrack_dir):
    # Read in the four csv files with the column names as the first row
    df1 = pd.read_csv(os.path.join(autotrack_dir, 'autotrack_lpca.csv'), header=0)
    df2 = pd.read_csv(os.path.join(autotrack_dir, 'autotrack_mppca.csv'), header=0)
    df3 = pd.read_csv(os.path.join(autotrack_dir, 'autotrack_nlmeans.csv'), header=0)
    df4 = pd.read_csv(os.path.join(autotrack_dir, 'autotrack_p2s.csv'), header=0)

    # Check that all dataframes have the same number of columns
    if not all(len(df.columns) == len(df1.columns) for df in [df2, df3, df4]):
        raise ValueError("All dataframes must have the same number of columns")

    # Add a column to each dataframe indicating the denoiser csv file
    df1['denoiser'] = 'lpca'
    df2['denoiser'] = 'mppca'
    df3['denoiser'] = 'nlmeans'
    df4['denoiser'] = 'p2s'

    # Concatenate the four dataframes into one
    df = pd.concat([df1, df2, df3, df4])

    # Group the dataframe by bundle_name
    grouped = df.groupby('bundle_name')

    # Loop through each unique bundle_name and perform paired t-tests on the column values
    # with pairs based on "subject_id" and "denoiser", only running the t-test if there are
    # numeric values in the column of interest. Save these to a new dataframe and write the
    # dataframe to a csv file.

    # Define the list of column names to loop through
    column_names = ['number_of_tracts', 'mean_length_mm', 'span_mm', 'curl', 'elongation', 
                    'diameter_mm', 'volume_mm3', 'trunk_volume_mm3', 'branch_volume_mm3', 
                    'total_surface_area_mm2', 'total_radius_of_end_regions_mm', 
                    'total_area_of_end_regions_mm2', 
                    'irregularity', 'area_of_end_region_1_mm2', 'radius_of_end_region_1_mm', 
                    'irregularity_of_end_region_1', 'area_of_end_region_2_mm2', 
                    'radius_of_end_region_2_mm', 'irregularity_of_end_region_2', 
                    'qa', 'dti_fa', 'rd1', 
                    'rd2', 'ha', 'md', 'ad', 'rd', 'gfa', 'iso', 'rdi']

    # Create an empty dataframe to store the results
    results_df = pd.DataFrame()

    # drop the following columns: session_id,task_id,dir_id,acq_id,space_id,rec_id,run_id,
    df = df.drop(columns=['session_id', 'task_id', 'dir_id', 'acq_id', 'space_id', 'rec_id', 'run_id'])

    # clean nan values from the dataframe
    df_nonan = df.dropna()
    # save the dataframe with no nan values to a csv file
    df_nonan.to_csv(os.path.join(autotrack_dir, 'autotrack_cleaned.csv'), index=False)

    # print a list of bundle names with no nan values
    no_nan_bundle_names = df_nonan['bundle_name'].unique()
    print(no_nan_bundle_names, file=open(os.path.join(autotrack_dir, 'bundle_names_no_nan.txt'), 'w'))

    # print a list of bundle names with nan values
    nan_bundle_names = df['bundle_name'].unique()
    print(nan_bundle_names, file=open(os.path.join(autotrack_dir, 'bundle_names_with_nan.txt'), 'w'))

    # Loop through each column name
    for column_name in column_names:
        # Loop through each unique value of 'denoiser'
        for denoiser in df['denoiser'].unique():
            # Create an empty dataframe to store the results for the current denoiser
            denoiser_results_df = pd.DataFrame()
            # Loop through each bundle_name
            for name, group in grouped:
                # Get the dataframe for the current bundle_name and denoiser
                bundle_df = grouped.get_group(name)
                # write the bundle dataframe to a csv file
                bundle_df.to_csv(os.path.join(autotrack_dir, 'bundle_dfs', f'{name}.csv'), index=False)
