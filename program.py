from sampler import sampler
import requests
from openpyxl import Workbook
from openpyxl.styles import Font, Color
from sqlalchemy import create_engine
import random
import sys

print(sampler.sample_group)
print(sampler.population_group)

print("Beginning A/B Testing...")

clean_population = sampler.concat([sampler.sample_group, sampler.population_group]).drop_duplicates(keep=False)

print(clean_population)

holdvar = '''
print("Gathering test data...")
testgroup = sampler.obtain_testgroup(sampler.testgroup)
testoutlets = []
for i in testgroup[1]:
    if i not in testoutlets:
        testoutlets.append(i[0])
outlets = []
results = []
for i in range(len(testgroup[1])):
    outlets.append(testgroup[1][i][0])
    results.append(testgroup[1][i][1])
testresults = dict(zip(outlets, results))
print("Test data obtained!")
print("Gathering population data...")
populationgroup = sampler.obtain_population(sampler.population)
print("Population data obtained!")
print("Cleaning population...")
outlets = []
results = []
for i in range(len(populationgroup[1])):
    outlets.append(populationgroup[1][i][0])
    results.append(populationgroup[1][i][1])
sampleresults = dict(zip(outlets, results))
popoutlets = []
for i in populationgroup[1]:
    if i not in popoutlets:
        popoutlets.append(i[0])
print("Population cleaned!")
'''
print("Comparing population with test data...")
print("\n ------------------------ \n")
#Remove the sample outlets from the population:
print("Number of outlets in population: " + str(len(popoutlets)))
for outlet in testoutlets:
    if outlet in popoutlets:
        popoutlets.remove(outlet)
print("Number of outlets in sample: " + str(len(testoutlets)))
print("After removing sample outlets from population data: " + str(len(popoutlets)))
print("\n ------------------------ \n")
print("Beginning Random Sampling of Population")

samplesgroups = sampler.random_numbers(popoutlets, len(popoutlets), len(testoutlets))
testgroup = [testoutlets]

print("\n ------------------------ \n")
#Begin attrition testing
print("Compiling Test Results")
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











