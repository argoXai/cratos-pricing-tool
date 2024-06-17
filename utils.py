import numpy as np
import pandas as pd
import random
import math
from random import randrange
from datetime import datetime


def severity_generator(notice_pct_dist, notice_pct_loss_dist, severity_dist):
    notice_pct = np.random.choice(notice_pct_dist)
    notice_pct_loss = np.random.choice(notice_pct_loss_dist)
    low_severity_pct = np.random.choice(severity_dist)
    med_high_severity_pct_generator = np.random.random(1)[0]
    med_severity_pct = (1 - low_severity_pct) * (med_high_severity_pct_generator)
    high_severity_pct = (1 - low_severity_pct) * (1-med_high_severity_pct_generator)
    
    return notice_pct, notice_pct_loss, low_severity_pct, med_severity_pct, high_severity_pct

def DV_generator(deal_count, DV_range, sme_low_DV, sme_upper_DV, mm_low_DV, mm_upper_DV, sme_pct, mm_pct, j_pct, j_low_DV, j_upper_DV):
    DV_list = []
    sme_count = int(deal_count*sme_pct)
    mm_count = int(deal_count*mm_pct)
    j_count = int(deal_count*j_pct)
    for x in range(sme_count):
        DV_list.append(random.randrange(sme_low_DV, sme_upper_DV, DV_range)) 
    for x in range(mm_count):
        DV_list.append(random.randrange(mm_low_DV, mm_upper_DV, DV_range)) 
    for x in range(j_count):
        DV_list.append(random.randrange(j_low_DV, j_upper_DV, DV_range))  
    if (sme_count + mm_count + j_count) != deal_count:
        for i in range(deal_count - len(DV_list)):
            x = random.randrange(1, 4)
            if x == 1:
                DV_list.append(random.randrange(sme_low_DV, sme_upper_DV, DV_range)) 
            if x == 2:
                DV_list.append(random.randrange(mm_low_DV, mm_upper_DV, DV_range))
            if x == 3:
                DV_list.append(random.randrange(j_low_DV, j_upper_DV, DV_range))
    random.shuffle(DV_list)
    
    return DV_list

def structure_generator(DV_list, low_limit, upper_limit, limit_range, primary_pct, xs_pct, pri_attachment_pt_range):
    primary_xs_list = []
    for dv in DV_list:
        if dv > 750_000_000:
            x = np.random.choice([0, 1], size=1, p=[primary_pct, xs_pct])
            primary_xs_list.append(x[0])
        else:
            primary_xs_list.append(0)
            
    tower_limit_list = []
    for value in DV_list:
        tower_limit_list.append(random.randrange(value*.1, value*.2, 500_000)) 
    
    limit_list = []
    for index, tower_limit in enumerate(tower_limit_list):
        policy_limit = random.randrange(low_limit, upper_limit, limit_range)
        if policy_limit >= tower_limit_list[index]:
            policy_limit = tower_limit_list[index]
            limit_list.append(policy_limit)
        if policy_limit < tower_limit_list[index]:
            limit_list.append(policy_limit) 
        
    attachment_pt_list = []        
    for index, pri_v_xs in enumerate(primary_xs_list):
        if pri_v_xs == 0:
            y = np.random.choice(pri_attachment_pt_range, size=1)
            attachment_pt_list.append(y[0])
        if pri_v_xs == 1:
            layer_num = int(tower_limit_list[index] // limit_list[index])
            y = np.random.choice(pri_attachment_pt_range, size=1)
            z = y + ((random.randrange(1, layer_num+1)*limit_list[index])/DV_list[index])
            attachment_pt_list.append(z[0])

    return limit_list, attachment_pt_list, primary_xs_list

def pricing_generator(DV_list, limit_list, attachment_pt_list, primary_xs_list, pricing_range, sme_pricing_low, sme_pricing_high, mm_pricing_low, mm_pricing_high, j_pricing_low, j_pricing_high):
    pricing_list = []
    for index, DV in enumerate(DV_list):
        if DV > 9_999_999 and DV < 75_000_001:
            pricing_list.append(round(random.uniform(sme_pricing_low, sme_pricing_high), 4)) 
        if DV > 75_000_000 and DV < 750_000_001:
            pricing_list.append(round(random.uniform(mm_pricing_low, mm_pricing_high), 4)) 
        if DV > 750_000_000 and primary_xs_list[index] == 1:
            attachment_pt = DV_list[index] * attachment_pt_list[index]
            ilf_mult = int(attachment_pt // limit_list[index]) 
            ilf_np_array = np.random.choice(np.arange(.75, .85, .025), size=ilf_mult)
            ilf = np.prod(ilf_np_array)
            xs_pricing = ilf * round(random.uniform(mm_pricing_low, mm_pricing_high), 4)
            pricing_list.append(xs_pricing)
        if DV > 750_000_000 and primary_xs_list[index] == 0:
            pricing_list.append(round(random.uniform(j_pricing_low, j_pricing_high), 4)) 

    return pricing_list

def notice_generator(deal_count, notice_pct, notice_pct_loss, low_severity_pct, med_severity_pct, high_severity_pct):
    notice_list = []
    for x in range(int(deal_count*notice_pct*notice_pct_loss)):
        notice_list.append(1)
    for x in range(int(deal_count*notice_pct*notice_pct_loss*low_severity_pct)):
        notice_list.append(2)
    for x in range(int(deal_count*notice_pct*notice_pct_loss*med_severity_pct)):
        notice_list.append(3)
    for x in range(int(deal_count*notice_pct*notice_pct_loss*high_severity_pct)):
        notice_list.append(4)
    for x in range(int(deal_count*(1-notice_pct))):
        notice_list.append(0)
    if deal_count - len(notice_list) > 0:
        for x in range(deal_count - len(notice_list)):
            notice_list.append(randrange(5))
    if deal_count - len(notice_list) < 0:
        for x in range(abs(deal_count - len(notice_list))):
            notice_list.pop(randrange(len(notice_list)))
    random.shuffle(notice_list)
    
    return notice_list 

def loss_generator(notice_list, limit_list, low_low_severity_loss, low_high_severity_loss, med_low_severity_loss, med_high_severity_loss):
    loss_list = []
    high_low_severity_loss = 10_000_000
    for index, notice in enumerate(notice_list):
        if notice == 0:
            loss_list.append(0) 
        if notice == 1:
            loss_list.append(0) 
        if notice == 2:
            loss_list.append(random.randrange(low_low_severity_loss, low_high_severity_loss)) 
        if notice == 3:
            loss_list.append(random.randrange(med_low_severity_loss, med_high_severity_loss))
        if notice == 4:
            if limit_list[index] > 10_000_000:
                loss_list.append(random.randrange(high_low_severity_loss, limit_list[index]))
            else:
                loss_list.append(random.randrange(high_low_severity_loss, 10_000_001))
    
    return loss_list

def performance(df):
    if df['Attachment_Pt'] - df['Loss_Amount'] >= 0:
            df['Performance'] = df['Premium']
    if df['Attachment_Pt'] - df['Loss_Amount'] <= 0:
        df['Performance'] = df['Premium'] + df['Attachment_Pt'] - df['Loss_Amount']
    return df['Performance']

def df_generator(DV_list,pricing_list,attachment_pt_list,notice_list,loss_list,limit_list):
    data_tuples = list(zip(DV_list,pricing_list,attachment_pt_list,notice_list,loss_list,limit_list))
    df = pd.DataFrame(data_tuples, columns=['DV','RoL','Attachment_Pt_Pct','Notice','Loss_Amount','Limit'])
    df['Premium'] = df['Limit'] * df['RoL']
    df['Attachment_Pt'] = df['DV']*df['Attachment_Pt_Pct']
    df['Performance'] = df.apply(performance, axis=1)
    return df


mapping_dict = {
    'Austria': 0.359,
    'Belgium': 0.277,
    'Bulgaria ': 1.0,
    'Croatia': 0.948,
    'Cyprus': 0.715,
    'Czech Republic': 0.51,
    'Denmark': 0.0,
    'Estonia': 0.415,
    'Finland': 0.129,
    'France': 0.399,
    'Germany': 0.157,
    'Greece': 0.883,
    'Hungary': 0.86,
    'Italy': 0.602,
    'Latvia': 0.804,
    'Lithuania': 0.555,
    'Luxembourg': 0.281,
    'Netherlands': 0.036,
    'Norway': 0.127,
    'Poland': 0.662,
    'Portugal': 0.548,
    'Republic of Ireland': 0.098,
    'Romania': 0.902,
    'Slovakia': 0.928,
    'Slovenia': 0.765,
    'Spain': 0.452,
    'Sweden': 0.023,
    'United Kingdom': 0.305
}

# industry_mapping = {
#     'Misc. Fabricated Products': ['Basic Materials', None, None, None, None],
#     'Fabricated Plastic & Rubber': ['Basic Materials', None, None, None, None],
#     'Containers & Packaging': ['Basic Materials', None, None, None, None],
#     'Metal Mining': ['Basic Materials', None, None, None, None],
#     'Gold & Silver': ['Basic Materials', None, None, None, None],
#     'Chemical Manufacturing': ['Basic Materials', None, None, None, None],
#     'Iron & Steel': ['Basic Materials', None, None, None, None],
#     'Non-Metallic Mining': ['Basic Materials', None, None, None, None],
#     'Chemicals - Plastics & Rubber': ['Basic Materials', None, None, None, None],
#     'Paper & Paper Products': ['Basic Materials', None, None, None, None],
#     'Forestry & Wood Products': ['Basic Materials', None, None, None, None],
#     'Mobile Homes & RVs': ['Capital Goods', None, None, None, None],
#     'Aerospace & Defense': ['Capital Goods', None, None, None, None],
#     'Misc. Capital Goods': ['Capital Goods', None, None, None, None],
#     'Constr. & Agric. Machinery': ['Capital Goods', None, None, None, None],
#     'Construction Services': ['Capital Goods', None, None, None, None],
#     'Construction - Raw Materials': ['Capital Goods', None, None, None, None],
#     'Constr. - Supplies & Fixtures': ['Capital Goods', None, None, None, None],
#     'Conglomerates': ['Conglomerates', None, None, None, None],
#     'Appliance & Tool': ['Consumer Cyclical', None, None, None, None],
#     'Auto & Truck Manufacturers': ['Consumer Cyclical', None, None, None, None],
#     'Recreational Products': ['Consumer Cyclical', None, None, None, None],
#     'Auto & Truck Parts': ['Consumer Cyclical', None, None, None, None],
#     'Apparel/Accessories': ['Consumer Cyclical', None, None, None, None],
#     'Jewelry & Silverware': ['Consumer Cyclical', None, None, None, None],
#     'Footwear': ['Consumer Cyclical', None, None, None, None],
#     'Furniture & Fixtures': ['Consumer Cyclical', None, None, None, None],
#     'Textiles - Non Apparel': ['Consumer Cyclical', None, None, None, None],
#     'Audio & Video Equipment': ['Consumer Cyclical', None, None, None, None],
#     'Tires': ['Consumer Cyclical', None, None, None, None],
#     'Photography': ['Consumer Cyclical', None, None, None, None],
#     'Beverages (Alcoholic)': ['Consumer Non-Cyclical', None, None, None, None],
#     'Food Processing': ['Consumer Non-Cyclical', None, None, None, None],
#     'Office Supplies': ['Consumer Non-Cyclical', None, None, None, None],
#     'Personal & Household Products': ['Consumer Non-Cyclical', None, None, None, None],
#     'Crops': ['Consumer Non-Cyclical', None, None, None, None],
#     'Beverages (Non-Alcoholic)': ['Consumer Non-Cyclical', None, None, None, None],
#     'Fish/Livestock': ['Consumer Non-Cyclical', None, None, None, None],
#     'Tobacco': ['Consumer Non-Cyclical', 0.0, None, None, None],
#     'Oil & Gas Operations': ['Energy', None, None, None, None],
#     'Oil Well Services & Equipment': ['Energy', None, None, None, None],
#     'Oil & Gas - Integrated': ['Energy', None, None, None, None],
#     'Coal': ['Energy', None, None, None, None],
#     'Alternative Energy': ['Energy', None, None, None, None],
#     'Insurance (Accident & Health)': ['Financial', None, None, None, None],
#     'Insurance (Prop. & Casualty)': ['Financial', None, None, None, None],
#     'Other (Mutual Fund)': ['Financial', None, None, None, None],
#     'Investment Services': ['Financial', None, None, None, None],
#     'S&Ls/Savings Banks': ['Financial', None, None, None, None],
#     'Insurance (Miscellaneous)': ['Financial', None, None, None, None],
#     'Misc. Financial Services': ['Financial', None, None, None, None],
#     'Money Center Banks': ['Financial', None, None, None, None],
#     'Consumer Financial Services': ['Financial', 1.0, 'Data Privacy', 'E&O ', 0.75],
#     'Insurance (Life)': ['Financial', None, None, None, None],
#     'Regional Banks': ['Financial', None, None, None, None],
#     'Healthcare Facilities': ['Healthcare', None, None, None, None],
#     'Medical Equipment & Supplies': ['Healthcare', None, None, None, None],
#     'Biotechnology & Drugs': ['Healthcare', None, None, None, None],
#     'Major Drugs': ['Healthcare', None, None, None, None],
#     'Business Services': ['Services', None, None, None, None],
#     'Waste Management Services': ['Services', None, None, None, None],
#     'Communications Services': ['Services', None, None, None, None],
#     'Real Estate Operations': ['Services', 1.0, 'Property & Planning Matters', 'Condition of the Property', 0.0],
#     'Broadcasting & Cable TV': ['Services', None, None, None, None],
#     'Restaurants': ['Services', None, None, None, None],
#     'Printing & Publishing': ['Services', None, None, None, None],
#     'Retail (Drugs)': ['Services', None, None, None, None],
#     'Casinos & Gaming': ['Services', None, None, None, None],
#     'Retail (Specialty)': ['Services', None, None, None, None],
#     'Retail & Repair (Automotive)': ['Services', None, None, None, None],
#     'Personal Services': ['Services', None, None, None, None],
#     'Recreational Activities': ['Services', None, None, None, None],
#     'Motion Pictures': ['Services', None, None, None, None],
#     'Rental & Leasing': ['Services', None, None, None, None],
#     'Retail (Apparel)': ['Services', None, None, None, None],
#     'Schools': ['Services', None, None, None, None],
#     'Retail (Home Improvement)': ['Services', None, None, None, None],
#     'Retail (Department & Discount)': ['Services', None, None, None, None],
#     'Retail (Catalog & Mail Order)': ['Services', None, None, None, None],
#     'Hotels & Motels': ['Services', None, None, None, None],
#     'Security Systems & Services': ['Services', None, None, None, None],
#     'Advertising': ['Services', None, None, None, None],
#     'Printing Services': ['Services', None, None, None, None],
#     'Retail (Grocery)': ['Services', None, None, None, None],
#     'Retail (Technology)': ['Services', None, None, None, None],
#     'Semiconductors': ['Technology', None, None, None, None],
#     'Computer Hardware': ['Technology', None, None, None, None],
#     'Communications Equipment': ['Technology', None, None, None, None],
#     'Software & Programming': ['Technology', None, None, None, None],
#     'Computer Networks': ['Technology', None, None, None, None],
#     'Computer Services': ['Technology', None, None, None, None],
#     'Computer Peripherals': ['Technology', None, None, None, None],
#     'Electronic Instruments & Controls': ['Technology', None, None, None, None],
#     'Office Equipment': ['Technology', None, None, None, None],
#     'Computer Storage Devices': ['Technology', None, None, None, None],
#     'Scientific & Technical Instr.': ['Technology', None, None, None, None],
#     'Airline': ['Transportation', None, None, None, None],
#     'Railroads': ['Transportation', None, None, None, None],
#     'Misc. Transportation': ['Transportation', None, None, None, None],
#     'Trucking': ['Transportation', None, None, None, None],
#     'Air Courier': ['Transportation', None, None, None, None],
#     'Water Transportation': ['Transportation', None, None, None, None],
#     'Natural Gas Utilities': ['Utilities', None, None, None, None],
#     'Electric Utilities': ['Utilities', None, None, None, None],
#     'Water Utilities': ['Utilities', None, None, None, None]
# }

industry_mapping = {'Misc. Fabricated Products': ['Basic Materials', np.nan, np.nan, np.nan, 0.0],
 'Fabricated Plastic & Rubber': ['Basic Materials', np.nan, np.nan, np.nan, 0.0],
 'Containers & Packaging': ['Basic Materials', np.nan, np.nan, np.nan, 0.0],
 'Metal Mining': ['Basic Materials', np.nan, np.nan, np.nan, 0.0],
 'Gold & Silver': ['Basic Materials', np.nan, np.nan, np.nan, 0.0],
 'Chemical Manufacturing': ['Basic Materials', np.nan, np.nan, np.nan, 0.0],
 'Iron & Steel': ['Basic Materials', np.nan, np.nan, np.nan, 0.0],
 'Non-Metallic Mining': ['Basic Materials', np.nan, np.nan, np.nan, 0.0],
 'Chemicals - Plastics & Rubber': ['Basic Materials', np.nan, np.nan, np.nan, 0.0],
 'Paper & Paper Products': ['Basic Materials', np.nan, np.nan, np.nan, 0.0],
 'Forestry & Wood Products': ['Basic Materials', np.nan, np.nan, np.nan, 0.0],
 'Mobile Homes & RVs': ['Capital Goods', np.nan, np.nan, np.nan, 0.0],
 'Aerospace & Defense': ['Capital Goods', np.nan, np.nan, np.nan, 0.0],
 'Misc. Capital Goods': ['Capital Goods', np.nan, np.nan, np.nan, 0.0],
 'Constr. & Agric. Machinery': ['Capital Goods', np.nan, np.nan, np.nan, 0.0],
 'Construction Services': ['Capital Goods', np.nan, np.nan, np.nan, 0.0],
 'Construction - Raw Materials': ['Capital Goods', np.nan, np.nan, np.nan, 0.0],
 'Constr. - Supplies & Fixtures': ['Capital Goods', np.nan, np.nan, np.nan, 0.0],
 'Conglomerates': ['Conglomerates', np.nan, np.nan, np.nan, 0.0],
 'Appliance & Tool': ['Consumer Cyclical', np.nan, np.nan, np.nan, 0.0],
 'Auto & Truck Manufacturers': ['Consumer Cyclical', np.nan, np.nan, np.nan, 0.0],
 'Recreational Products': ['Consumer Cyclical', np.nan, np.nan, np.nan, 0.0],
 'Auto & Truck Parts': ['Consumer Cyclical', np.nan, np.nan, np.nan, 0.0],
 'Apparel/Accessories': ['Consumer Cyclical', np.nan, np.nan, np.nan, 0.0],
 'Jewelry & Silverware': ['Consumer Cyclical', np.nan, np.nan, np.nan, 0.0],
 'Footwear': ['Consumer Cyclical', np.nan, np.nan, np.nan, 0.0],
 'Furniture & Fixtures': ['Consumer Cyclical', np.nan, np.nan, np.nan, 0.0],
 'Textiles - Non Apparel': ['Consumer Cyclical', np.nan, np.nan, np.nan, 0.0],
 'Audio & Video Equipment': ['Consumer Cyclical', np.nan, np.nan, np.nan, 0.0],
 'Tires': ['Consumer Cyclical', np.nan, np.nan, np.nan, 0.001457725948],
 'Photography': ['Consumer Cyclical', np.nan, np.nan, np.nan, 0.0],
 'Beverages (Alcoholic)': ['Consumer Non-Cyclical', np.nan, np.nan, np.nan, 0.0],
 'Food Processing': ['Consumer Non-Cyclical', np.nan, np.nan, np.nan, 0.0],
 'Office Supplies': ['Consumer Non-Cyclical', np.nan, np.nan, np.nan, 0.0],
 'Personal & Household Products': ['Consumer Non-Cyclical',
  np.nan,
  np.nan,
  np.nan,
  0.0],
 'Crops': ['Consumer Non-Cyclical', np.nan, np.nan, np.nan, 0.0],
 'Beverages (Non-Alcoholic)': ['Consumer Non-Cyclical', np.nan, np.nan, np.nan, 0.0],
 'Fish/Livestock': ['Consumer Non-Cyclical', np.nan, np.nan, np.nan, 0.002915451895],
 'Tobacco': ['Consumer Non-Cyclical', 0.0, np.nan, np.nan, 0.0],
 'Oil & Gas Operations': ['Energy', np.nan, np.nan, np.nan, 0.1574344023],
 'Oil Well Services & Equipment': ['Energy', np.nan, np.nan, np.nan, 0.0],
 'Oil & Gas - Integrated': ['Energy', np.nan, np.nan, np.nan, 0.0],
 'Coal': ['Energy', np.nan, np.nan, np.nan, 0.0],
 'Alternative Energy': ['Energy', np.nan, np.nan, np.nan, 0.0],
 'Insurance (Accident & Health)': ['Financial', np.nan, np.nan, np.nan, 0.0],
 'Insurance (Prop. & Casualty)': ['Financial', np.nan, np.nan, np.nan, 0.0],
 'Other (Mutual Fund)': ['Financial', np.nan, np.nan, np.nan, 0.0],
 'Investment Services': ['Financial', np.nan, np.nan, np.nan, 0.3731778426],
 'S&Ls/Savings Banks': ['Financial', np.nan, np.nan, np.nan, 0.0],
 'Insurance (Miscellaneous)': ['Financial', np.nan, np.nan, np.nan, 0.0],
 'Misc. Financial Services': ['Financial', np.nan, np.nan, np.nan, 0.250728863],
 'Money Center Banks': ['Financial', np.nan, np.nan, np.nan, 0.1690962099],
 'Consumer Financial Services': ['Financial',
  1.0,
  'Data Privacy',
  'E&O ',
  0.1909620991],
 'Insurance (Life)': ['Financial', np.nan, np.nan, np.nan, 0.0],
 'Regional Banks': ['Financial', np.nan, np.nan, np.nan, 0.2346938776],
 'Healthcare Facilities': ['Healthcare', np.nan, np.nan, np.nan, 0.1851311953],
 'Medical Equipment & Supplies': ['Healthcare', np.nan, np.nan, np.nan, 0.3950437318],
 'Biotechnology & Drugs': ['Healthcare', np.nan, np.nan, np.nan, 1.0],
 'Major Drugs': ['Healthcare', np.nan, np.nan, np.nan, 0.0],
 'Business Services': ['Services', np.nan, np.nan, np.nan, 0.3206997085],
 'Waste Management Services': ['Services', np.nan, np.nan, np.nan, 0.0],
 'Communications Services': ['Services', np.nan, np.nan, np.nan, 0.2827988338],
 'Real Estate Operations': ['Services',
  1.0,
  'Property & Planning Matters',
  'Condition of the Property',
  0.0],
 'Broadcasting & Cable TV': ['Services', np.nan, np.nan, np.nan, 0.0],
 'Restaurants': ['Services', np.nan, np.nan, np.nan, 0.0],
 'Printing & Publishing': ['Services', np.nan, np.nan, np.nan, 0.001457725948],
 'Retail (Drugs)': ['Services', np.nan, np.nan, np.nan, 0.0],
 'Casinos & Gaming': ['Services', np.nan, np.nan, np.nan, 0.0],
 'Retail (Specialty)': ['Services', np.nan, np.nan, np.nan, 0.0],
 'Retail & Repair (Automotive)': ['Services', np.nan, np.nan, np.nan, 0.0],
 'Personal Services': ['Services', np.nan, np.nan, np.nan, 0.0],
 'Recreational Activities': ['Services', np.nan, np.nan, np.nan, 0.0],
 'Motion Pictures': ['Services', np.nan, np.nan, np.nan, 0.0],
 'Rental & Leasing': ['Services', np.nan, np.nan, np.nan, 0.0],
 'Retail (Apparel)': ['Services', np.nan, np.nan, np.nan, 0.0],
 'Schools': ['Services', np.nan, np.nan, np.nan, 0.0],
 'Retail (Home Improvement)': ['Services', np.nan, np.nan, np.nan, 0.0],
 'Retail (Department & Discount)': ['Services', np.nan, np.nan, np.nan, 0.0],
 'Retail (Catalog & Mail Order)': ['Services', np.nan, np.nan, np.nan, 0.0],
 'Hotels & Motels': ['Services', np.nan, np.nan, np.nan, 0.0],
 'Security Systems & Services': ['Services', np.nan, np.nan, np.nan, 0.0],
 'Advertising': ['Services', np.nan, np.nan, np.nan, 0.0],
 'Printing Services': ['Services', np.nan, np.nan, np.nan, 0.0],
 'Retail (Grocery)': ['Services', np.nan, np.nan, np.nan, 0.0],
 'Retail (Technology)': ['Services', np.nan, np.nan, np.nan, 0.0],
 'Semiconductors': ['Technology', np.nan, np.nan, np.nan, 0.2740524781],
 'Computer Hardware': ['Technology', np.nan, np.nan, np.nan, 0.0],
 'Communications Equipment': ['Technology', np.nan, np.nan, np.nan, 0.3542274052],
 'Software & Programming': ['Technology', np.nan, np.nan, np.nan, 0.9052478134],
 'Computer Networks': ['Technology', np.nan, np.nan, np.nan, 0.0],
 'Computer Services': ['Technology', np.nan, np.nan, np.nan, 0.3177842566],
 'Computer Peripherals': ['Technology', np.nan, np.nan, np.nan, 0.0],
 'Electronic Instruments & Controls': ['Technology',
  np.nan,
  np.nan,
  np.nan,
  0.1370262391],
 'Office Equipment': ['Technology', np.nan, np.nan, np.nan, 0.0],
 'Computer Storage Devices': ['Technology', np.nan, np.nan, np.nan, 0.0],
 'Scientific & Technical Instr.': ['Technology', np.nan, np.nan, np.nan, 0.0],
 'Airline': ['Transportation', np.nan, np.nan, np.nan, 0.0],
 'Railroads': ['Transportation', np.nan, np.nan, np.nan, 0.0],
 'Misc. Transportation': ['Transportation', np.nan, np.nan, np.nan, 0.0],
 'Trucking': ['Transportation', np.nan, np.nan, np.nan, 0.0],
 'Air Courier': ['Transportation', np.nan, np.nan, np.nan, 0.001457725948],
 'Water Transportation': ['Transportation', np.nan, np.nan, np.nan, 0.0],
 'Natural Gas Utilities': ['Utilities', np.nan, np.nan, np.nan, 0.0],
 'Electric Utilities': ['Utilities', np.nan, np.nan, np.nan, 0.1253644315],
 'Water Utilities': ['Utilities', np.nan, np.nan, np.nan, 0.0]}


parent_sectors = ['Basic Materials', 'Capital Goods', 'Conglomerates', 'Consumer Cyclical', 'Consumer Non-Cyclical', 'Energy', 'Financial', 'Healthcare', 'Services', 'Technology', 'Transportation', 'Utilities']

sector_dict = {
    'Basic Materials': ['Chemical Manufacturing', 'Chemicals - Plastics & Rubber', 'Containers & Packaging', 'Fabricated Plastic & Rubber', 'Forestry & Wood Products', 'Gold & Silver', 'Iron & Steel', 'Metal Mining', 'Misc. Fabricated Products', 'Non-Metallic Mining', 'Paper & Paper Products'],
    'Capital Goods': ['Aerospace & Defense', 'Constr. & Agric. Machinery', 'Constr. - Supplies & Fixtures', 'Construction - Raw Materials', 'Construction Services', 'Misc. Capital Goods', 'Mobile Homes & RVs'],
    'Conglomerates': ['Conglomerates'],
    'Consumer Cyclical': ['Appliance & Tool', 'Apparel/Accessories', 'Audio & Video Equipment', 'Auto & Truck Manufacturers', 'Auto & Truck Parts', 'Footwear', 'Furniture & Fixtures', 'Jewelry & Silverware', 'Photography', 'Recreational Products', 'Textiles - Non Apparel', 'Tires'],
    'Consumer Non-Cyclical': ['Beverages (Alcoholic)', 'Beverages (Non-Alcoholic)', 'Crops', 'Fish/Livestock', 'Food Processing', 'Office Supplies', 'Personal & Household Products', 'Tobacco'],
    'Energy': ['Alternative Energy', 'Coal', 'Oil & Gas - Integrated', 'Oil & Gas Operations', 'Oil Well Services & Equipment'],
    'Financial': ['Consumer Financial Services', 'Insurance (Accident & Health)', 'Insurance (Life)', 'Insurance (Miscellaneous)', 'Insurance (Prop. & Casualty)', 'Investment Services', 'Misc. Financial Services', 'Money Center Banks', 'Other (Mutual Fund)', 'Regional Banks', 'S&Ls/Savings Banks'],
    'Healthcare': ['Biotechnology & Drugs', 'Healthcare Facilities', 'Major Drugs', 'Medical Equipment & Supplies'],
    'Services': ['Advertising', 'Broadcasting & Cable TV', 'Business Services', 'Casinos & Gaming', 'Communications Services', 'Hotels & Motels', 'Motion Pictures', 'Personal Services', 'Printing & Publishing', 'Printing Services', 'Real Estate Operations', 'Recreational Activities', 'Rental & Leasing', 'Restaurants', 'Retail (Apparel)', 'Retail (Catalog & Mail Order)', 'Retail (Department & Discount)', 'Retail (Drugs)', 'Retail (Grocery)', 'Retail (Home Improvement)', 'Retail (Specialty)', 'Retail (Technology)', 'Retail & Repair (Automotive)', 'Schools', 'Security Systems & Services', 'Waste Management Services'],
    'Technology': ['Communications Equipment', 'Computer Hardware', 'Computer Networks', 'Computer Peripherals', 'Computer Services', 'Computer Storage Devices', 'Electronic Instruments & Controls', 'Office Equipment', 'Scientific & Technical Instr.', 'Semiconductors', 'Software & Programming'],
    'Transportation': ['Air Courier', 'Airline', 'Misc. Transportation', 'Railroads', 'Trucking', 'Water Transportation'],
    'Utilities': ['Electric Utilities', 'Natural Gas Utilities', 'Water Utilities']
}
