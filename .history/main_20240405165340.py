import pandas as pd
import numpy as np
# import seaborn as sns
import random
import numpy as np
# import matplotlib.pyplot as plt
import plotly.graph_objects as go
import plotly.express as px

import math
from random import randrange
from datetime import datetime

import re
import streamlit as st
from dotenv import load_dotenv
import os
import json
from utils import severity_generator, DV_generator, structure_generator, pricing_generator, notice_generator, loss_generator, df_generator



# Streamlit UI
st.set_page_config(layout="wide")  # Force wide mode
with open("style.css") as css:
    st.markdown(f'<style>{css.read()}</style>', unsafe_allow_html=True)

# AWS Credentials
aws_access_key_id = st.secrets.AWS_ACCESS_KEY_ID
aws_secret_access_key = st.secrets.AWS_SECRET_ACCESS_KEY
aws_default_region = st.secrets.AWS_DEFAULT_REGION

def div():
    st.divider()
    
st.title("ArgoXai - CRATOS - Pricing Tool - v2.4.5")
col1, col2, _, _, _, _, _, _ = st.columns([3,3,1,1,1,1,1,1])
number_of_simulations = col1.number_input("Enter Number of Simulations", value=10000)

st.divider()


# Notice Percentage Distribution
with st.container(border=True):
    st.subheader("Notice Percentage Distribution")
    col1, col2, col3, col4 = st.columns([2,2,2,2])
    notice_pct_dist_x1 = col1.number_input("Left", value=0.05, key="notice_left", format="%.2f")
    notice_pct_dist_x2 = col2.number_input("Center", value=0.15, key="notice_center", format="%.2f")
    notice_pct_dist_x3 = col3.number_input("Right", value=0.25, key="notice_right", format="%.2f")
    notice_pct_dist_x4 = col4.number_input("Size", value=100000, key="notice_size")
    
    # Generate Notice Percentage Distribution Plot
    fig_notice_pct = go.Figure()
    fig_notice_pct.add_trace(go.Histogram(x=np.random.triangular(
        notice_pct_dist_x1, 
        notice_pct_dist_x2, 
        notice_pct_dist_x3, 
        notice_pct_dist_x4
    ), name="Notice %"))
    st.plotly_chart(fig_notice_pct)

# Notice Percentage Loss Distribution
with st.container(border=True):
    st.subheader("Notice Percentage Loss Distribution")
    col5, col6, col7, col8 = st.columns([2,2,2,2])
    notice_pct_loss_dist_x1 = col5.number_input("Left", value=0.15, key="loss_left", format="%.2f")
    notice_pct_loss_dist_x2 = col6.number_input("Center", value=0.25, key="loss_center", format="%.2f")
    notice_pct_loss_dist_x3 = col7.number_input("Right", value=0.35, key="loss_right", format="%.2f")
    notice_pct_loss_dist_x4 = col8.number_input("Size", value=100000, key="loss_size")
    
    # Generate Notice Percentage Loss Distribution Plot
    fig_notice_pct_loss = go.Figure()
    fig_notice_pct_loss.add_trace(go.Histogram(x=np.random.triangular(
        notice_pct_loss_dist_x1, 
        notice_pct_loss_dist_x2, 
        notice_pct_loss_dist_x3, 
        notice_pct_loss_dist_x4
    ), name="Notice % Loss"))
    st.plotly_chart(fig_notice_pct_loss)

# Severity Distribution
with st.container(border=True):
    st.subheader("Severity Distribution")
    col9, col10, col11, col12 = st.columns([2,2,2,2])
    severity_dist_x1 = col9.number_input("Left", value=0.65, key="severity_left", format="%.2f")
    severity_dist_x2 = col10.number_input("Center", value=0.7, key="severity_center", format="%.2f")
    severity_dist_x3 = col11.number_input("Right", value=0.75, key="severity_right", format="%.2f")
    severity_dist_x4 = col12.number_input("Size", value=100000, key="severity_size")
    
    # Generate Severity Distribution Plot
    fig_severity = go.Figure()
    fig_severity.add_trace(go.Histogram(x=np.random.triangular(
        severity_dist_x1, 
        severity_dist_x2, 
        severity_dist_x3, 
        severity_dist_x4
    ), name="Severity"))
    st.plotly_chart(fig_severity)


notice_pct_dist = np.random.triangular(notice_pct_dist_x1, notice_pct_dist_x2, notice_pct_dist_x3, notice_pct_dist_x4)
notice_pct_loss_dist = np.random.triangular(notice_pct_loss_dist_x1, notice_pct_loss_dist_x2, notice_pct_loss_dist_x3, notice_pct_loss_dist_x4)
severity_dist = np.random.triangular(severity_dist_x1, severity_dist_x2, severity_dist_x3, severity_dist_x4)

# notice_pct, notice_pct_loss, low_severity_pct, med_severity_pct, high_severity_pct = severity_generator(notice_pct_dist, notice_pct_loss_dist, severity_dist)

# st.write("Notice %:", notice_pct)
# st.write("Notice % Loss:", notice_pct_loss)
# st.write("Low Severity %:", low_severity_pct)
# st.write("Medium Severity %:", med_severity_pct)
# st.write("High Severity %:", high_severity_pct)

with st.container(border=True):
    col13, col14, _, _ = st.columns([2,2,2,2])
    deal_count = col13.number_input("Deal Count", value=100)
    DV_range = col14.number_input("DV Range", value=2500000)

with st.container(border=True):
    col15, col16, col17, _ = st.columns([2,2,2,2])
    sme_low_DV, sme_upper_DV = col15.slider("Select SME DV Range", min_value=1000000, max_value=100000000, value=(10000000, 75000000))
    mm_low_DV, mm_upper_DV = col16.slider("Select MM DV Range", min_value=50000000, max_value=1000000000, value=(75000000, 750000000))
    j_low_DV, j_upper_DV = col17.slider("Select J DV Range", min_value=500000000, max_value=10000000000, value=(750000000, 5000000000))

with st.container(border=True):
    col1, col2, col3, _ = st.columns([2,2,2,2])
    sme_pct = col1.number_input("SME %", value=0.35, format="%.2f")
    mm_pct = col2.number_input("MM %", value=0.55, format="%.2f")
    j_pct = col3.number_input("J %", value=0.1, format="%.2f")

# DV_list = DV_generator(deal_count, DV_range, sme_low_DV, sme_upper_DV, mm_low_DV, mm_upper_DV, sme_pct, mm_pct, j_pct, j_low_DV, j_upper_DV)

# st.write(f'DV list: {DV_list}')

with st.container(border=True):
    col4, col5, col6, col7 = st.columns([2,2,2,2])
    low_limit, upper_limit = col4.slider("Select Limit Range", min_value=10000000, max_value=100000000, value=(30000000, 50000000), step=2500000)
    limit_range = col5.number_input("Limit Range Increment", value=2500000)

with st.container(border=True):
    col8, col9,_,_ = st.columns([2,2,2,2])
    primary_pct = col8.number_input("Primary %", value=0.7, format="%.2f")
    xs_pct = col9.number_input("XS %", value=0.3, format="%.2f")

with st.container(border=True):
    col18, col19, col20, _ = st.columns([2,2,2,2])
    pri_attachment_pt_range_x1 = col18.number_input("Pri Attachment Pt Range Start", value=0.0025, format="%.4f")
    pri_attachment_pt_range_x2 = col19.number_input("Pri Attachment Pt Range End", value=0.005, format="%.4f")
    pri_attachment_pt_range_x3 = col20.number_input("Pri Attachment Pt Range Step", value=0.0005, format="%.4f")
    pri_attachment_pt_range = np.arange(pri_attachment_pt_range_x1, pri_attachment_pt_range_x2, pri_attachment_pt_range_x3)

# limit_list, attachment_pt_list, primary_xs_list = structure_generator(DV_list, low_limit, upper_limit, limit_range, primary_pct, xs_pct, pri_attachment_pt_range)

# st.write("Limit List:", limit_list)
# st.write("Attachment Point List:", attachment_pt_list)
# st.write("Primary XS List:", primary_xs_list)

with st.container(border=True):
    col21, col22, col23, col24 = st.columns([1,1,1,1])
    pricing_range = col21.number_input("Pricing Range", value=0.05)
    sme_pricing_low, sme_pricing_high = col22.slider("Select SME Pricing Range", min_value=0.01, max_value=0.02, value=(0.012, 0.0145))
    mm_pricing_low, mm_pricing_high = col23.slider("Select MM Pricing Range", min_value=0.01, max_value=0.02, value=(0.0135, 0.0165))
    j_pricing_low, j_pricing_high = col24.slider("Select J Pricing Range", min_value=0.03, max_value=0.08, value=(0.035, 0.075))

# pricing_list = pricing_generator(DV_list, limit_list, attachment_pt_list, primary_xs_list, pricing_range, sme_pricing_low, sme_pricing_high, mm_pricing_low, mm_pricing_high, j_pricing_low, j_pricing_high)

def w(string):
    st.write(string)

# w(f'procong list:{pricing_list}')

# notice_list = notice_generator(deal_count, notice_pct, notice_pct_loss, low_severity_pct, med_severity_pct, high_severity_pct)

# w(f'notice list: {notice_list}')

with st.container():
    col1, col2,_,_ = st.columns([1,1,1,1])
    
    low_low_severity_loss, low_high_severity_loss = col1.slider("Select Low Severity Loss Range", min_value=0, max_value=1000000, value=(0, 1000000))
    med_low_severity_loss, med_high_severity_loss = col2.slider("Select Medium Severity Loss Range", min_value=1000000, max_value=10000000, value=(1000000, 10000000))
    # loss_list = loss_generator(notice_list, limit_list, low_low_severity_loss, low_high_severity_loss, med_low_severity_loss, med_high_severity_loss)


div()
# Calculate button placed at the bottom after all parameters have been set
data = st.button("Calculate")

# df = df_generator(DV_list, pricing_list, attachment_pt_list, notice_list, loss_list, limit_list)

with st.container(border=True):
    # Initialize an empty plot before calculations are triggered by the search button
    if not data:
        st.write("Please initiate calculations by clicking the 'Calculate' button.")
        st.empty()
    else:
        performance_stats = []

        # Adding a progress bar
        progress_bar = st.progress(0)
        # Adding placeholders for messages
        process_message = st.empty()
        section_message = st.empty()

        for i in range(number_of_simulations):
            progress = int(((i+1)/number_of_simulations)*100)
            progress_bar.progress(progress)
            # Updating messages
            process_message.text(f"Processing: Simulation {i+1}/{number_of_simulations}")
            

            notice_pct, notice_pct_loss, low_severity_pct, med_severity_pct, high_severity_pct = severity_generator(notice_pct_dist, notice_pct_loss_dist, severity_dist)
            section_message.text("Generating Severity...")
            DV_list = DV_generator(deal_count, DV_range, sme_low_DV, sme_upper_DV, mm_low_DV, mm_upper_DV, sme_pct, mm_pct, j_pct, j_low_DV, j_upper_DV)
            section_message.text("Generating DV...")
            limit_list, attachment_pt_list, primary_xs_list = structure_generator(DV_list, low_limit, upper_limit, limit_range, primary_pct, xs_pct, pri_attachment_pt_range)
            section_message.text("Generating Structure...")
            pricing_list = pricing_generator(DV_list, limit_list, attachment_pt_list, primary_xs_list, pricing_range, sme_pricing_low, sme_pricing_high, mm_pricing_low, mm_pricing_high, j_pricing_low, j_pricing_high)
            section_message.text("Generating Pricing...")
            notice_list = notice_generator(deal_count, notice_pct, notice_pct_loss, low_severity_pct, med_severity_pct, high_severity_pct)
            section_message.text("Generating Notice...")
            loss_list = loss_generator(notice_list, limit_list, low_low_severity_loss, low_high_severity_loss, med_low_severity_loss, med_high_severity_loss)
            section_message.text("Generating Loss...")
            df = df_generator(DV_list, pricing_list, attachment_pt_list, notice_list, loss_list, limit_list)
            performance_stats.append(df['Performance'].sum().round(0))

        # Plotting the performance statistics using Plotly
        fig = px.histogram(performance_stats, nbins=100, title="Performance Statistics Distribution")
        fig.update_layout(bargap=0.1)
        fig.add_vline(x=np.mean(performance_stats), line_dash="dash", line_color="red", annotation_text="Mean", annotation_position="top right")
        st.plotly_chart(fig)

        # Displaying additional performance statistics
        percentage_above_0 = len([i for i in performance_stats if i > 0])/len(performance_stats)
        percentage_above_1m = len([i for i in performance_stats if i > 1_000_000])/len(performance_stats)
        percentage_above_10m = len([i for i in performance_stats if i > 10_000_000])/len(performance_stats)
        average_performance = round(sum(performance_stats)/len(performance_stats))
        max_performance = round(max(performance_stats))
        min_performance = round(min(performance_stats))

        st.write(f"Percentage of scenarios above 0: {percentage_above_0*100:.2f}%")
        st.write(f"Percentage of scenarios above 1m: {percentage_above_1m*100:.2f}%")
        st.write(f"Percentage of scenarios above 10m: {percentage_above_10m*100:.2f}%")
        st.write(f"Average: {average_performance}")
        st.write(f"Max: {max_performance}")
        st.write(f"Min: {min_performance}")

        # Clearing messages after completion
        process_message.empty()
        section_message.empty()

        # Reset progress bar after completion
        progress_bar.empty()

w(f'Frozen: 05-04-2024')