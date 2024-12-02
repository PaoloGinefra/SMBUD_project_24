import pandas as pd
import numpy as np
import os


class DatasetSplitter:
    '''
    This class is responsible to ingest a CSV file and return a reduced version of it via random sampling.

    '''

    def __init__(self, csvFilepath: str, outputDir: str, seed: int = 0):
        self.csvFilepath = csvFilepath
        self.outputDir = outputDir
        self.fileName = os.path.basename(csvFilepath)[:-4]
        self.seed = seed
        self.__loadData()
        self.__sanitize_data([DatasetSplitter.__sanitize_quotes])
        self.__shuffleData()

    def __loadData(self):
        '''
        Load the data from the CSV file.
        '''
        print('Loading data from ' + self.csvFilepath + '...')
        self.data = pd.read_csv(self.csvFilepath)
        print('Data loaded from ' + self.csvFilepath)
        print('Data shape: ' + str(self.data.shape))

    def __shuffleData(self):
        '''
        Shuffle the data.
        '''
        self.data = self.data.sample(
            frac=1, random_state=self.seed).reset_index(drop=True)
        print('Data shuffled')

    def __sanitize_quotes(value):
        if isinstance(value, str):
            return value.replace('""', '"').replace('\\"', '"')
        return value

    def __sanitize_data(self, sanitazers: list):
        print('Sanitizing data...')
        for sanitazer in sanitazers:
            self.data = self.data.map(sanitazer)
        print('Data sanitized')

    def __saveData(self, data: pd.DataFrame):
        '''
        Save the data to the output directory.

        :param data: The data to be saved.
        '''
        nEntries = len(data)
        outFileDir = self.outputDir + self.fileName + f'[{nEntries}].csv'
        data.to_csv(outFileDir, index=False)

        print('Data saved to ' + outFileDir)

    def splitAndSavePercentage(self, sizePercentage: float):
        '''
        Split the data and save it to the output directory.

        :param sizePercentage: The percentage of the data to be saved.
        '''
        nEntries = int(len(self.data) * sizePercentage)
        self.splitAndSaveEntries(nEntries)

    def splitAndSaveEntries(self, nEntries: int):
        '''
        Split the data and save it to the output directory.

        :param sizePercentage: The percentage of the data to be saved.
        '''
        splitData = self.data.iloc[:nEntries]
        print('Data splited into shape: ' + str(splitData.shape))
        self.__saveData(splitData)


if __name__ == '__main__':
    Neo4JImportPath = 'C:\\Users\\Paolo\\.Neo4jDesktop\\relate-data\\dbmss\\dbms-d410dbd9-acc1-4cc0-a8ac-271554bed9c8\\import\\'
    splitter = DatasetSplitter(
        csvFilepath='./Dataset/recipes.csv',
        outputDir=Neo4JImportPath
    )
    splitter.splitAndSaveEntries(1000)
