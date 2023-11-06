import pandas as pd
import os

def process_autotrack_csvs(csvs_dir):
    # Define the four methods as a list
    methods = ['p2s', 'nlmeans', 'lpca', 'mppca']

    # Create empty dataframes to store the DSI Studio Autotrack csv data for each method
    df_p2s = pd.DataFrame()
    df_nlmeans = pd.DataFrame()
    df_lpca = pd.DataFrame()
    df_mppca = pd.DataFrame()

    # Loop through each method in the list of methods
    for method in methods:
        # Define the path to the directory for the current method
        method_dir = os.path.join(csvs_dir, f'CUPS_{method}', 'bids', 'derivatives', 'qsirecon')
        
        # Loop through each subject in the directory
        for subject in os.listdir(method_dir):
            # skip_subs = ['sub-CUPS059', 'sub-CUPS067', 'sub-CUPS018', 'sub-CUPS017']
            skip_subs = []
            # Check if the subject is a directory and not an html file
            if os.path.isdir(os.path.join(method_dir, subject)) and 'log' not in subject and subject not in skip_subs:
                # Get the ID number of the subject
                subject_id = int(subject[-3:])
                
                # Define the path to the directory for the current subject
                subject_dir = os.path.join(method_dir, subject, 'ses-A', 'dwi')
                
                # Define the path to the DSI Studio Autotrack csv file for the current subject and session
                autotrack_file = os.path.join(subject_dir, f'{subject}_ses-A_run-1_space-T1w_desc-preproc_AutoTrackGQI.csv')
                
                # Read the csv file into a pandas dataframe
                autotrack_df = pd.read_csv(autotrack_file)
                
                # Add a column to the dataframe to store the method name
                autotrack_df['method'] = method
                
                # Concatenate the dataframe to the appropriate dataframe based on the method name
                if method == 'p2s':
                    df_p2s = pd.concat([df_p2s, autotrack_df], ignore_index=True)
                elif method == 'nlmeans':
                    df_nlmeans = pd.concat([df_nlmeans, autotrack_df], ignore_index=True)
                elif method == 'lpca':
                    df_lpca = pd.concat([df_lpca, autotrack_df], ignore_index=True)
                elif method == 'mppca':
                    df_mppca = pd.concat([df_mppca, autotrack_df], ignore_index=True)

    # Save the dataframes as csv files
    df_p2s.to_csv(os.path.join(csvs_dir, 'autotrack_p2s.csv'), index=False)
    df_nlmeans.to_csv(os.path.join(csvs_dir, 'autotrack_nlmeans.csv'), index=False)
    df_lpca.to_csv(os.path.join(csvs_dir, 'autotrack_lpca.csv'), index=False)
    df_mppca.to_csv(os.path.join(csvs_dir, 'autotrack_mppca.csv'), index=False)

if __name__ == '__main__':
    # Define the path to the directory containing the DSI Studio Autotrack csv files
    csvs_dir = '/datain/CUPS/derivatives/qsirecon'
    
    # Process the DSI Studio Autotrack csv files
    process_autotrack_csvs(csvs_dir)
