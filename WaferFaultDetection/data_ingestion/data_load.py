import pandas as pd

class DataGetter:

    def __init__(self):
        
        self.log_file = ""
        self.log_writer = ""

    def set_object(self,log_file,log_writer):
        self.log_file = log_file
        self.log_writer = log_writer

    def get_data(self,file_name):
       
        try:
            self.data = pd.read_csv(file_name)
            self.log_writer.log(self.log_file,'Data Load Successful.Exited the get_data method of the Data_Getter class')
            self.log_writer.log(self.log_file,"size of the training data :" + str(self.data.shape))

            return self.data

        except Exception as e:
            msg = "Error occured in class:'get_data':" + str(e)
            self.log_writer.log(self.log_file, msg)
