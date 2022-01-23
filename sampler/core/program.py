import pandas as pd

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
