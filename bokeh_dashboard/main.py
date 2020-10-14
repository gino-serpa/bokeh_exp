# Bunch of imports
from bokeh.plotting import figure, curdoc
from bokeh.models import ColumnDataSource
import pandas as pd
import random

def get_fake_data(n_s_label=5):

    random.seed(a=19)
    s_labels = [ ('s_label'+str(i),random.rand_range(4,10))
                         for i in range(n_s_label) ]
    s_label_label = []
    for s_label, size in s_labels:
        for topic in range(size):
            pair = (s_label,s_label+str(topic))
            s_label_label.append(pair)
    s_label_label.sort(key= lambda x:random.random())


    data_dict = {'super label':super_label,
                 'label':      ['tomato','potato','dog','leek','cat'],
                 'x':[i for i in range(5)],
                 'y':[i*i for i in range(5)],
                 'size':[5+i for i in range(5)],
                 'color':['red','red','blue','red','blue']}
    print(data_dict)
    fake_data = pd.DataFrame(data_dict)
    return fake_data


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


# Create a data frame with 3 potential plots
data_df = get_fake_data()
print(data_df.head())

traces_df_dict = get_traces_df_dict(data_df)

traces_CDS = {}
for s_label in traces_df_dict:
    print(s_label, traces_df_dict[s_label])
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

# Define interactivity



# Place elements in the dashboard
curdoc().add_root(p)
