from requests.sessions import session
from sqlalchemy import create_engine, MetaData, inspect, Table, Column, Integer, String, Float, Date, select, and_, func
import pandas as pd
import datetime



meta = MetaData()
engine = create_engine('postgresql://afliegel:DA0qvgWxn6fNW9oVaHfk@192.168.1.150:5432/agility_prod')
conn = engine.connect()

tables = engine.table_names()

#Define a SQL Alchemy Table off a existing database
transactions = Table(
   'transactions', meta, 
   Column('id', Integer, primary_key = True), 
   Column('debit_amount', Float), 
   Column('credit_amount', Float), 
   Column('acct_id', Date), 
   Column('txn_date', Date), 
)

#Define queries to gather the test group and population group
test_group = select([transactions.c.id, transactions.c.debit_amount - transactions.c.credit_amount]).where(and_(transactions.c.acct_id==52, transactions.c.txn_date>='2021-10-01'
                    , transactions.c.txn_date>='2021-10-31')).order_by(transactions.c.id)

population_group = select([transactions.c.id, transactions.c.debit_amount - transactions.c.credit_amount]).where(and_(transactions.c.acct_id==52)).order_by(transactions.c.id)


sample_group = pd.read_sql(test_group, conn)
population_group = pd.read_sql(population_group, conn)

from sampler import Sampler
import sys

sampler = Sampler()

data = sampler.random_sampling(population_group, sample_group)

print(data)

sys.exit()

print("Beginning A/B Testing...")
print("Cleaning population data...")
totpop = str(len(sampler.population_group))

clean_population = pd.concat([sampler.sample_group, sampler.population_group]).drop_duplicates(keep=False)

print("Population data cleaned!")
print("Comparing population with test data...")
print("\n ------------------------ \n")
#Remove the sample outlets from the population:
print("Number of outlets in test group: " + str(len(sampler.sample_group)))
print("Number of outlets in population: " + totpop)
print("After removing sample outlets from population data: " + str(len(clean_population)))
print("\n ------------------------ \n")
print("Beginning Random Sampling of Population")
samplesgroups = sampler.random_numbers_pandas(clean_population, len(clean_population), len(sampler.sample_group))
print("\n ------------------------ \n")
#Begin testing
print("Compiling Test Results")

##Implement in Class based system for better functionality from this point forward

for i in len(samplesgroups):
    if sampler.analysis_type == 'Average':
        samplesgroups[i]


testgroup = [testoutlets]


#testattritiondata = sampler.attritionmodeling(populationgroup, testgroup)
testattritiondata = sampler.attritionmodelingdict(testresults, testgroup)
print("Test results compiled")
print("Compiling Sample Results")
sampleattritiondata = sampler.attritionmodelingdict(sampleresults, samplesgroups)
#sampleattritiondata = sampler.attritionmodeling(populationgroup, samplesgroups)
print("Sample results compiled")
print("\n ------------------------ \n")

testkeys = sampler.dictkeylist(testattritiondata)
samplekeys = sampler.dictkeylist(sampleattritiondata)
allkeys = testkeys + samplekeys
cleankeys = []
for key in allkeys:
    if key not in cleankeys:
            cleankeys.append(key)
cleankeys.sort()

print("Loading results into Excel file")

sampler.importExcel(cleankeys, testattritiondata, sampleattritiondata)

print("File saved to " + sampler.filepath + "!")
print("Exiting A/B Tester")











