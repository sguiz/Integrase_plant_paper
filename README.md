# Codes to process data for Guiziou et al., 2023: An integrase toolbox to record gene-expression during plant development.

## Seedling plotting scrit

This script allows you to create stacked bar plots showing the switching categories (either for tuning or lateral root switching data). It also computes statistical significance for the tuning dataset using analysis of variance (ANOVA) with a post hoc Tukey’s test.

### Package dependencies
Pandas<br>
Matplotlib<br>
Scipy.stats<br>
Scikit_posthocs<br>
Statsmodels<br>
Itertools<br><br>

Data file included as a reference for data formatting

## Tobacco injection plotting script

This script allows you to plot tobacco injection data (plate reader fluorescence measurements from injected leaf punches). It also computes statistical significance using ANOVA with post hoc Tukey’s test.

### Package dependencies
Pandas<br>
Matplotlib<br>
Scipy.stats<br>
Scikit_posthocs<br>
Statsmodels<br>
Seaborn<br><br>

Data (raw plate reader output) and plate layout example files are included for reference

## ImageJ image processing macro

This macro allows you to take a .lif file and automatically process many multichannel images from the fluorescent microscope as a batch. It adjusts brightness/contrast, adds appropriate lookup tables, merges channels, and adds a scale bar for 10x magnification.
Dependency: Save_all ImageJ plugin can be found https://imagejdocu.list.lu/plugin/utilities/save_all/start

### Instructions for macro use
1. Import .lif file. In the pop-up check only the Autoscale box. Set “view stack with” as Hyperstack and set “Color mode” as colorized. <br>
2. Hit Ok and select desired image set. <br>
3. Go to Plugins>SaveAllImages and enter the directory where you want to save your processed images. For the “is this image a stack” option select No. <br> 
4. Go to Process>Batch>Macro. In the Input space enter where you saved your images in the last step. In the Output space put where you want your processed images to be saved. In the box, paste the macro from the macro .txt file in this repo.<br>
5. Select process and your images will all be processed and in the specified output folder!<br><br>
