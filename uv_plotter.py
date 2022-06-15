import streamlit as st
import pandas as pd
import numpy as np 
import csv
import plotly
import plotly.express as px
from io import StringIO
from PIL import Image



st.title('UV VisPlotter V1') 

filter_name = st.text_input('Type a condition you would  like to look  at, clear this area if you want to see all your data!', 'Ex: pH 7.0')
cuvettes_used = st.text_input('Type the number of measurements done in your experiment'
                               '/nIf you did a time trial,  [Measurements  = (# Cuvettes Loaded) x (# Timepoints)]' ) 




def uv_vis_cleaner():
    uploaded_file = st.file_uploader("Upload a csv file!", type={"csv", "txt"})
    if uploaded_file is not None:
        stringio = StringIO(uploaded_file.getvalue().decode("utf-8"))
        read_file = csv.reader(stringio, delimiter=",")
        data = list(read_file)
        
        
        
        #removeing all spectral data that is not absorbtions / emission spectra
        no_sides = []

        for row in range(len(data)):
            try:
                if len(data[row][0]) == 0:
                    break
                current_row = []
                for col in range(int(cuvettes_used)*2):
                    current_row.append(data[row][col])
                no_sides.append(current_row)
            
            except IndexError:
                break
                
                
                
        #removing header labels and reassigning them#
        
        table = pd.DataFrame(no_sides,  dtype = float).round(3)
        
        header = table.iloc[0,:].tolist()
        
        new_header = ['Wavelength (nm)']
        for i in range(len(header)):
            if len(header[i]) > 0:
                new_header.append(header[i])
        
        
            
        
        #table is headerless and has removed duplicate wavelength columns
        
        table = table.iloc[1:,:]
        df2 = table.T.drop_duplicates().T
        
        data_numeric = pd.DataFrame(df2.iloc[1:,:],  dtype = float).round(3)
        
        
        ##assigning headers for cleaned columns
        data_numeric.columns = new_header
        
        if filter_name:
            
            data_numeric_filtered = data_numeric.filter(regex = filter_name)
            wavelengths =  df2[0][1:].tolist()
            wavelengths = pd.to_numeric(wavelengths)
            
            data_numeric_filtered.insert(0, 'Wavelength (nm)' , wavelengths)
            
            
            
            return data_numeric_filtered.round(3)
                                        
                                        
        return data_numeric

table = uv_vis_cleaner()
st.write(table)

def uv_vis_plotter(table):
        
    labels = table.columns.tolist()[1:]
        
    
    fig = px.line(table, x= 'Wavelength (nm)', y = table.columns)
        
    fig.update_yaxes(title_text= 'Abs' , range = [0,2.5])
    
    fig.update_traces(line_color= labels, selector=dict(type='scatter'))
        
    fig.update_layout(scene = dict(
                        xaxis_title= 'Wavelenth (nm)',
                        yaxis_title='Abs'),
                        width=1000,
                        height = 500
                            
                    )
        
    return fig
if table is not None:
    plot = uv_vis_plotter(table)
    st.plotly_chart(plot, sharing="streamlit"  )
