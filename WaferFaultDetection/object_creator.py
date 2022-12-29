from data_ingestion.data_load import DataGetter
from data_preprocessing.preprocessing import Preprocessor
from data_preprocessing.clustering import KMeansClustering
from file_operations.file_methods import FileOperation
from best_model_finder.tuner import ModelFinder

#from file_operations.read_json import GetJsonData
from application_logging.logger import AppLogger


class GetObject:
    def __init__(self,log_path):
        #self.json_obj = GetJsonData()
        #self.ConfigFile = self.json_obj.configfile
        self.training_file = "training_file_db/InputFile.csv"
        self.prediction_file = "prediction_file_db/InputFile.csv"

        self.dataloader = DataGetter()
        self.preprocessor = Preprocessor()
        self.model_finder = ModelFinder() 
        self.file_operation = FileOperation()
        self.cluster = KMeansClustering()

        self.log_writer = AppLogger()
        self.log_file = self.log_writer.create_log_Files(log_path)
