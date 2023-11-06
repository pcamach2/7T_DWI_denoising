import pandas as pd
import matplotlib.pyplot as plt


def plot_runtimes(filepath):
    df = pd.read_csv(filepath, header=None, names=['Participant ID','Run Time (s)','CPU Time','Threads','Memory (GB)','N_Jobs','Volumes Denoised','Method'])
    volumes = df['Volumes Denoised'].unique()
    methods = df['Method'].unique()
    fig, ax = plt.subplots(figsize=(10, 6))
    for participant in df['Participant ID'].unique():
        for volume in volumes:
            for method in methods:
                data = df[(df['Participant ID'] == participant) & (df['Volumes Denoised'] == volume) & (df['Method'] == method)]
                if method == 'patch2self':
                    ax.plot(data['N_Jobs'], data['Run Time (s)'], 'o', markersize=10, label=f'{volume} {method}')
                else:
                    ax.plot(data['N_Jobs'], data['Run Time (s)'], label=f'{volume} {method}')
    ax.set_xlabel('N_Jobs')
    ax.set_ylabel('Run Time (s)')
    # plt.subplots_adjust(right=0.8) # adjust the spacing between the subplots
    ax.xaxis.set_major_locator(plt.MaxNLocator(integer=True)) # set x-axis ticks to integer values
    # add a label on the plot for 'Volumes Denoised'=60 and 'Volumes Denoised'=128
    ax.text(0.5, 0.08, 'Volumes Denoised=60', horizontalalignment='center', verticalalignment='center', transform=ax.transAxes)
    # for each value of N_Jobs, calculate the range of the y-axis values for all Volumes Denoised
    y_range = df.groupby('N_Jobs')['Run Time (s)'].max() - df.groupby('N_Jobs')['Run Time (s)'].min()
    # plot the y_range array as a curved line
    ax.plot(y_range * 0.85, color='grey', linestyle='dashed')
    ax.text(0.5, 0.15, 'Volumes Denoised=128', horizontalalignment='center', verticalalignment='center', transform=ax.transAxes) 
    # add a title   
    ax.set_title('Run Time vs. Value of n_jobs for Patch2Self and Patch2Self Parallel')
    plt.show()

plot_runtimes('time.csv')
