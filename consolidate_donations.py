#!/usr/bin/env python
# coding: utf-8

# In[315]:


import pandas as pd


# In[368]:


# read in CSV files
# na_filter=False means fill empty cells with "" instead of "NaN"

# Assumptions
# - people.csv doesn't contain duplicate people (ex. John Smith & John Smith are different)
# - paytrace_transactions.csv rows are in chronological order from top to bottom (most recent last)

df_people = pd.read_csv('people.csv', header=0, na_filter=False)
df_transactions = pd.read_csv('transactions.csv', header=0, na_filter=False)
df_ptransactions = pd.read_csv('paytrace_transactions.csv', header=0, na_filter=False)


# In[369]:


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
dict_merged = {"first":"first",
               "middle": "middle",
               "last":"last",
               "email":"email",
               "member_type": "member type",
               "state": "state",
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


# In[374]:


# table of people's names (unique)
#df_people
# table of transactions (names may repeat)
#df_transactions
# table of paytrace transactions (names may repeat)
#df_ptransactions


# In[372]:


# TODO - CREATE LIST OF NON-UNIQUE NAMES IN CASE THERE ARE DUPLICATES IN THE PEOPLE TABLE


# In[371]:


# new_emails = []
# for i, row in df_people.iterrows():
#     new_emails.append(row[dict_people['email']].lower())
# df_people[dict_people['email']] = new_emails
    
# new_emails = []
# for i, row in df_ptransactions.iterrows():
#     new_emails.append(row[dict_ptrans['email']].lower())
# df_ptransactions[dict_ptrans['email']] = new_emails


# In[373]:


# set up variables
mergedTable = []
# create a list to keep track of which transactions were counted
counted = [""] * len(df_transactions)

# for each person in the people table
for i, row_people in df_people.iterrows():

    # create an entry in the final table
    tempList = list(row_people)
    tempList[-1] = us_state_abbrev[tempList[-1]]

    tempList.append(0) # with a total donation amount of 0
    mergedTable.append(tempList)

    # for each transaction
    for j, row_trans in df_transactions.iterrows():

        # if the first and last name matches the current person
        if row_people[dict_people['last']]==row_trans[dict_trans['last']] and row_people[dict_people['first']]==row_trans[dict_trans['first']] and counted[j]!="y":
            
################################################################################################################################################################################################
            # if the middle name doesn't match exactly, check with the user
#             if row_people[dict_people['middle']]!=row_trans[dict_trans['middle']]:
#             ans = input(f"Is {row_people[dict_people['first']]} {row_people[dict_people['middle']]} {row_people[dict_people['last']]} ({row_people[dict_people['state']]}) the same person as"
#                         + f" {row_trans[dict_trans['first']]} {row_trans[dict_trans['last']]} ({row_trans[dict_trans['company']]}) ? [y/N]\n")
            # if user says they aren't the same person, don't count this transaction
#             if(ans.lower() != 'y'):
#                 # this skips to the next iteration of the for loop
#                 continue

            #print("{} + {}".format(finalList[-1], row2[dict_transactions["amt"]]))
################################################################################################################################################################################################
    
    
            # add the transaction amount to the person's total donations
            mergedTable[-1][-1]+=row_trans[dict_trans["amt"]]
            counted[j] = "y"


# In[333]:


# Track any donors not in df_people and add to mergedTable

if(counted != ["y"] * len(df_transactions)):
    print("\nNOTE: some transactions were not counted!\n")
    df_transactions['Counted'] = counted
    count = 0
    for i, row in df_transactions.iterrows():
        if row['Counted'] != "y":
            count+=1
            print(f"{row[dict_trans['last']]}, {row[dict_trans['first']]}, ${row[dict_trans['amt']]}, {row[dict_trans['company']]}")
            uncountedPerson = [row[dict_trans['first']], "", row[dict_trans['last']],"", "", "", row[dict_trans['amt']]]
            mergedTable.append(uncountedPerson)
    print("\nTotal: {}".format(count))
else:
    print("\nConsolidation successful.")


# In[334]:


# turn the list of donation totals into a table

labels = ['first','middle','last','email','member type','state']
labels.append('total amount')
df_merged = pd.DataFrame(mergedTable, columns=labels)


# In[335]:


# function to get name from string format
def get_name(name):
    # format example:
    # username@email.com-Firstname Lastname
    # email or name may be missing
    # usename@email.com-None
    # Firstname Lastname
    firstlast = name.split("-")[-1]
    if(" " in firstlast):
        name_arr = firstlast.split()
        # dropping middle name
        # first and last capitalized
        name_arr[0] = name_arr[0][0].upper() + name_arr[0][1:]
        name_arr[-1] = name_arr[-1][0].upper() + name_arr[-1][1:]
        return name_arr[0], name_arr[-1]
    
    return "", ""

# first, last = get_name("johndeere@email.com-John Deere")

# function to get recurring info from string
def get_recur(invoice):
    # format example:
    # 01/01/2021 1of999
    # may be empty
    if invoice != "":
        return invoice.split()[-1]
    return ""
    
# get_recur("01/01/2021 1of999")


# In[360]:


finalTable = []
# create a list to keep track of which transactions were counted
counted = [""] * len(df_ptransactions)

# for each person in the people table
for i, row_merged in df_merged.iterrows():

    # create an entry in the final table
    # first, middle, last, email, member type, state, total amount
    tempList = list(row_merged)
    # recurring payment, recurring amt
    tempList += ["", 0.0]
    finalTable.append(tempList)

    # for each transaction
    for j, row_ptrans in df_ptransactions.iterrows():

        # if the first and last name matches the current person
        first_name, last_name = get_name(row_ptrans[dict_ptrans['name']])
        recurring = get_recur(row_ptrans[dict_ptrans["recurring"]])
        email=row_ptrans[dict_ptrans["email"]]
        amt = float(row_ptrans[dict_ptrans["amt"]][1:])
        
        if (row_merged[dict_merged['last']]==last_name and row_merged[dict_merged['first']]==first_name                 and first_name!= "" and last_name!= "")                 or (row_merged[dict_merged['email']].lower()==email.lower())                 and counted[j]!="y":
            
            if row_merged[dict_merged['email']].lower()!=email.lower():
                ans = input(f"Is {row_merged[dict_merged['first']]} {row_merged[dict_merged['last']]} {row_merged[dict_merged['email']]} ({row_merged[dict_merged['state']]}) the same person as"
                        + f" {first_name} {last_name} {email} ({row_ptrans[dict_ptrans['state']]}) ? [y/N]\n")
                # if user says they aren't the same person, don't count this transaction
                if(ans.lower() != 'y'):
                    #this skips to the next iteration of the for loop
                    continue
                        
            # add to donation total
            finalTable[-1][-3]+=amt
            # add recurring payment info
            finalTable[-1][-2]=recurring
            # add recurring payment amount
            finalTable[-1][-1] = 0.0 if recurring == "" else amt
            
            counted[j] = "y"


# In[361]:


# Track any recuring donors not in df_people and add to finalTable

if(counted != ["y"] * len(df_ptransactions)):
    print("\nNOTE: some transactions were not counted!\n")
    df_ptransactions['Counted'] = counted
    count = 0
    
    for i, row in df_ptransactions.iterrows():
        if row['Counted'] != "y":
            count+=1
            print(f"{row[dict_ptrans['name']]}, {row[dict_ptrans['email']]}, {row[dict_ptrans['amt']]}, {row[dict_ptrans['recurring']]}")
            
            first_name, last_name = get_name(row[dict_ptrans['name']])
            recurring = get_recur(row[dict_ptrans["recurring"]])
            amt = float(row[dict_ptrans["amt"]][1:])
            email=row[dict_ptrans["email"]]
            
            uncountedTrans = [first_name, "", last_name, 
                              email, "",
                              row[dict_ptrans['state']], 
                              amt,
                              recurring,
                              0.0 if recurring == "" else amt,
                             ]
            
            finalTable.append(uncountedTrans)
    print("\nTotal: {}".format(count))
    
else:
    print("\nConsolidation successful.")


# In[362]:


# turn the table into a df

labels = list(df_merged.columns) # use the same columns as the merged df
labels += ['recurring payment', 'recurring amt']

df_final = pd.DataFrame(finalTable, columns=labels)


# In[363]:


# remove all non-donors from df_donors
df_donors = df_final[df_final['total amount'] > 0]


# In[364]:


# Tag and assign to club based on donation and recurring donation amount
taggedTable = []

# for each person in the donor table
for i, row_donors in df_donors.iterrows():

    #create an entry in the final table
    #first, middle, last, email, member type, state, total amount, recurring payment, recurring amt
    tempList = list(row_donors)
    tempList.append([])
    taggedTable.append(tempList)
    
    #Look at total amount and tag accordingly
    if row_donors['total amount'] >= 1000: 
        taggedTable[-1][-1].append('Presidents Club Platinum')
    elif row_donors['total amount'] >= 500:
        taggedTable[-1][-1].append('Presidents Club Gold')
        
    #TODO - ADD MORE DONATION LEVLES HERE
    #elif row_donors['total amount']>= : 
       # taggedTable[-1][-1]=""
        
   #Look at recuring donation amount and tag accordingly
    if float(row_donors['recurring amt']) > 83.32:
        taggedTable[-1][-1].append('Presidents Club Platinum Sustainer')
        
    elif float(row_donors['recurring amt']) > 41.66:
        taggedTable[-1][-1].append('Presidents Club Gold Sustainer')  
        
    #TODO - ADD SUSTAINER LEVELS
    #if row_donors['recurring amt']>25.00:
        #taggedTable[-1][-1].append("INSTERT TITLE HERE")


# In[365]:


# turn tag list into string to look pretty
for row in taggedTable:
    row[-1] = ", ".join(row[-1])


# In[366]:


# turn the table into a df

labels = list(df_final.columns) # use the same columns as the merged df
labels.append('Tags')

df_tagged = pd.DataFrame(taggedTable, columns=labels)
# df_tagged


# In[367]:


# export it as a CSV
df_tagged.to_csv('donation_totals.csv')


# ## Dictionaries
# 
# Different CSV files might have different names for the columns. We'll set up dictionaries for the CSV files at the top so this can be taken care of at the beginning and not cause changes throughout the code.
# 
# A dictionary is basically a lookup table. Its entries are pairs, called key-value pairs. For example:
# 
# |Key |Value|
# |:---|:----|
# |Apple|fruit|
# |Banana|fruit|
# |Cucumber|vegetable|
# 
# The way we'll use this is to standardize the column names. We know the data will have first names and last names. So we'll always refer to those columns as `first` and `last`, and use a dictionary to translate it into the actual name in the CSV file. For example:
# 
# | Key | Value|
# |:----|:-----|
# |first|FirstName|
# |last |LastName|
# 
# Say the data from the CSV file is in the DataFrame `df`. We want to get the first name column. However, the columns are labeled based on their original names in the CSV file. From the example above, say their names are `FirstName` and `LastName`. (Another CSV file may instead use different names, like `first_name` and `last_name`, but we want to avoid having to change all the time and always use our convention: `first` and `last`.) What we'll do is enter the column names from the CSV file into a dictionary for that CSV file, which encapsulates the table above; call it `dict`. Here is how we write it in code:
# 
# ```
# dict = {"first":"FirstName", "last":"LastName"}
# ```
# 
# Notice that the entries are separated by commas, and the notation is `key : value`. The `{` and `}` make it a dictionary instead of an array or something else. Now when we access the data frame, we use square brackets. We'll get the names of the columns from the dictionary as `dict["first"]` ("look up the value for the key `"first"`, which is a string") and `dict["last"]`. Now we have the names of the Data Frame columns, so we can ask the Data Frame for those columns: `df[dict["first"]]` and `df[dict["last"]]`:
# 
# ```
# df[dict["first"]]
# = df["FirstName"]
# ```
# 
# ### Function
# 
# Python:
# ```
# def get_first_name(df):
#     return df[dict["first"]]
# ```
# 
# Java:
# ```
# int get_first_name(DataFrame df) {
#     return df[dict["first"]]
# }
# ```
