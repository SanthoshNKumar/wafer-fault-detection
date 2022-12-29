from object_creator import GetObject
from file_operations.read_json import GetJsonData

if __name__ == '__main__':

    try: 
        from training_model.train_model import TrainModel
        TrainModel().training_model()

        from prediction.predict import PredictFinal
        PredictFinal().predict_model_output();
        
    except Exception as e :
        print(str(e))
