# import pandas as pd
# import numpy as np
# # import seaborn as sns
# import random
import numpy as np
# import matplotlib.pyplot as plt
import plotly.graph_objects as go
import plotly.express as px
from scipy.stats import skewnorm
import math
from random import randrange
from datetime import datetime

import re
import streamlit as st
from dotenv import load_dotenv
import os
import json
import pandas as pd
from utils import severity_generator, DV_generator, structure_generator, pricing_generator, notice_generator, loss_generator, df_generator, mapping_dict



# Streamlit UI
st.set_page_config(layout="wide")  # Force wide mode
with open("style.css") as css:
    st.markdown(f'<style>{css.read()}</style>', unsafe_allow_html=True)

# # AWS Credentials
# aws_access_key_id = st.secrets.AWS_ACCESS_KEY_ID
# aws_secret_access_key = st.secrets.AWS_SECRET_ACCESS_KEY
# aws_default_region = st.secrets.AWS_DEFAULT_REGION


st.title("ArgoXai - CRATOS - Pricing Tool - v4")

def div():
    st.divider()
    
tab1, tab2, tab3, tab4 = st.tabs(["Country Risk", "Business Risk", "Legal Documentation Risk", "Portfolio Creator"])



with tab1:
    st.title("Country Risk Section")
    col1, col2, _, _, _, _, _, _ = st.columns([3,3,1,1,1,1,1,1])
    with col1.container(border=True):
        option = st.selectbox(
            "Select a country",
            list(mapping_dict.keys()),
            index=None)
        st.write("You selected:", option)

    
    # col1, col2, _, _, _, _, _, _ = st.columns([3,3,1,1,1,1,1,1])
    # with col1.container(border=True):
    #     if option in mapping_dict:
    #         total_n = mapping_dict[option]
    #         # st.subheader("CR Adjusted Rate")
    #         if 'average_rate_on_line' in locals():
    #             cr_adjusted_rate = (average_rate_on_line + (average_rate_on_line * total_n))
    #             st.metric(label="CR Adjusted Rate", value=f"{cr_adjusted_rate:.2f}%")
    #         else:
    #             st.write("Please run the Portfolio Creator")
    #     else:
    #         st.write("Selected country is not in the mapping dictionary.")

            
with tab2:
    st.title("Business Risk Section")
    
    parent_sectors = ['Basic Materials', 'Capital Goods', 'Conglomerates', 'Consumer Cyclical', 'Consumer Non-Cyclical', 'Energy', 'Financial', 'Healthcare', 'Services', 'Technology', 'Transportation', 'Utilities']
    sector_dict = {
        'Basic Materials': ['Misc. Fabricated Products', 'Fabricated Plastic & Rubber', 'Containers & Packaging', 'Metal Mining', 'Gold & Silver', 'Chemical Manufacturing', 'Iron & Steel', 'Non-Metallic Mining', 'Chemicals - Plastics & Rubber', 'Paper & Paper Products', 'Forestry & Wood Products'],
        'Capital Goods': ['Mobile Homes & RVs', 'Aerospace & Defense', 'Misc. Capital Goods', 'Constr. & Agric. Machinery', 'Construction Services', 'Construction - Raw Materials', 'Constr. - Supplies & Fixtures'],
        'Conglomerates': ['Conglomerates'],
        'Consumer Cyclical': ['Appliance & Tool', 'Auto & Truck Manufacturers', 'Recreational Products', 'Auto & Truck Parts', 'Apparel/Accessories', 'Jewelry & Silverware', 'Footwear', 'Furniture & Fixtures', 'Textiles - Non Apparel', 'Audio & Video Equipment', 'Tires', 'Photography'],
        'Consumer Non-Cyclical': ['Beverages (Alcoholic)', 'Food Processing', 'Office Supplies', 'Personal & Household Products', 'Crops', 'Beverages (Non-Alcoholic)', 'Fish/Livestock', 'Tobacco'],
        'Energy': ['Oil & Gas Operations', 'Oil Well Services & Equipment', 'Oil & Gas - Integrated', 'Coal', 'Alternative Energy'],
        'Financial': ['Insurance (Accident & Health)', 'Insurance (Prop. & Casualty)', 'Other (Mutual Fund)', 'Investment Services', 'S&Ls/Savings Banks', 'Insurance (Miscellaneous)', 'Misc. Financial Services', 'Money Center Banks', 'Consumer Financial Services', 'Insurance (Life)', 'Regional Banks'],
        'Healthcare': ['Healthcare Facilities', 'Medical Equipment & Supplies', 'Biotechnology & Drugs', 'Major Drugs'],
        'Services': ['Business Services', 'Waste Management Services', 'Communications Services', 'Real Estate Operations', 'Broadcasting & Cable TV', 'Restaurants', 'Printing & Publishing', 'Retail (Drugs)', 'Casinos & Gaming', 'Retail (Specialty)', 'Retail & Repair (Automotive)', 'Personal Services', 'Recreational Activities', 'Motion Pictures', 'Rental & Leasing', 'Retail (Apparel)', 'Schools', 'Retail (Home Improvement)', 'Retail (Department & Discount)', 'Retail (Catalog & Mail Order)', 'Hotels & Motels', 'Security Systems & Services', 'Advertising', 'Printing Services', 'Retail (Grocery)', 'Retail (Technology)'],
        'Technology': ['Semiconductors', 'Computer Hardware', 'Communications Equipment', 'Software & Programming', 'Computer Networks', 'Computer Services', 'Computer Peripherals', 'Electronic Instruments & Controls', 'Office Equipment', 'Computer Storage Devices', 'Scientific & Technical Instr.'],
        'Transportation': ['Airline', 'Railroads', 'Misc. Transportation', 'Trucking', 'Air Courier', 'Water Transportation'],
        'Utilities': ['Natural Gas Utilities', 'Electric Utilities', 'Water Utilities']
    }
    
    col1, col2, _, _, _, _, _, _ = st.columns([3,3,1,1,1,1,1,1])
    with col1.container(border=True):
        selected_parent = st.selectbox("Select Sector", parent_sectors, index=None, placeholder="Select a Sector...")
    
    col1, col2, _, _, _, _, _, _ = st.columns([3,3,1,1,1,1,1,1])
    with col1.container(border=True):
        if selected_parent:
            selected_child = st.selectbox("Select an Industry", sector_dict[selected_parent], index=None, placeholder="Select Industry...")
            st.write(f"You selected sector: {selected_parent}")
            st.write(f"You selected industry: {selected_child}")
        else:
            st.write("Please select a parent sector to see child sectors.")
    
with tab3:
    st.title("Legal Documentation Risk")

with tab4:
    
    
    col1, col2, _, _, _, _, _, _ = st.columns([3,3,1,1,1,1,1,1])
    number_of_simulations = col1.number_input("Enter Number of Simulations", value=100)

    st.divider()
    # Combined Distribution Containers
    with st.container(border=True):
        st.subheader("Distributions")
        
        # Distribution Type Selection
        dist_type = st.radio("Select Distribution Type", ['Triangular', 'Normal'], index=0)
        
        col1, col2, col3 = st.columns([2,2,2])

        # Notice Percentage Distribution
        with col1:
            with st.container(border=True):
                st.subheader("Notice Pct. Distribution")
                col1_1, col1_2, col1_3, col1_4 = st.columns(4)
                if dist_type == 'Triangular':
                    notice_pct_dist_x1 = col1_1.number_input("Left", value=0.05, key="notice_left", format="%.2f")
                    notice_pct_dist_x2 = col1_2.number_input("Center", value=0.15, key="notice_center", format="%.2f")
                    notice_pct_dist_x3 = col1_3.number_input("Right", value=0.25, key="notice_right", format="%.2f")
                    notice_pct_dist_x4 = col1_4.number_input("Size", value=100000, key="notice_size")
                    notice_pct_dist = np.random.triangular(notice_pct_dist_x1, notice_pct_dist_x2, notice_pct_dist_x3, notice_pct_dist_x4)
                else:
                    notice_pct_dist_mean = col1_2.number_input("Mean", value=0.15, key="notice_mean", format="%.2f")
                    notice_pct_dist_std = col1_3.number_input("Std", value=0.05, key="notice_std", format="%.2f")
                    notice_pct_dist_skew = col1_1.number_input("Skew", value=3, key="notice_skew", format="%d")
                    notice_pct_dist_x4 = col1_4.number_input("Size", value=100000, key="notice_size")
                    notice_pct_dist = skewnorm.rvs(a=notice_pct_dist_skew, loc=notice_pct_dist_mean, scale=notice_pct_dist_std, size=notice_pct_dist_x4)
                
                # Generate Notice Percentage Distribution Plot
                fig_notice_pct = go.Figure()
                fig_notice_pct.add_trace(go.Histogram(x=notice_pct_dist, name="Notice %"))
                fig_notice_pct.update_layout(margin=dict(l=5, r=5, t=5, b=5), autosize=True, height=200)
                st.plotly_chart(fig_notice_pct, use_container_width=True)

        # Notice Percentage Loss Distribution
        with col2:
            with st.container(border=True):
                st.subheader("Notice Pct-Loss Distribution")
                col2_1, col2_2, col2_3, col2_4 = st.columns(4)
                if dist_type == 'Triangular':
                    notice_pct_loss_dist_x1 = col2_1.number_input("Left", value=0.15, key="loss_left", format="%.2f")
                    notice_pct_loss_dist_x2 = col2_2.number_input("Center", value=0.25, key="loss_center", format="%.2f")
                    notice_pct_loss_dist_x3 = col2_3.number_input("Right", value=0.35, key="loss_right", format="%.2f")
                    notice_pct_loss_dist_x4 = col2_4.number_input("Size", value=100000, key="loss_size")
                    notice_pct_loss_dist = np.random.triangular(notice_pct_loss_dist_x1, notice_pct_loss_dist_x2, notice_pct_loss_dist_x3, notice_pct_loss_dist_x4)
                else:
                    notice_pct_loss_dist_mean = col2_2.number_input("Mean", value=0.25, key="loss_mean", format="%.2f")
                    notice_pct_loss_dist_std = col2_3.number_input("Std", value=0.05, key="loss_std", format="%.2f")
                    notice_pct_loss_dist_skew = col2_1.number_input("Skew", value=-3, key="loss_skew", format="%d")
                    notice_pct_loss_dist_x4 = col2_4.number_input("Size", value=100000, key="loss_size")
                    notice_pct_loss_dist = skewnorm.rvs(a=notice_pct_loss_dist_skew, loc=notice_pct_loss_dist_mean, scale=notice_pct_loss_dist_std, size=notice_pct_loss_dist_x4)
                
                # Generate Notice Percentage Loss Distribution Plot
                fig_notice_pct_loss = go.Figure()
                fig_notice_pct_loss.add_trace(go.Histogram(x=notice_pct_loss_dist, name="Notice % Loss"))
                fig_notice_pct_loss.update_layout(margin=dict(l=5, r=5, t=5, b=5), autosize=True, height=200)
                st.plotly_chart(fig_notice_pct_loss, use_container_width=True)

        # Severity Distribution
        with col3:
            with st.container(border=True):
                st.subheader("Severity Distribution")
                col3_1, col3_2, col3_3, col3_4 = st.columns(4)
                if dist_type == 'Triangular':
                    severity_dist_x1 = col3_1.number_input("Left", value=0.65, key="severity_left", format="%.2f")
                    severity_dist_x2 = col3_2.number_input("Center", value=0.7, key="severity_center", format="%.2f")
                    severity_dist_x3 = col3_3.number_input("Right", value=0.75, key="severity_right", format="%.2f")
                    severity_dist_x4 = col3_4.number_input("Size", value=100000, key="severity_size")
                    severity_dist = np.random.triangular(severity_dist_x1, severity_dist_x2, severity_dist_x3, severity_dist_x4)
                else:
                    severity_dist_mean = col3_2.number_input("Mean", value=0.7, key="severity_mean", format="%.2f")
                    severity_dist_std = col3_3.number_input("Std", value=0.05, key="severity_std", format="%.2f")
                    severity_dist_skew = col3_1.number_input("Skew", value=0, key="severity_skew", format="%d")
                    severity_dist_x4 = col3_4.number_input("Size", value=100000, key="severity_size")
                    severity_dist = skewnorm.rvs(a=severity_dist_skew, loc=severity_dist_mean, scale=severity_dist_std, size=severity_dist_x4)
                
                # Generate Severity Distribution Plot
                fig_severity = go.Figure()
                fig_severity.add_trace(go.Histogram(x=severity_dist, name="Severity"))
                fig_severity.update_layout(margin=dict(l=5, r=5, t=5, b=5), autosize=True, height=200)
                st.plotly_chart(fig_severity, use_container_width=True)

    # notice_pct, notice_pct_loss, low_severity_pct, med_severity_pct, high_severity_pct = severity_generator(notice_pct_dist, notice_pct_loss_dist, severity_dist)

    # st.write("Notice %:", notice_pct)
    # st.write("Notice % Loss:", notice_pct_loss)
    # st.write("Low Severity %:", low_severity_pct)
    # st.write("Medium Severity %:", med_severity_pct)
    # st.write("High Severity %:", high_severity_pct)

    ########################################################################################################################################################

    with st.container(border=True):
        col13, col14, col15, col16,_,_ = st.columns(6)
        deal_count = col13.number_input("Deal Count", value=100)
        DV_range = 25  # Initial value for DV_range in millions
        DV_range_input = col14.number_input("DV Range Increment (millions)", value=DV_range, step=1)
        DV_range = DV_range_input * 1000000  # Convert to actual value
        col14.text(f"Current Value: {DV_range:,}")

    ########################################################################################################################################################   

    with st.container(border=True):
        col17, col18, col19, col20, col21, col22 = st.columns(6)



        sme_low_DV = col17.number_input("Select SME DV Min", min_value=1000000, max_value=99999999, value=10000000, step=DV_range)
        col17.text(f"Current Value: {sme_low_DV:,}")
        sme_upper_DV = col18.number_input("Select SME DV Max", min_value=sme_low_DV + DV_range, max_value=100000000, value=75000000, step=DV_range)
        col18.text(f"Current Value: {sme_upper_DV:,}")
        mm_low_DV = col19.number_input("Select MM DV Min", min_value=50000000, max_value=999999999, value=75000000, step=DV_range)
        col19.text(f"Current Value: {mm_low_DV:,}")
        mm_upper_DV = col20.number_input("Select MM DV Max", min_value=mm_low_DV + DV_range, max_value=1000000000, value=750000000, step=DV_range)
        col20.text(f"Current Value: {mm_upper_DV:,}")
        j_low_DV = col21.number_input("Select J DV Min", min_value=500000000, max_value=9999999999, value=750000000, step=DV_range)
        col21.text(f"Current Value: {j_low_DV:,}")
        j_upper_DV = col22.number_input("Select J DV Max", min_value=j_low_DV + DV_range, max_value=10000000000, value=5000000000, step=DV_range)
        col22.text(f"Current Value: {j_upper_DV:,}")

        # Empty columns to fill the space as per instruction, but not used for inputs
        # col18, col19, col20 are placeholders for future expansion or to maintain the layout

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
        pricing_range = col21.number_input("Pricing Range", value=0.005, format="%.3f")
        sme_pricing_low, sme_pricing_high = col22.slider("Select SME Pricing Range", min_value=0.01, max_value=0.02, value=(0.012, 0.0145), step=pricing_range, format="%.3f")
        mm_pricing_low, mm_pricing_high = col23.slider("Select MM Pricing Range", min_value=0.01, max_value=0.02, value=(0.0135, 0.0165), step=pricing_range, format="%.3f")
        j_pricing_low, j_pricing_high = col24.slider("Select J Pricing Range", min_value=0.03, max_value=0.08, value=(0.035, 0.075), step=pricing_range, format="%.3f")

    # pricing_list = pricing_generator(DV_list, limit_list, attachment_pt_list, primary_xs_list, pricing_range, sme_pricing_low, sme_pricing_high, mm_pricing_low, mm_pricing_high, j_pricing_low, j_pricing_high)

    def w(string):
        st.write(string)

    # w(f'procong list:{pricing_list}')
    # notice_list = notice_generator(deal_count, notice_pct, notice_pct_loss, low_severity_pct, med_severity_pct, high_severity_pct)
    # w(f'notice list: {notice_list}')

    with st.container(border=True):
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

            performance_stats = []
            average_rol_list = []

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
                average_rol_list.append(df['RoL'].mean())

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

            # Dummy delta values
            delta_percentage_above_0 = "+0.5%"
            delta_percentage_above_1m = "-0.2%"
            delta_percentage_above_10m = "+1.2%"
            delta_average_performance = "+1000"
            delta_max_performance = "-500"
            delta_min_performance = "+200"
            # delta_average_rol = "+0.1%"

            col1, _ = st.columns(2)

            with col1.container(border=True):
                col1_1, col1_2, col1_3 = st.columns(3)
                with col1_1:
                    st.metric(label="Pct. of scenarios above 0m", value=f"{percentage_above_0*100:.2f}%", delta=delta_percentage_above_0)
                with col1_2:
                    st.metric(label="Pct. of scenarios above 1m", value=f"{percentage_above_1m*100:.2f}%", delta=delta_percentage_above_1m)
                with col1_3:
                    st.metric(label="Pct. of scenarios above 10m", value=f"{percentage_above_10m*100:.2f}%", delta=delta_percentage_above_10m)
            

            col1, _ = st.columns(2)
            with col1.container(border=True):
                col2_1, col2_2, col2_3 = st.columns(3)
                with col2_1:
                    st.metric(label="Average", value=f"{average_performance:,.0f}", delta=delta_average_performance)
                with col2_2:
                    st.metric(label="Max", value=f"{max_performance:,.0f}", delta=delta_max_performance)
                with col2_3:
                    st.metric(label="Min", value=f"{min_performance:,.0f}", delta=delta_min_performance)


            col1, col2, _ = st.columns(3)
            with col1.container(border=True):
                average_rate_on_line = np.mean(average_rol_list) * 100
                st.metric(label="Average Rate On Line", value=f"{average_rate_on_line:,.2f}%")
            with col2.container(border=True):
                if option in mapping_dict:
                    total_n = mapping_dict[option]
                    cr_adjusted_rate = (average_rate_on_line + (average_rate_on_line * total_n))
                    st.metric(label="CR Adjusted Rate", value=f"{cr_adjusted_rate:.2f}%")
                else:
                    st.write("Selected country is not in the mapping dictionary.")

            div()
            w(df)
            w(average_rol_list)
            
            # Clearing messages after completion
            process_message.empty()
            section_message.empty()

            # Reset progress bar after completion
            progress_bar.empty()

    # w(f'Frozen: 09-04-2024')
    # st.header('Frozen: 09-04-2024')