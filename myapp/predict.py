from sqlalchemy import create_engine
import pandas as pd
from mlxtend.preprocessing import TransactionEncoder
from mlxtend.frequent_patterns import apriori
from mlxtend.frequent_patterns import association_rules

engine = create_engine("mysql+mariadbconnector://user:password@host:port/database_name")

QLoanParcel = "SELECT * FROM LoanParcel"
QLoanDurable = "SELECT * FROM LoanDurable"

dfParcel = pd.read_sql(QLoanParcel, engine)
dfDurable = pd.read_sql(QLoanDurable, engine)

dfParcel = dfParcel.drop(["id", "date_add", "start_date", "description", "reasonfromstaff", "status", 
                          "type", "quantity", "statusParcel", "quantitytype", "nameposition", "parcel_item_id"], axis = 1)
dfDurable = dfDurable.drop(["id", "date_add", "start_date", "end_date", "description", "reasonfromstaff", "status", 
                          "type", "quantity", "statusDurable", "quantitytype", "nameposition", "durable_item_id"], axis = 1)

df = pd.concat([dfParcel, dfDurable], axis=0)
#one_hot = pd.get_dummies(df, columns=['LoanParcel', 'LoanDurable'])
#frequent_item_sets = apriori(one_hot, min_support=0.5, use_colnames=True)
#association_rules = association_rules(frequent_item_sets, metric="lift", min_threshold=1.0)
#add_parcel_rules = association_rules[association_rules['antecedents'].apply(lambda x: 'Add_Parcel' in x)]

te = TransactionEncoder()
te_array = te.fit(df.groupby('user_id')['name'].apply(list)).transform(df.groupby('user_id')['name'].apply(list))
df = pd.DataFrame(te_array, columns=te.columns_)
freq_item = apriori(df, min_support=0.3, use_colnames=True)
rules = association_rules(freq_item, metric="confidence", min_threshold=0.6)
add_parcel_rules = rules[rules['antecedents'].apply(lambda x: 'Add_Parcel' in x)]
print(add_parcel_rules)
