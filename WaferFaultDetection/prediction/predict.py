import pandas as pd
from file_operations.read_json import GetJsonData
from object_creator import GetObject

class PredictFinal:
    def __init__(self):

        self.log_path = GetJsonData().read_data_json("LogPath")["prediction"]
        self.get_object = GetObject(self.log_path)

    def predict_model_output(self):
        try:
            self.get_object.log_writer.log(self.get_object.log_file, 'Start of Prediction')

            self.get_object.dataloader.set_object(self.get_object.log_file,self.get_object.log_writer)

            data = self.get_object.dataloader.get_data(self.get_object.prediction_file)

            if data.__len__()==0:
                self.get_object.log_writer.log(self.get_object.log_file,"No data was present to perform prediction existing prediction method")
                return path,"No data was present to perform prediction"


            self.get_object.preprocessor.set_object(self.get_object.log_file,self.get_object.log_writer)

            is_null_present = self.get_object.preprocessor.is_null_present(data)
            if(is_null_present):
                data=self.get_object.preprocessor.impute_missing_values(data)

            _data = self.get_object.preprocessor.remove_columns(data,['Wafer'])

            cols_to_drop=self.get_object.preprocessor.get_columns_with_zero_std_deviation(_data)
            _data = self.get_object.preprocessor.remove_columns(_data,cols_to_drop)
            data = self.get_object.preprocessor.remove_columns(data,cols_to_drop)

            self.get_object.cluster.set_object(self.get_object.log_file,self.get_object.log_writer,self.get_object.file_operation)
            self.get_object.file_operation.set_object(self.get_object.log_file,self.get_object.log_writer)

            kmeans = self.get_object.file_operation.load_model('KMeans')

            clusters=kmeans.predict(_data)

            data['clusters']=clusters

            clusters=data['clusters'].unique()

            for i in clusters:
                cluster_data = data[data['clusters']==i]
                wafer_names = list(cluster_data['Wafer'])
                cluster_data = data.drop(labels=['Wafer'],axis=1)
                cluster_data = cluster_data.drop(labels=['clusters'],axis=1)

                model_name = self.get_object.file_operation.find_correct_model_file(i)
                model = self.get_object.file_operation.load_model(model_name)
                result = list(model.predict(cluster_data))
                result = [1 if x == 1 else -1 for x in result]

                result = pd.DataFrame(list(zip(wafer_names,result)),columns=['Wafer','Prediction'])
                result.to_csv("prediction_output_file/Predictions.csv",header=True,mode='a+') #appends result to prediction file

            # logging the successful Training
            self.get_object.log_writer.log(self.get_object.log_file, 'End of Prediction')
            self.get_object.log_file.close()

        except Exception as e:
            raise Exception()
