import os
import pandas as pd
from mlxtend.preprocessing import TransactionEncoder
from mlxtend.frequent_patterns import apriori, association_rules

df = pd.read_csv("myapp/Recommend.csv", encoding="utf-8")

te = TransactionEncoder()
te_array = te.fit(df.groupby('user_id')['name'].apply(list)).transform(df.groupby('user_id')['name'].apply(list))
df = pd.DataFrame(te_array, columns=te.columns_)
freq_item = apriori(df, min_support=0.3, use_colnames=True)
rules = association_rules(freq_item, metric="confidence", min_threshold=0.6)

#one_hot = pd.get_dummies(df, columns=['LoanParcel', 'LoanDurable'])
#frequent_item_sets = apriori(one_hot, min_support=0.5, use_colnames=True)
#association_rules = association_rules(frequent_item_sets, metric="lift", min_threshold=1.0)
#add_parcel_rules = association_rules[association_rules['antecedents'].apply(lambda x: 'Add_Parcel' in x)]