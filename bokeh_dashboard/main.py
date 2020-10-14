# Bunch of imports
from bokeh.plotting import figure, curdoc
from bokeh.models import ColumnDataSource
from bokeh.models.widgets import TextInput
from bokeh.layouts import row

import pandas as pd
import random

import matplotlib.pyplot as plt
import matplotlib.colors as mcolors

def get_fake_data(n_s_label=5):

    random.seed(a=19)

    # Initialize data dict
    data = {'s_label'+str(i): {'labels':[],
                               'x':[],
                               'y':[],
                               'size':[],
                               'color':{}}
                               for i in range(n_s_label)}
    # Select a color for each s_label
    s_colors = random.sample( list(mcolors.CSS4_COLORS.keys()), n_s_label)
    s_label_color={ 's_label'+str(i):s_colors[i] for i in range(n_s_label)}

    print('s_colors ',s_colors)

    # Fill the dictionary
    list_of_df = []
    for s_label in data:
        n_labels=random.randrange(4,10)
        data[s_label]['labels'] = [ s_label+'_'+str(i) for i in range(n_labels)]
        data[s_label]['x']      = [random.uniform(0,10) for i in range(n_labels)]
        data[s_label]['y']      = [random.uniform(0,10) for i in range(n_labels)]
        data[s_label]['size']   = [random.uniform(10,50) for i in range(n_labels)]
        data[s_label]['color']  = n_labels*[s_label_color[s_label]]

        df = pd.DataFrame(data[s_label])
        df['super label'] = n_labels *[s_label]
        list_of_df.append(df)

    data_df = pd.concat(list_of_df)
    data_df = data_df.sample(frac=1).reset_index(drop=True)
    data_df = data_df.reset_index()
    data_df = data_df.rename(columns={'index':'Topic Index'})

    return data_df


def get_traces_df_dict(data_df):
    # First get the super labels, which define the number of traces
    traces_labels = data_df['super label'].unique()
    n_traces= len(traces_labels)
    print(n_traces, traces_labels)

    # Now for each label create a df
    traces_dict = { s_label:data_df[data_df['super label']==s_label]
                    for s_label in traces_labels}

    return traces_dict

'''---------------------------------------------------------------

                                main

---------------------------------------------------------------'''


# Create a fake data frame
data_df = get_fake_data()
print(data_df.head())

traces_df_dict = get_traces_df_dict(data_df)

traces_CDS = {}
for s_label in traces_df_dict:
    traces_CDS[s_label]=ColumnDataSource(traces_df_dict[s_label])

# Create dashboard elements
# given the traces CDS's make one plot for each trace
p=figure()
traces={}
for s_label in traces_CDS:
    traces[s_label] = p.circle(x='x',
                               y='y',
                               color='color',
                               size='size',
                               source=traces_CDS[s_label])



text_input = TextInput(value="default", title="Label:")


# Define interactivity
def my_text_input_handler(attr, old, new):
    print("Previous label: " + old)
    print("Updated label: " + new)
text_input.on_change("value", my_text_input_handler)

# Place elements in the dashboard
curdoc().add_root(row(text_input,p))
