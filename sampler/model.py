from requests.sessions import session
from sqlalchemy import create_engine, MetaData, inspect, Table, Column, Integer, String, Float, Date, select, and_, func
import pandas as pd
import datetime
import sampler

meta = MetaData()
engine = create_engine(sampler.engine)
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
test_group = select([transactions.c.id, transactions.c.debit_amount - transactions.c.credit_amount]).where(and_(transactions.c.acct_id==52, transactions.c.txn_date>='2021-10-01', transactions.c.txn_date>='2021-10-31'))

population_group = select([transactions.c.id, transactions.c.debit_amount - transactions.c.credit_amount]).where(and_(transactions.c.acct_id==52))


sample_group = pd.read_sql(test_group, conn)
population_group = pd.read_sql(population_group, conn)
