# Bunch of imports
from bokeh.plotting import figure, curdoc
from bokeh.models import ColumnDataSource, Circle
from bokeh.models.widgets import TextInput
from bokeh.layouts import row


import pandas as pd
import random

import matplotlib.pyplot as plt
import matplotlib.colors as mcolors

def get_fake_data(n_s_label=5, seed=19):

    random.seed(a=seed)

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

def get_bubble_plot(traces_CDS):
    TOOLS = "tap,box_zoom,reset,wheel_zoom"
    bubble_plot = figure(tools=TOOLS)
    traces={}
    for s_label in traces_CDS:
        traces[s_label] = bubble_plot.circle(x='x',
                                   y='y',
                                   color='color',
                                   size='size',
                                   fill_alpha = 0.3,
                                   line_color = 'grey',
                                   source=traces_CDS[s_label])
        s_label_color = list(traces_df_dict[s_label]['color'])[0]
        traces[s_label].selection_glyph = \
                        Circle(fill_alpha=0.7,
                               fill_color=s_label_color,
                               line_color="red")
        traces[s_label].nonselection_glyph = \
                        Circle(fill_alpha= 0.3,
                               fill_color= s_label_color,
                               line_color="grey")
    return bubble_plot

'''---------------------------------------------------------------

                                main

---------------------------------------------------------------'''


# Create a fake data frame. This is part of what data.gz would provide
data_df = get_fake_data(seed=17)

# Each supelabel has a trace and each trace feeds
# from its ColumnDataSource (CDS)
traces_df_dict = get_traces_df_dict(data_df)
traces_CDS = {}
for s_label in traces_df_dict:
    traces_CDS[s_label]=ColumnDataSource(traces_df_dict[s_label])

#                       Create dashboard elements

# bubble_plot element
bubble_plot = get_bubble_plot(traces_CDS)

# text_input object
text_input = TextInput(value="default", title="Label:")


# Define interactivity
def my_text_input_handler(attr, old, new):
    print("Previous label: " + old)
    print("Updated label: " + new)
    try:
        int(new)
    except ValueError:
        print('Please enter a valid topic number')
    return
text_input.on_change("value", my_text_input_handler)

# Place elements in the dashboard
curdoc().add_root(row(text_input,bubble_plot))
