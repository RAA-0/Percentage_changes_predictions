import pandas as pd 
import pickle

class Model:
    def __init__(self,target,alpha=0.1,gamma=0.9):
        self.target = target 
        self.alpha = alpha
        self.gamma = gamma 
        self.q_table = {}


    def train(self,training_data):
        self.predicted_changes = {}
        self.training_data=training_data
        for event in self.training_data['event'].unique():
            event_data = self.training_data[self.training_data['event'] == event]
            self.q_table[event] = event_data[f'{self.target}_percentage_change'].mean()
        self.predicted_changes = {tuple(row[['year','event']]): row[f'{self.target}_percentage_change'] for _, row in self.training_data.iterrows()}
            

    def predict(self,year,event):
        if not (self.training_data['event'] == event).any():
            self.predicted_changes[(year,event)]=0
            return 0 
         
        for index,row in self.training_data.iterrows():
            if (year ==int(row['year'])) & (event==row['event']):
                return row[f'{self.target}_percentage_change']
            
        self.predicted_changes[(year,event)]=self.q_table.get(event, 0)
        return self.q_table.get(event, 0)
    
    def update_q_table(self,state,actual_value):
        predicted_value = self.predicted_changes.get(state, 0)
        reward = actual_value - predicted_value
        
        self.q_table[state[1]] = predicted_value + self.alpha * (reward + self.gamma * max(self.q_table.values()))

        self.predicted_changes[state]=actual_value
        new_data = pd.DataFrame({'year': [state[0]], 'event': [state[1]], f'{self.target}_percentage_change': [actual_value]})
        self.training_data = pd.concat([self.training_data, new_data], ignore_index=True)
            
    def save_model(self, filename='model.pkl'):
        with open(filename, 'wb') as file:
            pickle.dump(self, file)
    
    @classmethod
    def load_model(cls, filename='model.pkl'):
        with open(filename, 'rb') as file:
            return pickle.load(file)
        
        
"""df= pd.read_csv('RL_approach\\TrainingDataset2 copy 2.csv')
model = Model()
model.train(df)
predicted_change = model.predict(2023, 'ramadan_season')
print(f'Predicted change: {predicted_change}')
print(model.q_table)
model.update_q_table((2023,'ramadan_season'),-6.1895019006593115)
print(model.q_table)
"""



#2023,ramadan_season,-6.1895019006593115
#2021,christmas_season,19.485893427840466


'''
Another idea ::
improvement? :
make the state of the year and event 
load the training set in the q-table 
if the state is not found in the q-table check the states of the q-table that has the same event and take the average of the values 
and add the state year,event with the prediction to the table 

'''