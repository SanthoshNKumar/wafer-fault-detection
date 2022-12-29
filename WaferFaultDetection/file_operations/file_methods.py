import pickle
import os
import shutil
import re

class FileOperation:
    def __init__(self):
        self.log_file = ""
        self.log_writer = ""

        self.model_directory='model'

    def set_object(self,log_file,log_writer):
        self.log_file = log_file
        self.log_writer = log_writer

    def save_model(self,model,filename):

        self.log_writer.log(self.log_file, 'Entered the save_model method of the File_Operation class')

        directory_name=self.model_directory + '-' + filename

        try:
            path = self.model_directory + '/' + directory_name

            if os.path.isdir(path): #remove previously existing models for each clusters

                shutil.rmtree(self.model_directory)

                os.makedirs(path)
            else:
                os.makedirs(path)

            with open(path +'/' + filename+'.sav','wb') as f:
                pickle.dump(model, f) # save the model to file

            self.log_writer.log(self.log_file,'Model File '+filename+' saved. Exited the save_model method of the Model_Finder class')

            return 'success'

        except Exception as e:
            self.log_writer.log(self.log_file,'Exception occured in save_model method of the Model_Finder class. Exception message:  ' + str(e))
            self.log_writer.log(self.log_file,'Model File '+filename+' could not be saved. Exited the save_model method of the Model_Finder class')

            raise Exception()

    def load_model(self,filename):
        self.log_writer.log(self.log_file, 'Entered the load_model method of the File_Operation class')

        try:

            directory = self.model_directory + '-' + filename
            filename= filename +'.sav'

            self.log_writer.log(self.log_file, 'Entered the load_model method of the File_Operation class')

            self.log_writer.log(self.log_file, 'Model File ' + filename + ' loaded. Exited the load_model method of the Model_Finder class')
                
            objectRep = open(self.model_directory + '/' + directory + '/' + filename,'rb')
            self.log_writer.log(self.log_file,'Model File ' + filename + ' loaded. Exited the load_model method of the Model_Finder class')
            return pickle.load(objectRep)

        except Exception as e:
            self.log_writer.log(self.log_file,'Exception occured in load_model method of the Model_Finder class. Exception message:  ' + str(e))
            self.log_writer.log(self.log_file,'Model File ' + filename + ' could not be saved. Exited the load_model method of the Model_Finder class')

            raise Exception()

    def find_correct_model_file(self,cluster_number):
        try:

            self.log_writer.log(self.log_file, 'Entered the find_correct_model_file method of the File_Operation class')

            list_of_model_files = []
            list_files = os.listdir(self.model_directory)
            list_of_files=[]

            for dir in list_files:
                if re.search("^model[-][a-zA-z]{2,17}[0-9]",dir):
                    list_of_files.append(dir)

            for file in list_of_files:
                try:
                    models = os.listdir('model' + '/' + file)
                    for model_name_ in models:
                        if(model_name_.index(str(cluster_number))!=-1):
                            model_name=model_name_
                except:
                    continue

            model_name = model_name.split('.')[0]
            return model_name

        except Exception as e:
            self.log_writer.log(self.log_file,'Exception occured in find_correct_model_file method of the Model_Finder class. Exception message:  ' + str(e))
            self.log_writer.log(self.log_file,'Exited the find_correct_model_file method of the Model_Finder class with Failure')
            raise Exception()


