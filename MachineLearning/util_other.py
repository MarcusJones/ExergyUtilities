
import numpy as np
import matplotlib as mpl
import pandas as pd
import matplotlib.pyplot as plt
import logging





#--- EDA tools

#%% Function to calculate missing values by column# Funct 
def missing_values_table(df, sort = True, show_all=True):
        # Total missing values
        mis_val = df.isnull().sum()
        
        # Percentage of missing values
        mis_val_percent = 100 * df.isnull().sum() / len(df)
        
        # Make a table with the results
        mis_val_table = pd.concat([mis_val, mis_val_percent], axis=1)
        
        # Rename the columns
        mis_val_table_ren_columns = mis_val_table.rename(
        columns = {0 : 'Missing Values', 1 : '% of Total Values'})
        
        # Sort the table by percentage of missing descending
        if sort:
            mis_val_table_ren_columns = mis_val_table_ren_columns[
                mis_val_table_ren_columns.iloc[:,1] != 0].sort_values(
            '% of Total Values', ascending=False).round(1)
        
        # Print some summary information
        print ("Your selected dataframe has " + str(df.shape[1]) + " columns.\n"      
            "There are " + str(mis_val_table_ren_columns.shape[0]) +
              " columns that have missing values.")
        
        # Return the dataframe with missing information
        return mis_val_table_ren_columns


def create_column_summary(this_df):
    
    #this_df = dfs['bureau_balance']
    #this_df.columns
    
    this_summary = exergyml_util_other.missing_values_table(this_df,sort=False)
    this_summary = pd.concat([this_summary, this_df.dtypes], axis=1)
    
    this_summary = this_summary.rename({0:"dtype"},axis='columns')
    
    this_summary['num_cats'] = None
    this_summary['cats'] = ""
    for cat_col in this_df.select_dtypes(include='category'):
        this_summary.loc[cat_col, 'num_cats'] = this_df[cat_col].nunique()
        
        these_categories = this_df[cat_col].cat.categories.values.tolist()
        categories_str = ", ".join(these_categories)
        this_summary.loc[cat_col, 'cats'] = categories_str
        
        #this_df.select_dtypes(include='category').nunique()
    logging.debug("Created summary for a data frame")
    return this_summary




def grid_scores_to_df(grid_scores):
    """
    Convert a sklearn.grid_search.GridSearchCV.grid_scores_ attribute to a tidy
    pandas DataFrame where each row is a hyperparameter-fold combinatination.
    """
    rows = list()
    for i,grid_score in enumerate(grid_scores):
        
        for fold, score in enumerate(grid_score.cv_validation_scores):
            #row = dict()
            row = grid_score.parameters.copy()
            row['param_set'] = i
            row['fold'] = fold
            row['score'] = score
            rows.append(row)
    df = pd.DataFrame(rows)
    return df

#--- Conversions
def strfdelta(tdelta, fmt):
    d = {"days": tdelta.days}
    d["hours"], rem = divmod(tdelta.seconds, 3600)
    d["minutes"], d["seconds"] = divmod(rem, 60)
    return fmt.format(**d)

def convert_categorical(df):
    logging.debug("\tConverted object columns to category")
    return pd.concat([
        df.select_dtypes(include=[], exclude=['object']),
        df.select_dtypes(include=['object']).apply(pd.Series.astype, dtype='category')
        ], axis=1).reindex(df.columns, axis=1)

#--- Plotting
#exergy.util_excel
def get_contour_verts(cn):
    contours = []
    # for each contour line
    for cc in cn.collections:
        paths = []
        # for each separate section of the contour line
        for pp in cc.get_paths():
            xy = []
            # for each segment of that section
            for vv in pp.iter_segments():
                xy.append(vv[0])
            paths.append(np.vstack(xy))
        contours.append(paths)

    return contours





# http://scipy-cookbook.readthedocs.io/items/Matplotlib_ColormapTransformations.html
def cmap_map(function, cmap):
    """ Applies function (which should operate on vectors of shape 3: [r, g, b]), on colormap cmap.
    This routine will break any discontinuous points in a colormap.
    """
    cdict = cmap._segmentdata
    step_dict = {}
    # Firt get the list of points where the segments start or end
    for key in ('red', 'green', 'blue'):
        step_dict[key] = list(map(lambda x: x[0], cdict[key]))
    step_list = sum(step_dict.values(), [])
    step_list = np.array(list(set(step_list)))
    # Then compute the LUT, and apply the function to the LUT
    reduced_cmap = lambda step : np.array(cmap(step)[0:3])
    old_LUT = np.array(list(map(reduced_cmap, step_list)))
    new_LUT = np.array(list(map(function, old_LUT)))
    # Now try to make a minimal segment definition of the new LUT
    cdict = {}
    for i, key in enumerate(['red','green','blue']):
        this_cdict = {}
        for j, step in enumerate(step_list):
            if step in step_dict[key]:
                this_cdict[step] = new_LUT[j, i]
            elif new_LUT[j,i] != old_LUT[j, i]:
                this_cdict[step] = new_LUT[j, i]
        colorvector = list(map(lambda x: x + (x[1], ), this_cdict.items()))
        colorvector.sort()
        cdict[key] = colorvector

    return mpl.colors.LinearSegmentedColormap('colormap',cdict,1024)



def plot_confusion_matrix(cm, classes,
                          normalize=False,
                          title='Confusion matrix',
                          cmap=plt.cm.Blues,
                          size = None
                          
                          ):
    """
    This function prints and plots the confusion matrix.
    Normalization can be applied by setting `normalize=True`.
    """
    if normalize:
        cm = cm.astype('float') / cm.sum(axis=1)[:, np.newaxis]
        print("Normalized confusion matrix")
    else:
        print('Confusion matrix, without normalization')

    print(cm)
    
    fig, ax = plt.subplots(figsize=size)         # Sample figsize in inches



    plt.style.use('ggplot')


#sns.heatmap(addr_cross_cat, linewidths=.5,cmap='jet');
#sns.heatmap(addr_cross_cat, linewidths=.5,cmap = cmap,ax=ax)
#plt.tight_layout(pad=5)
#plt.suptitle(title_str,fontname = 'Arial', fontsize=16)
#plt.title("{} to {}, {} records".format(min_time,max_time,num_recs))

    plt.imshow(cm, interpolation='nearest', cmap=cmap)
    plt.title(title)
    plt.colorbar()
    tick_marks = np.arange(len(classes))
    plt.xticks(tick_marks, classes, rotation=45)
    plt.yticks(tick_marks, classes)
    #plt.tight_layout()
    plt.ylabel('True label')
    plt.xlabel('Predicted label')
    plt.tight_layout(pad=5)

#    fmt = '.2f' if normalize else 'd'
#    thresh = cm.max() / 2.
#    for i, j in itertools.product(range(cm.shape[0]), range(cm.shape[1])):
#        plt.text(j, i, format(cm[i, j], fmt),
#                 horizontalalignment="center",
#                 color="white" if cm[i, j] > thresh else "black")





