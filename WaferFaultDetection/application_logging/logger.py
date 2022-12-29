import os
from datetime import datetime

class AppLogger:

    def __init__(self):
        pass

    def log(self, file_object, log_message):
        try:
            
            self.now = datetime.now()
            self.date = self.now.date()
            self.current_time = self.now.strftime("%H:%M:%S.%f")

            file_object.write(str(self.date) + " " + str(self.current_time) + "--------->" + log_message + "\n")
        
        except Exception as e:
             return str(e)

    def create_log_Files(self,path):
        try:
            log_name = datetime.now().strftime(path + '_%d_%m_%Y_%H_%M_%S.%f.log')

            if os.path.exists(path):
                pass
            else:
                os.makedirs(path)

            with open(os.path.join(path, log_name), 'w') as fp:
                pass

            fileObj = open(path + "/" + log_name , "w")

            return fileObj

        except Exception as e:
            raise Exception()
