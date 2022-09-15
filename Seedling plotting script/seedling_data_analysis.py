# %%
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.colors as color
import matplotlib
from scipy import stats
import scikit_posthocs as sp
from scipy.stats import f_oneway
from statsmodels.stats.multicomp import pairwise_tukeyhsd
from itertools import cycle, islice
from itertools import cycle, islice

##############################################################################################
##############################################################################################
#DEFINE FIRST the directory where your files are and where your want to generate your graphs.#
#Those need to be characters"
##############################################################################################
path_to_tuning_data_file=" "
sheet_tuning=" "
path_to_normalized_tuning_data_file=" "
sheet_normalized_tuning=" "
path_to_T2_data_file=" "
sheet_T2_data=" "
path_for_plot= " "
##############################################################################################
##############################################################################################


plt.rcParams.update({'font.size':20})

# function that given a construct name, pulls out numerical form data 
# Ex for L1P1: input is ['L1P1', 0, 0, 2, 12, 16, 30], output is [3, 3, 4, 4, 4, 
# 4, 4, 4, 4, 4, 4, 4, 4, 4, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5]
def anova_array(input_array):
    anova_array = input_array[1]*[1]+input_array[2]*[2]+input_array[3]*[3]+ input_array[4]*[4]+input_array[5]*[5]
    return anova_array

# function to input list of construct names and get ANOVA stats output
# returns tuple containing oneway F test and Tukey post-hoc correction results
def getStats(construct_list):
    anova_list = []
    str_list = []
    for i in range(0, len(construct_list)):
        anova_list.append(anova_array(construct_list[i]))
        str_list.append(f'{construct_list[i][0]}'.split(',')[0])
    print('ONE WAY F TEST RESULT:', f_oneway(*anova_list))
    stats_df = stat_data_df.loc[stat_data_df['Construct'].isin(str_list)]
    tukey_test = pairwise_tukeyhsd(endog=stats_df['switching class'],
                          groups=stats_df['Construct'],
                          alpha=0.05)
    print()
    print('TUKEY CORRECTION COMPARISONS:')
    print(tukey_test)
    return f_oneway(*anova_list), tukey_test

# function for plotting seedling switching data for either constitutive or LR  
# promoter expressed integrase constructs 
def plot_data(plot_info, constructs_to_plot, ylim, filename):
    plt.rcParams.update({'font.size':20})
    matplotlib.rc('font', family='Arial')
  
    plotting_data = plot_info[0].loc[plot_info[0]['Construct'].isin(constructs_to_plot)]
    seedling_nums = plotting_data['total'].values.tolist()
    fig, ax = plt.subplots(figsize=(len(seedling_nums)*1.2, plot_info[1]))
    plotting_data.drop(['total'], axis=1).plot(x='Construct', kind='bar', stacked=True, ax=ax, 
    color = plot_info[2], width=0.65)
    for i in range(len(seedling_nums)):
        plt.text(i, 102, 'n='+str(seedling_nums[i]), ha = 'center')
    ax.set_ylim(0, ylim)
    ax.legend().set_visible(False)
    ax.set_ylabel('Seedling Percentage', fontsize=20)
    ax.set(xlabel=None)
    ax.tick_params(axis='both', which='major', labelsize=20)
    ax.figure.savefig(filename, bbox_inches='tight')

# read in seedling classification data from excel sheet
tuning_data = pd.read_excel(r'path to tuning data file', sheet_name=sheet_tuning, usecols="B:H")
tuning_data_norm = pd.read_excel(r'path to normalized tuning data file', sheet_name=sheet_normalized_tuning, usecols="B:H")
LR_data_norm = pd.read_excel(r'path to T2 data file', sheet_name=sheet_T2_data, usecols="B:F")

# read out all data from df into a big list of lists for easier statistical analysis
arrays_main = tuning_data.values.tolist()

# read constructs out into individual list variables
for i in arrays_main:
    construct = i[0]
    globals()[construct] = i

# dictionary mapping tuning switch level to int values (1=no switch, 5=full switch)
# for ANOVA statistical analysis
tuning_class_dict = {'no switch':1, 'slight':2, 'partial':3, 'strong':4, 'full':5}

# reads all tuning data into an array with each seedling as a row for statistical 
# analysis
# creates individual list variables for each construct (named based on construct name in 
# data excel sheet) which is the numerical array for ANOVA analysis 
# (ex: L1P1 = ['L1P1', 0, 0, 2, 12, 16, 30])
stat_data = []
for index, row in tuning_data.iterrows():
    construct = row[0]
    for i in range(0, 5):
        for k in range(0, row[i+1]):
            stat_data.append([construct, tuning_class_dict.get(tuning_data.columns[i+1])])

# create dataframe from generated array
stat_data_df = pd.DataFrame(stat_data, columns=['Construct', 'switching class'])

# input list of construct names into getStats functionand get ANOVA stats and Tukey post 
# hoc adjustment
# fill in list with construct names (taken from data file) you want to analyze
getStats([])

# create color palette variables for tuning and LR plots
colors_tuning = list(islice(cycle(['#25276a', '#878dc5', '#c4c4c3', 
'#f4888a', '#b11f24']), None, 5))
colors_LR = list(islice(cycle(['#414042','#217a47', 'silver']), None, 3))

# creates catch all variables to encompass differences in plots for tuning and LR data
LR_plot_info = [LR_data_norm, 5, colors_LR]
tuning_plot_info = [tuning_data_norm, 3.5, colors_tuning]


##############################################################################################
##############################################################################################
# run command to plot the data (2 examples shown)
# plot_info: put in either LR_plot_info (if plotting switch pattern based on LRs) or 
# tuning_plot_info (for of constitutively expressed integrase switch level quantification)
# constructs_to_plot: put in names of constructs to plot (as they appear on the excel data 
# sheet) as a list of strings 
# ylim: max y axis value to show on plot
# filename: path in string form at which to save the generated plot, change file extension to 
# choose file type
##############################################################################################
#Example:
plot_data(LR_plot_info, ['L1_ARF19_4_T2P2_rd1','L1_ARF19_4_T2P3_rd1', 'L1_ARF19_4_T2P4_rd1', 'L1_ARF19_4_T2P12_rd1', 'L1_ARF19_4_T2P13_rd1','L1_ARF19_4_T2P14_rd1'], 110, path_for_plot)
plot_data(tuning_plot_info, ['L1B1','L1B2', 'L1B6', 'L1B8', 'NC'], 115, path_for_plot)

# %%
