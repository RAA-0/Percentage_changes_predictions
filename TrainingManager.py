from Training.Preprocessingg import EventFeatureExtractor
from Training.Training import DataTrainer
from path_config.paths_config import PathConfig
import pandas as pd

def main():
    data = pd.read_csv(conf.path('training_data'))
    process = EventFeatureExtractor()
    transformed_data = process.extract(data)
    for target in ['arrival','departure']:
        data = transformed_data.copy()
        trainer = DataTrainer(data,target)
        model=trainer.prophet_model()
        trainer.train(model)

if __name__=='__main__':
    conf = PathConfig()
    main()

  