import pandas as pd
from halo import Halo

spinner = Halo(text='Loading', spinner='dots')


def printSuccess(message):
    spinner.stop()
    print('\033[92m' + message + '\033[0m')


def printError(message):
    print('\033[91m' + message + '\033[0m')


def printStarting(message):
    print('\033[94m' + message + '\033[0m')
    spinner.start()


def sanitize_quotes(value):
    if isinstance(value, str):
        return value.replace('""', '"').replace('\\"', '"').rstrip('\\')
    return value


csvFilepath_recepies = './Dataset/recipes.csv'
csvFilepath_reviews = './Dataset/reviews.csv'
Neo4JImportPath = 'C:\\Users\\Paolo\\.Neo4jDesktop\\relate-data\\dbmss\\dbms-d410dbd9-acc1-4cc0-a8ac-271554bed9c8\\import\\'
nEntries = 10000


printStarting('Loading data from ' + csvFilepath_recepies + '...')
recepies = pd.read_csv(csvFilepath_recepies)
printSuccess('Data loaded from ' + csvFilepath_recepies)

printStarting('Sanitizing data...')
recepies = recepies.map(sanitize_quotes)
printSuccess('Data sanitized')

print('Data shape: ' + str(recepies.shape))

seed = 42
printStarting('Shuffling data...')
recepies = recepies.sample(frac=1, random_state=seed).reset_index(drop=True)
printSuccess('Data shuffled')

splitData = recepies.iloc[:nEntries]
printSuccess('Data splited into shape: ' + str(splitData.shape))

outFileDir = Neo4JImportPath + 'recipes(' + str(nEntries) + ').csv'

printStarting('Saving data to ' + outFileDir + '...')
splitData.to_csv(outFileDir, index=False)
printSuccess('Data saved to ' + outFileDir)


recepieIndices = splitData['RecipeId']

printStarting('Loading data from ' + csvFilepath_reviews + '...')
reviews = pd.read_csv(csvFilepath_reviews)
printSuccess('Data loaded from ' + csvFilepath_reviews)

printStarting('Sanitizing data...')
reviews = reviews.map(sanitize_quotes)
printSuccess('Data sanitized')

print('Data shape: ' + str(reviews.shape))

printStarting('Filtering relevant reviews...')
relevantReviews = reviews[reviews['RecipeId'].isin(recepieIndices)]
printSuccess('Relevant reviews shape: ' + str(relevantReviews.shape))

outFileDir = Neo4JImportPath + 'reviews(' + str(nEntries) + ').csv'

printStarting('Saving data to ' + outFileDir + '...')
relevantReviews.to_csv(outFileDir, index=False)
printSuccess('Data saved to ' + outFileDir)
