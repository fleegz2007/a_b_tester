import requests
import foundryapi
from openpyxl import Workbook
from openpyxl.styles import Font, Color
import config
import random
import sys
import pandas as pd

for i in range(1000):
    num = i*2
    print(str(num))

print("Beginning A/B Testing...")
print("Gathering test data...")
testgroup = foundryapi.obtain_testgroup(config.testgroup)
testoutlets = []
for i in testgroup[1]:
    if i not in testoutlets:
        testoutlets.append(i[0])
print("Test data obtained!")
print("Gathering population data...")
populationgroup = foundryapi.obtain_population(config.population)
outlets = []
results = []
for i in range(len(populationgroup[1])):
    outlets.append(populationgroup[1][i][0])
    results.append(populationgroup[1][i][1])
results = dict(zip(outlets, results))
popoutlets = []
for i in populationgroup[1]:
    if i not in popoutlets:
        popoutlets.append(i[0])
print("Population data obtained!")
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

samplesgroups = foundryapi.random_numbers(popoutlets, len(popoutlets), len(testoutlets))
testgroup = [testoutlets]

print("\n ------------------------ \n")
#Begin attrition testing
print("Compiling Test Results")
#testattritiondata = foundryapi.attritionmodeling(populationgroup, testgroup)
testattritiondata = foundryapi.attritionmodelingdict(results, testgroup)
print("Test results compiled")
print("Compiling Sample Results")
sampleattritiondata = foundryapi.attritionmodelingdict(results, samplesgroups)
print("Sample results compiled")
print("\n ------------------------ \n")

testkeys = foundryapi.dictkeylist(testattritiondata)
samplekeys = foundryapi.dictkeylist(sampleattritiondata)
allkeys = testkeys + samplekeys
cleankeys = []
for key in allkeys:
    if key not in cleankeys:
            cleankeys.append(key)
cleankeys.sort()

print("Loading results into Excel file")


wb = Workbook()
ws = wb.active
ws.title = "SourceData"
for y in range(len(cleankeys)):
    ws.cell(row=1, column=y+1).value = cleankeys[y]
for x in range(len(testattritiondata[0])):
    try:
        ws.cell(row=2, column=x+1).value = testattritiondata[0][int(ws.cell(row=1, column=x+1).value)]
    except:
        continue
for x in range(len(sampleattritiondata)):
    for y in range(len(sampleattritiondata[x])):
        try:
            ws.cell(row=x+3, column=y+1).value = sampleattritiondata[x][int(ws.cell(row=1, column=y+1).value)]
        except:
            continue
wb.save(filename = config.filepath)

print("File saved to " + config.filepath + "!")
print("Exiting A/B Tester")











