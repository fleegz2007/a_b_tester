import requests
import logic
from openpyxl import Workbook
from openpyxl.styles import Font, Color
import config
import random
import sys
import pandas as pd

print("Beginning A/B Testing...")
print("Gathering test data...")
testgroup = logic.obtain_testgroup(config.testgroup)
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
populationgroup = logic.obtain_population(config.population)
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

samplesgroups = logic.random_numbers(popoutlets, len(popoutlets), len(testoutlets))
testgroup = [testoutlets]

print("\n ------------------------ \n")
#Begin attrition testing
print("Compiling Test Results")
#testattritiondata = logic.attritionmodeling(populationgroup, testgroup)
testattritiondata = logic.attritionmodelingdict(testresults, testgroup)
print("Test results compiled")
print("Compiling Sample Results")
sampleattritiondata = logic.attritionmodelingdict(sampleresults, samplesgroups)
#sampleattritiondata = logic.attritionmodeling(populationgroup, samplesgroups)
print("Sample results compiled")
print("\n ------------------------ \n")

testkeys = logic.dictkeylist(testattritiondata)
samplekeys = logic.dictkeylist(sampleattritiondata)
allkeys = testkeys + samplekeys
cleankeys = []
for key in allkeys:
    if key not in cleankeys:
            cleankeys.append(key)
cleankeys.sort()

print("Loading results into Excel file")

logic.importExcel(cleankeys, testattritiondata, sampleattritiondata)

print("File saved to " + config.filepath + "!")
print("Exiting A/B Tester")











