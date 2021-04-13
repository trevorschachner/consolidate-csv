# Consolidate CSVs

## Dictionaries

Different CSV files might have different names for the columns. We'll set up dictionaries for the CSV files at the top so this can be taken care of at the beginning and not cause changes throughout the code.

A dictionary is basically a lookup table. Its entries are pairs, called key-value pairs. For example:

|Key |Value|
|:---|:----|
|Apple|fruit|
|Banana|fruit|
|Cucumber|vegetable|

The way we'll use this is to standardize the column names. We know the data will have first names and last names. So we'll always refer to those columns as `first` and `last`, and use a dictionary to translate it into the actual name in the CSV file. For example:

| Key | Value|
|:----|:-----|
|first|FirstName|
|last |LastName|

Say the data from the CSV file is in the DataFrame `df`. We want to get the first name column. However, the columns are labeled based on their original names in the CSV file. From the example above, say their names are `FirstName` and `LastName`. (Another CSV file may instead use different names, like `first_name` and `last_name`, but we want to avoid having to change all the time and always use our convention: `first` and `last`.) What we'll do is enter the column names from the CSV file into a dictionary for that CSV file, which encapsulates the table above; call it `dict`. Here is how we write it in code:

```
dict = {"first":"FirstName", "last":"LastName"}
```

Notice that the entries are separated by commas, and the notation is `key : value`. The `{` and `}` make it a dictionary instead of an array or something else. Now when we access the data frame, we use square brackets. We'll get the names of the columns from the dictionary as `dict["first"]` ("look up the value for the key `"first"`, which is a string") and `dict["last"]`. Now we have the names of the Data Frame columns, so we can ask the Data Frame for those columns: `df[dict["first"]]` and `df[dict["last"]]`:

```
df[dict["first"]]
= df["FirstName"]
```

### Function

Python:
```
def get_first_name(df):
    return df[dict["first"]]
```

Java:
```
int get_first_name(DataFrame df) {
    return df[dict["first"]];
}
```