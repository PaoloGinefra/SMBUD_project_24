import pandas as pd


def sanitize_quotes(value):
    if isinstance(value, str):
        return value.replace('""', '"').replace('\\"', '"').rstrip('\\')
    return value


csvFilepath_recepies = './Dataset/recipes.csv'
csvFilepath_reviews = './Dataset/reviews.csv'
Neo4JImportPath = 'C:\\Users\\Paolo\\.Neo4jDesktop\\relate-data\\dbmss\\dbms-d410dbd9-acc1-4cc0-a8ac-271554bed9c8\\import\\'
nEntries = 10000


print('Loading data from ' + csvFilepath_recepies + '...')
recepies = pd.read_csv(csvFilepath_recepies)
print('Data loaded from ' + csvFilepath_recepies)

print('Sanitizing data...')
recepies = recepies.map(sanitize_quotes)
print('Data sanitized')

print('Data shape: ' + str(recepies.shape))

seed = 42
print('Shuffling data...')
recepies = recepies.sample(frac=1, random_state=seed).reset_index(drop=True)
print('Data shuffled')

splitData = recepies.iloc[:nEntries]
print('Data splited into shape: ' + str(splitData.shape))

outFileDir = Neo4JImportPath + 'recipes(' + str(nEntries) + ').csv'

print('Saving data to ' + outFileDir + '...')
splitData.to_csv(outFileDir, index=False)
print('Data saved to ' + outFileDir)


recepieIndices = splitData['RecipeId']

print('Loading data from ' + csvFilepath_reviews + '...')
reviews = pd.read_csv(csvFilepath_reviews)
print('Data loaded from ' + csvFilepath_reviews)

print('Sanitizing data...')
reviews = reviews.map(sanitize_quotes)
print('Data sanitized')

print('Data shape: ' + str(reviews.shape))

print('Filtering relevant reviews...')
relevantReviews = reviews[reviews['RecipeId'].isin(recepieIndices)]
print('Relevant reviews shape: ' + str(relevantReviews.shape))

outFileDir = Neo4JImportPath + 'reviews(' + str(nEntries) + ').csv'

print('Saving data to ' + outFileDir + '...')
relevantReviews.to_csv(outFileDir, index=False)
print('Data saved to ' + outFileDir)
