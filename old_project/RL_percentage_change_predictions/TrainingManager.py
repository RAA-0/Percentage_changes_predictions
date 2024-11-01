import pandas as pd

from Training.BuildDataset import DatasetBuilder
from Training.new_model import Model

def main():
    df = DatasetBuilder("data\\Training\\TrainingDataset.csv").build_dataset()
    #df = pd.read_csv("data\\Training\\TrainingDataset.csv")
    arrival_model = Model('arrival')
    arrival_model.train(df)
    arrival_model.save_model('arrival_model.pkl')

    departure_model = Model('departure')
    departure_model.train(df)
    departure_model.save_model('departure_model.pkl')

if __name__=='__main__':
    main()