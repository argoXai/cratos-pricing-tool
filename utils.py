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