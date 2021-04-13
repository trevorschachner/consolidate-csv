#!/usr/bin/env python
# coding: utf-8

# In[20]:


import pandas as pd


# In[21]:


# read in CSV files
# na_filter=False means fill empty cells with "" instead of "NaN"

# Assumptions
# - people.csv doesn't contain duplicate people (ex. John Smith & John Smith are different)
# - paytrace_transactions.csv rows are in chronological order from top to bottom (most recent last)

df_people = pd.read_csv('people.csv', header=0, na_filter=False)
df_transactions = pd.read_csv('transactions.csv', header=0, na_filter=False)
df_ptransactions = pd.read_csv('paytrace_transactions.csv', header=0, na_filter=False)
df_misc = pd.read_csv('misc_transactions.csv', header=0, na_filter=False)


# In[2]:


# dictionaries of csv column labels
# lookup name : name in CSV
dict_people = {"last": "[Name | Last]", 
               "first": "[Name | First]", 
               "middle": "[Name | Middle]", 
               "email": "[Email | Primary]",
               "state": "[Address | Primary | State]", 
               "member_type":"[Member Type]",
}
dict_trans = {"last": "Last Name", 
              "first": "First Name", 
              "amt": "Amount",
              "company": "Company",
}
dict_ptrans = {"name":"Billing_Name",
               "recurring": "Invoice",
               "state": "Billing_State",
               "amt": "Amount",
               "email": "User",
}
us_state_abbrev = {
    'Alabama': 'AL','Alaska': 'AK','American Samoa': 'AS','Arizona': 'AZ','Arkansas': 'AR',
    'California': 'CA','Colorado': 'CO','Connecticut': 'CT','Delaware': 'DE','District of Columbia': 'DC',
    'Florida': 'FL','Georgia': 'GA','Guam': 'GU','Hawaii': 'HI','Idaho': 'ID','Illinois': 'IL',
    'Indiana': 'IN','Iowa': 'IA','Kansas': 'KS','Kentucky': 'KY','Louisiana': 'LA','Maine': 'ME',
    'Maryland': 'MD','Massachusetts': 'MA','Michigan': 'MI','Minnesota': 'MN','Mississippi': 'MS',
    'Missouri': 'MO','Montana': 'MT','Nebraska': 'NE','Nevada': 'NV','New Hampshire': 'NH',
    'New Jersey': 'NJ','New Mexico': 'NM','New York': 'NY','North Carolina': 'NC','North Dakota': 'ND',
    'Northern Mariana Islands':'MP','Ohio': 'OH','Oklahoma': 'OK','Oregon': 'OR','Pennsylvania': 'PA',
    'Puerto Rico': 'PR','Rhode Island': 'RI','South Carolina': 'SC','South Dakota': 'SD',
    'Tennessee': 'TN','Texas': 'TX','Utah': 'UT','Vermont': 'VT',
    'Virgin Islands': 'VI','Virginia': 'VA','Washington': 'WA','West Virginia': 'WV',
    'Wisconsin': 'WI','Wyoming': 'WY','':'',
}


# In[23]:


# table of people's names (unique)
#df_people
# table of transactions (names may repeat)
#df_transactions
# table of paytrace transactions (names may repeat)
#df_ptransactions


# In[29]:


# function to get name from string format
# ----------------------------------------
# format example:
#     username@email.com-Firstname Lastname
#     email or name may be missing
#     usename@email.com-None
#     Firstname Lastname
# example usage:
#     first, last = get_name("johndeere@email.com-John Deere")
def get_name(name):
    firstlast = name.split("-")[-1]
    if(" " in firstlast):
        name_arr = firstlast.split()
        # dropping middle name
        # first and last capitalized
        name_arr[0] = name_arr[0][0].upper() + name_arr[0][1:]
        name_arr[-1] = name_arr[-1][0].upper() + name_arr[-1][1:]
        return name_arr[0], name_arr[-1]
    
    return "", ""

# function to get recurring info from string
# ----------------------------------------
# format example:
#     01/01/2021 1of999
#     may be empty
# example usage:
#     get_recur("01/01/2021 1of999")
def get_recur(invoice):
    if invoice != "":
        return invoice.split()[-1]
    return "" 


# In[ ]:


# read row entries and into corresponding variables
def parse_row(row, label_dict):
    first_name = ""
    last_name = ""
    # ptrans
    if "name" in label_dict.keys():
        first_name, last_name = get_name(row[label_dict['name']])
    # trans
    elif "first" in label_dict.keys() and "last" in label_dict.keys():
        first_name = row2[dict2['first']]
        last_name = row2[dict2['last']]
    else:
        print("ERROR: could not get name")
        exit(-1)

    recurring = False
    # ptrans
    if "recurring" in label_dict.keys():
        recurring = get_recur(row[label_dict["recurring"]])

    email = ""
    # ptrans
    if "email" in label_dict.keys():
        email=row[label_dict["email"]]

    amt = row[label_dict["amt"]]
    # ptrans
    if "$" in amt:
        amt = float(amt[1:])
        
    return first_name, last_name, recurring, email, amt


# In[6]:


##################################################################
# @param df_base :     base dataframe to merge into
#                      (probably a list of people)
# @param dict_base :   dictionary of column labels fordf_base
# @param df2 :         dataframe to merge into df_base
#                      (probably a list of transactions)
# @param dict2 :       dictionary of column labels for df2
# @param append_cols : column names to be appended to the 
#                      base dataframe
# @returns 2D array representing the merged table
##################################################################
def merge(df_base, dict_base, df2, dict2, append_cols):
    mergedTable = []
    # create a list to keep track of which rows in df2 were counted
    counted = [""] * len(df2)
    
    # for each person in the base table
    for i, row in df_base.iterrows():
        # create an entry in the final table
        tempList = list(row)
        
        # convert state name to abbreviation
        if(tempList[-1] in us_state_abbrev.keys()):
            tempList[-1] = us_state_abbrev[tempList[-1]]
        
        # append new columns
        if "total_amt" in append_cols:
            tempList.append(0)
        if "recur_payment" in append_cols:
            tempList.append("")
        if "recur_amt" in append_cols:
            tempList.append(0.0)
        
        mergedTable.append(tempList)
        
        # for each element in df2
        for j, row2 in df2.iterrows():
            
            first_name, last_name, recurring, email, amt = parse_row(row2, dict2)
            
            ##### merge record into mergedTable
            if (row[dict_base['last']]==last_name and row[dict_base['first']]==first_name                     and first_name != "" and last_name != "")                 or (row[dict_base['email']].lower()==email.lower()                     and email != "")                 and counted[j]!="y":
                
                if row[dict_base['email']].lower()!=email.lower() and email != "":
                    ans = input(f"Is {row[dict_base['first']]} {row[dict_base['last']]} {row[dict_base['email']]} ({row[dict_base['state']]}) the same person as"
                        + f" {first_name} {last_name} {email} ({row2[dict2['state']]}) ? [y/N]\n")
                
                    # if user says they are the same person, save this info
                    if(ans.lower() == 'y'):
                        save_entry = [row[dict_base['first']], row[dict_base['last']], 
                                      row[dict_base['email']], row[dict_base['state']], 
                                      first_name, last_name, email, row2[dict2['state']]
                                     ]
                        saved.append(save_entry)
                        # TODO consult saved entries before asking user    
                    # otherwise, don't count this transaction
                    else:
                        #this skips to the next iteration of the for loop
                        continue
                
                # update donation totals
                if "recur_payment" in append_cols and "recur_amt" in append_cols: # ptrans
                    # last 3 cols are total, recurring, recur amt
                    mergedTable[-1][-3] += amt
                    mergedTable[-1][-2]=recurring
                    mergedTable[-1][-1] = 0.0 if recurring == "" else amt
                else: # trans
                    # last col is total
                    mergedTable[-1][-1] += amt
            
                counted[j] = "y"

    # track any rows from df2 not added to df_base
    if(counted != ["y"] * len(df2)):
        print("\nNOTE: some rows were not merged/counted!\n")
        df_2['Counted'] = counted
        count = 0
        for i, row in df2.iterrows():
            if row['Counted'] != "y":
                count+=1
                
                first_name, last_name, recurring, email, amt = parse_row(row, dict2)
                state = ""
                if "state" in dict2.keys():
                    state = row[dict2['state']]
                    
                uncounted = [first_name, "", last_name,
                             email, "", 
                             state,
                             amt]
                if "recur_payment" in append_cols and "recur_amt" in append_cols: # ptrans
                    uncounted += [recurring, 0.0 if recurring == "" else amt]
                #print(uncounted)
                mergedTable.append(uncounted)
                
        print("\nTotal: {}".format(count))
        print("These have been appended to the end of the merged table.")
    else:
        print("\nConsolidation successful.")
        
    return mergedTable


# In[ ]:


# merge transactions.csv into people.csv
mergedTable = merge(df_people, dict_people, df_transactions, dict_trans, append_cols=["total_amount"])

labels = ['first','middle','last','email','member type','state']
labels.append('total amount')
dict_merged = {"first":"first",
               "middle": "middle",
               "last":"last",
               "email":"email",
               "member_type": "member type",
               "state": "state",
}

df_merged = pd.DataFrame(mergedTable, columns=labels)


# In[ ]:


# merge ptransactions.csv into the merged table
finalTable = merge(df_merged, dict_merged, df_ptransactions, dict_ptrans, append_cols=["recur_payment", "recur_amt"])

labels = list(df_merged.columns) # use the same columns as the merged df
labels += ['recurring payment', 'recurring amt']

df_final = pd.DataFrame(finalTable, columns=labels)


# In[34]:


# get a table with only donors
df_donors = df_final[df_final['total amount'] > 0]


# In[35]:


# Tag and assign to club based on donation and recurring donation amount
taggedTable = []

# for each person in the donor table
for i, row_donors in df_donors.iterrows():

    # create an entry in the final table
    # first, middle, last, email, member type, state, total amount, recurring payment, recurring amt
    tempList = list(row_donors)
    tempList.append([])
    taggedTable.append(tempList)
    
    # Look at total amount and tag accordingly
    if row_donors['total amount'] >= 1000: 
        taggedTable[-1][-1].append('Presidents Club Platinum')
    elif row_donors['total amount'] >= 500:
        taggedTable[-1][-1].append('Presidents Club Gold')
        
   # Look at recuring donation amount and tag accordingly
    if float(row_donors['recurring amt']) > 100.00:
        taggedTable[-1][-1].append('Super Sustainer')
        
    elif float(row_donors['recurring amt']) > 50.00:
        taggedTable[-1][-1].append('Presidents Club Sustainer')  
        
    elif float(row_donors['recurring amt']) > 25.00:
        taggedTable[-1][-1].append('Fellow Sustainer')
        
    elif float(row_donors['recurring amt']) > 10.00:
        taggedTable[-1][-1].append('Student Sustainer')


# In[36]:


# turn tag list into string to look pretty
for row in taggedTable:
    row[-1] = ", ".join(row[-1])


# In[37]:


# turn the table into a df

labels = list(df_final.columns) # use the same columns as the merged df
labels.append('Tags')

df_tagged = pd.DataFrame(taggedTable, columns=labels)
#df_tagged


# In[38]:


# export it as a CSV
df_tagged.to_csv('donation_totals.csv')


# In[ ]:




