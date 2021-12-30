#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import pandas as pd


# In[ ]:


# Assumptions
# - people.csv doesn't contain duplicate people (ex. John Smith & John Smith are different)
# - paytrace_transactions.csv rows are in chronological order from top to bottom (most recent last)

# read in CSV files
# na_filter=False means fill empty cells with "" instead of "NaN"
df_people = pd.read_csv('people.csv', header=0, na_filter=False)
df_transactions = pd.read_csv('transactions.csv', header=0, na_filter=False)
df_ptransactions = pd.read_csv('paytrace_transactions.csv', header=0, na_filter=False)
#df_duplicate_accounts = pd.read_csv('duplicate_accounts.csv', header=0, na_filter=False)
#df_misc = pd.read_csv('misc_transactions.csv', header=0, na_filter=False)


# In[ ]:


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
               "scholarship_fund":"Donate to Diversity Scholarship",
               "legislative_fund":"Donate to Legislative Fund",
}
# dictionary of US state abbreviations
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


# In[ ]:


# table of people's names (unique)
# df_people
# table of transactions (names may repeat)
# df_transactions
# table of paytrace transactions (names may repeat)
#df_ptransactions


# In[ ]:


def capitalize_name(first, middle, last):
    """Fixes name capitalization
    
    :param first: the first name
    :param middle: the middle name
    :param last: the last name
    
    :return: 3 strings. correctly capitalized first, middle, and last name
    
    >> capitalize_name("JOHN","k","SMITH")
    "John", "K", "Smith"
    """
    names = [first, middle, last]
    for i in range(len(names)):
        temp = ""
        if len(names[i])>0:
            temp = names[i][0].upper()
        if len(names[i])>1:
            temp += names[i][1:].lower()
        names[i] = temp
    return names[0], names[1], names[2]


# In[ ]:


def get_name(billing_name):
    """Parse name from the Paytrace "Billing Name" field
    
    :param billing_name: Paytrace Billing Name string
    - `username@email.com-Firstname Lastname`
    - email or name may be missing: `usename@email.com-None` or `Firstname Lastname`
    
    :return: 2 strings. first and last name
    
    >> get_name("johndeere@email.com-John Deere")
    "John", "Deere"
    """
    firstlast = billing_name.split("-")[-1]
    if(" " in firstlast):
        name_arr = firstlast.split()
        # dropping middle name
        # first and last capitalized
        name_arr[0] = name_arr[0][0].upper() + name_arr[0][1:].lower()
        name_arr[-1] = name_arr[-1][0].upper() + name_arr[-1][1:].lower()
        return name_arr[0], name_arr[-1]
    
    return "", ""

def get_recur(invoice):
    """Get recurring payment information from Paytrace "Invoice" field
    
    :param: invoice field (`01/01/2021 1of999` or may be empty)
    
    :return: string. recurring payment info (XofXXX)
    
    >>> get_recur("01/01/2021 1of999")
    "1of999"
    """
    if invoice != "":
        return invoice.split()[-1]
    return ""


# In[ ]:


def parse_row(row, label_dict):
    """read row entries and into corresponding variables
    """
    
    first_name = ""
    last_name = ""
    # ptrans
    if "name" in label_dict.keys():
        first_name, last_name = get_name(row[label_dict['name']])
    # trans
    elif "first" in label_dict.keys() and "last" in label_dict.keys():
        first_name = row[label_dict['first']]
        last_name = row[label_dict['last']]
    else:
        print("ERROR: could not get name")
        exit(-1)

    ##### TODO #####
    # if recurring != '' getrecur(invoice) # 
    # need to always update record with recurring info if they submit one recurring and one single # 
    recurring = ""
    # ptrans
    if "recurring" in label_dict.keys():
        recurring = get_recur(row[label_dict["recurring"]])

    email = ""
    # ptrans
    if "email" in label_dict.keys():
        email=row[label_dict["email"]]

    amt = row[label_dict["amt"]]
    # ptrans
    if "$" in str(amt):
        amt = float(amt[1:])
    
    legpercent = 1.0
    scholpercent = 0.0
    
    if "legislative_fund" in label_dict.keys():
    
        legpercent_str = str(row[label_dict["legislative_fund"]])
        # ptrans
        if "%" in legpercent_str:
            legpercent = float(legpercent_str.strip()[:-1])/100
    
    if "scholarship_fund" in label_dict.keys():
    
        scholpercent_str = str(row[label_dict["scholarship_fund"]])
        # ptrans
        if "%" in scholpercent_str:
            scholpercent = float(scholpercent_str.strip()[:-1])/100
    
        
    return first_name, last_name, recurring, email, float(amt), legpercent, scholpercent


# In[ ]:


def update_donation_totals(mergedTable, append_cols, data):
    if "recur_payment" in append_cols and "recur_amt" in append_cols and "total_amt_leg" in append_cols and "total_amt_schol" in append_cols: # ptrans
        # last cols are total, recurring, recur amt, total amount leg, total amount schol
        mergedTable[-1][-5] += float(data["amt"])
        mergedTable[-1][-4] = data["recurring"]
        mergedTable[-1][-3] = 0.0 if data["recurring"] == "" else data["amt"]
        mergedTable[-1][-2] += data["amt"] - (data["scholpercent"] * data["amt"])
        mergedTable[-1][-1] += data["scholpercent"] * data["amt"]
    elif "total_amount" in append_cols: # trans
        # last col is total
        mergedTable[-1][-1] += data["amt"]


# In[ ]:


def merge(df_base, dict_base, df2, dict2, append_cols):
    """Merge transactions from a dataframe into a base dataframe
    
    :param df_base:     base dataframe to merge into (probably a list of people)
    :param dict_base:   dictionary of column labels fordf_base
    :param df2:         dataframe to merge into df_base (probably a list of transactions)
    :param dict2:       dictionary of column labels for df2
    :param append_cols: column names to be appended to the base dataframe
    
    :return:            2D array. the merged table
    """
    mergedTable = []
    saved = []
    # create a column to keep track of which rows in df2 were counted
    if 'Counted' not in df2.columns:
        df2['Counted'] = [""] * len(df2)
    
    # for each person in the base table
    for i, row in df_base.iterrows():
        # create an entry in the final table
        tempList = list(row)
        
        # convert state name to abbreviation
        if(tempList[-1] in us_state_abbrev.keys()):
            tempList[-1] = us_state_abbrev[tempList[-1]]
        
        # append new columns
        if "total_amount" in append_cols:
            tempList.append(0.0)
        if "recur_payment" in append_cols:
            tempList.append("")
        if "recur_amt" in append_cols:
            tempList.append(0.0)
        if "total_amt_leg" in append_cols:
            tempList.append(0.0)
        if "total_amt_schol" in append_cols:
            tempList.append(0.0)
        
        mergedTable.append(tempList)
        
        # for each element in df2
        for j, row2 in df2.iterrows():
            
            first_name, last_name, recurring, email, amt, legpercent, scholpercent = parse_row(row2, dict2)
            if email == None:
                print(j, row2)
            
            ##### merge record into mergedTable
            if ((row[dict_base['last']]==last_name and
                row[dict_base['first']]==first_name and 
                first_name != "" and
                last_name != ""
               ) or (email != "" and
                     row[dict_base['email']].lower()==email.lower() 
                    )) and row2['Counted'] != "y":
                
                if 'email' not in dict_base.keys() or (row[dict_base['email']].lower()!=email.lower() and email != ""):
                    base_email = row[dict_base['email']] if 'email' in dict_base.keys() else ""
                    base_state = row[dict_base['state']] if 'email' in dict_base.keys() else ""
                    state2 = row2[dict2['state']] if 'state' in dict2.keys() else ""
                    ans = input(f"Is {row[dict_base['first']]} {row[dict_base['last']]} {base_email} ({base_state}) the same person as"
                        + f" {first_name} {last_name} {email} ({state2}) ? [y/N]\n")
                   # if df_duplicate_accounts.isin([email]).any().any()==True
                        #pass
                    #else:
                
                    # TODO: if user says they are the same person, save this info
                    # Example: Jeff Carroll is Jeffrey Carroll in the people table
                    if(ans.lower() == 'y'):
                        save_entry = [row[dict_base['first']], row[dict_base['last']], 
                                      base_email, base_state, 
                                      first_name, last_name, email, state2
                                     ]
                        saved.append(save_entry)
                        #df_duplicate_accounts.append(save_entry)
                    # otherwise, don't count this transaction
                    else:
                        #this skips to the next iteration of the for loop
                        continue
                
                # update donation totals
                update_donation_totals(mergedTable, append_cols, {"amt": amt, 
                                                                  "recurring": recurring, 
                                                                  "legpercent": legpercent, 
                                                                  "scholpercent": scholpercent})
            
                df2.at[j,'Counted'] = "y"

    count = sum(df2['Counted'] != "y")
    if count > 0:
        print("\nNOTE: {} rows were not merged/counted!\n".format(count))
    else:
        print("\nConsolidation successful.")
        
    return mergedTable
#saved_df.to_csv('saved_df')


# In[ ]:


# merge transactions.csv into people.csv
mergedTable = merge(df_people, dict_people, df_transactions, dict_trans, append_cols=["total_amount"])


# In[ ]:


### merge the uncounted transactions (by people who are not in people.csv)
uncounted_trans = df_transactions.loc[df_transactions['Counted'] != "y"]

dict_uncounted_people = dict([(key, dict_trans[key]) for key in dict_trans.keys() if key in ['first','last','email','state']])
uncounted_people = uncounted_trans.loc[:,[dict_trans[key] for key in dict_uncounted_people.keys()]].drop_duplicates()

# match format of the people table (with better labels):
dict_merged = {"first":"first",
               "middle": "middle",
               "last":"last",
               "email":"email",
               "member_type": "member type",
               "state": "state",
}
uncounted_people.rename(columns={dict_trans[k]:dict_merged[k] for k in dict_uncounted_people.keys()},inplace=True)
for c in dict_merged.keys():
    if c not in uncounted_people.columns:
        dict_uncounted_people[c] = c
        uncounted_people[dict_uncounted_people[c]] = [""]*len(uncounted_people)
uncounted_people= uncounted_people.reindex(columns=dict_merged.keys())
dict_uncounted_people = dict_merged


# In[ ]:


unregistered_people_merged = merge(uncounted_people, dict_uncounted_people, uncounted_trans, dict_trans, append_cols=["total_amount"])
mergedTable += unregistered_people_merged
df_merged = pd.DataFrame(mergedTable, columns=list(dict_merged.keys())+['total amount'])


# In[ ]:


# merge ptransactions.csv into the merged table
finalTable = merge(df_merged, dict_merged, df_ptransactions, dict_ptrans, append_cols=["recur_payment", "recur_amt", "total_amt_leg", "total_amt_schol"])


# In[ ]:


### merge the uncounted paytrace transactions (people who are not in people.csv)
uncounted_ptrans = df_ptransactions.loc[df_ptransactions['Counted'] != "y"]

dict_uncounted_people = dict([(key, dict_ptrans[key]) for key in dict_ptrans.keys() if key in ['first','middle','last','email','member_type','state']])
uncounted_people = uncounted_ptrans.loc[:,[dict_ptrans[key] for key in dict_uncounted_people.keys()]].drop_duplicates()
uncounted_people.rename(columns={dict_uncounted_people[key]:dict_merged[key] for key in dict_uncounted_people.keys()},inplace=True)
for c in df_merged.columns:
    if c not in uncounted_people.columns:
        dict_uncounted_people[c] = c
        if c == "total amount":
            newcol = [0.0]*len(uncounted_people)
        else:
            newcol = [""]*len(uncounted_people)
        uncounted_people[dict_uncounted_people[c]] = newcol
uncounted_people= uncounted_people.reindex(columns=list(df_merged.columns))
dict_uncounted_people = dict_merged
dict_uncounted_people["total amount"] = "total amount"


# In[ ]:


unregistered_people_merged = merge(uncounted_people, dict_uncounted_people, uncounted_ptrans, dict_ptrans, append_cols=["recur_payment", "recur_amt", "total_amt_leg", "total_amt_schol"])

finalTable += unregistered_people_merged

labels = list(df_merged.columns) # use the same columns as the merged df
labels += ['recurring payment', 'recurring amt', 'total amount leg', 'total amount schol']

df_final = pd.DataFrame(finalTable, columns=labels)


# In[ ]:


# get a table with only donors
df_donors = df_final[df_final['total amount'] > 0]


# In[ ]:


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


# In[ ]:


# turn tag list into string to look pretty
for row in taggedTable:
    row[-1] = ", ".join(row[-1])


# In[ ]:


# turn the table into a df

labels = list(df_final.columns) # use the same columns as the merged df
labels.append('Tags')

df_tagged = pd.DataFrame(taggedTable, columns=labels)
df_tagged


# In[ ]:


# export it as a CSV
df_tagged.to_csv('donation_totals.csv')

