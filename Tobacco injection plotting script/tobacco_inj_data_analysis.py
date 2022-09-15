# %%
import pandas as pd
import matplotlib.pyplot as plt
from scipy import stats
import scikit_posthocs as sp
from scipy.stats import f_oneway
from statsmodels.stats.multicomp import pairwise_tukeyhsd
import seaborn as sns

plt.rcParams.update({'font.size':20})


# takes in list of raw platereader output dfs and takes the median yfp, rfp intensities
# per well and creates merged lists of all intensity valuesthrough all the experiments. 
# Then divides the values to get median ratiometric intensities
# returns median per well yfp, rfp, and ratiometric fluorescence by for all experiments
def process_raw_data(data_list):
    data_yfp = []
    data_rfp = []
    yfp_med_per_exp = []
    rfp_med_per_exp = []
    ratio_med_list = []
    # take subset of excel sheet that contains yfp and rfp measurements
    for i in data_list:
        data_yfp_temp = i.loc[51:62]
        data_rfp_temp = i.loc[95:106]
        # calculate median per well for yfp measurement
        for col in data_yfp_temp.columns:
            yfp_med_per_well = data_yfp_temp[col].median()
            yfp_med_per_exp.append(yfp_med_per_well)
        # calculate median per well for rfp measurement
        for col in data_rfp_temp.columns:
            rfp_med_per_well = data_rfp_temp[col].median()
            rfp_med_per_exp.append(rfp_med_per_well)
    # calculate ratiometric fluorescence
    for i in range(0, len(yfp_med_per_exp)):
        ratio_med_list.append(yfp_med_per_exp[i] / rfp_med_per_exp[i])

    return yfp_med_per_exp, rfp_med_per_exp, ratio_med_list


# input list of construct names and get ANOVA stats output
# prints one way F test results and tukeys test table
# returns tuple containing oneway F test and Tukey post-hoc correction results
def getStats(construct_list):

    anova_list = []
    str_list = []
    for i in construct_list:
        ind = construct_dict.get(i)
        anova_list.append(ratio_vals[ind])
        # str_list.append(f'{construct_list[i][0]}'.split(',')[0])
    print('ONE WAY F TEST RESULT:', f_oneway(*anova_list))
    stats_df = med_intensity_data.loc[med_intensity_data['Construct'].isin(construct_list)]
    tukey_test = pairwise_tukeyhsd(endog=stats_df['Intensity Ratio'].astype('float'),
                          groups=list(stats_df['Construct']),
                          alpha=0.05)
    print()
    print('TUKEY CORRECTION COMPARISONS:')
    print(tukey_test)
    return f_oneway(*anova_list), tukey_test


# function to make boxplots of each set of tobacco injection data
# reads in dataset to plot, figure size, construct order (order to plot from left to right) 
# and filename (path to which to save the generated plot)
def plot_data(dataset, figuresize, construct_order, filename):
    fig, ax = plt.subplots(figsize=(figuresize, 8))
    ax = sns.boxplot(x = 'Construct', y='Intensity Ratio', hue = 'Experiment', data = dataset, 
    palette='Greys', width=0.7, order=construct_order, boxprops={'alpha':0.4}, showfliers=False)
    handles, labels = ax.get_legend_handles_labels()
    sns.stripplot(x = 'Construct', y='Intensity Ratio', hue = 'Experiment', data = dataset, jitter=True, 
    palette='Greys', dodge = True, linewidth = 1, s=4, order=construct_order, ax=ax)
    ax.legend().set_visible(False)
    ax.figure.savefig(filename, bbox_inches='tight')


# read in all raw platereader fluorescence measurement data (example in github repo)
# replace with the path to your data, copy the line as many times as data files you have 
data1 = pd.read_excel(r'path to your platereader data', usecols="B:CS")


# combine all platereader data outputs as one list
# fill in list with variables above of platereader output dataframes
# copy line for as many data files you have
raw_data_list = []

# read in all 96 well plate data layout files
# replace with your data layout file (example in github repo)
# copy line for as many data files you have
data_layout1 = pd.read_csv(r'path to data layout file')

# combine all layouts into one list
# fill in list with your layout dataframes
layout_list = []

# calculate median values per well for entire data list
med_per_exp = process_raw_data(raw_data_list)

# merge all layouts into one df, then add calculated median intensity per well data as new column
layout_merged_df = pd.DataFrame()
for i in layout_list:
    layout_merged_df = pd.concat([layout_merged_df, i,], axis = "rows")
layout_merged_df.insert(4, "YFP Intensity", med_per_exp[0])
layout_merged_df.insert(5, "RFP Intensity", med_per_exp[1])
layout_merged_df.insert(6, "Intensity Ratio", med_per_exp[2])

# drop any row with NA values (corresponding to unused wells)
med_intensity_data = layout_merged_df.dropna()

# changes float values for these constructs into string to be consistent with the rest of the data
med_intensity_data.replace(439.0, '439', inplace=True)
med_intensity_data.replace(440.0, '440', inplace=True)
med_intensity_data.replace(472.0, '472', inplace=True)
med_intensity_data.replace(473.0, '473', inplace=True)

# make an ordered list of constructs to iterate over
construct_list = ['P1', 'P2', 'P4', 'P5', 'P16', 'P17', 'P18', 'P19', 'P22', 'P23', 'P24', 'P25', 'P27', 'P46', 'P47', 'P56', 
'439', '440', '472', '473', '294arf', '277']
# map construct name to index
construct_dict = {'P1':0, 'P2':1, 'P4':2, 'P5':3, 'P16':4, 'P17':5, 'P18':6, 'P19':7, 'P22':8, 'P23':9, 'P24':10, 'P25':11, 'P27':12, 
'P46':13, 'P47':14, 'P56':15, '439':16, '440':17, '472':18, '473':19, '294arf':20, '277':21}

# makes a list of lists (ratio_vals) where each list is all the median ratiometric intensities for a construct
# in order of the construct_list above
ratio_vals = []
for i in construct_list:
    ratio_vals_temp = []
    for ind, row in med_intensity_data.iterrows():
        if row['Construct'] == i:
            ratio_vals_temp.append(row['Intensity Ratio'])
    ratio_vals.append(ratio_vals_temp)

# example of running statistical analysis for group of pPP2AA3 constructs
getStats(['P1', 'P2', 'P4', 'P5'])

# subset pooled data into different dataframes for generating the separate plots
main_tuning = med_intensity_data[med_intensity_data.Construct.isin(['P27', 'P46', 'P47', 'P56', 
'294', 277.0, '277'])==False]
term_tuning = med_intensity_data[med_intensity_data.Construct.isin(['P1', 'P2', 'P46', 'P47', '294arf'])]
ub_tuning = med_intensity_data[med_intensity_data.Construct.isin(['P23', 'P27', 'P56', '294arf'])]

# plot and save main tuning data
plot_data(main_tuning, 30, ['P1', 'P2', 'P4', 'P5', 'P16', 'P17', 'P18', 'P19', 'P22', 'P23', 'P24', 'P25', '294arf'],
"path where you want to save plot")

# plot and save terminator tuning data
plot_data(term_tuning, 10, ['P1', 'P2', 'P46', 'P47', '294arf'],
"path where you want to save plot")

# plot and save ub tuning data
plot_data(ub_tuning, 8, ['P23', 'P27', 'P56', '294arf'],
"path where you want to save plot")

# %%
