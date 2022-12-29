import pandas as pd
import numpy as np
from sklearn.impute import KNNImputer

class Preprocessor:

    def __init__(self):
        self.log_file = ""
        self.log_writer = ""

    def set_object(self,log_file,log_writer):
        self.log_file = log_file
        self.log_writer = log_writer

    def remove_columns(self,data,columns):
        self.data=data
        self.columns=columns

        try:
            self.useful_data=self.data.drop(labels=self.columns, axis=1)
            self.log_writer.log(self.log_file,'Column removal Successful.Exited the remove_columns method of the Preprocessor class')
            return self.useful_data

        except Exception as e:
            self.log_writer.log(self.log_file, 'Exception occured in remove_columns method of the Preprocessor class. Exception message:  '+str(e))
            self.log_writer.log(self.log_file, 'Column removal Unsuccessful. Exited the remove_columns method of the Preprocessor class')
            raise Exception()

    def separate_label_feature(self,data,label_column_name):
        self.log_writer.log(self.log_file, 'Entered the separate_label_feature method of the Preprocessor class')

        try:
            # drop the columns specified and separate the feature columns
            self.X=data.drop(labels=label_column_name,axis=1)

            # Filter the Label columns
            self.Y=data[label_column_name]

            self.log_writer.log(self.log_file, 'Label Separation Successful. Exited the separate_label_feature method of the Preprocessor class')
            return self.X,self.Y

        except Exception as e:
            self.log_writer.log(self.log_file,'Exception occured in separate_label_feature method of the Preprocessor class. Exception message:  ' + str(e))
            self.log_writer.log(self.log_file, 'Label Separation Unsuccessful. Exited the separate_label_feature method of the Preprocessor class')
            raise Exception()

    def is_null_present(self,data):
        
        self.log_writer.log(self.log_file, 'Entered the is_null_present method of the Preprocessor class')
        self.null_present = False

        try:
            # check for the count of null values per column
            self.null_counts=data.isna().sum()
            for i in self.null_counts:
                if i>0:
                    self.null_present=True
                    break
            
            if(self.null_present): # write the logs to see which columns have null values
                dataframe_with_null = pd.DataFrame()
                dataframe_with_null['columns'] = data.columns
                dataframe_with_null['missing values count'] = np.asarray(data.isna().sum())
                
                # storing the null column information to file
                dataframe_with_null.to_csv('preprocessing_data/null_values.csv')

            self.log_writer.log(self.log_file,'Finding missing values is a success.Data written to the null values file. Exited the is_null_present method of the Preprocessor class')
            return self.null_present

        except Exception as e:
            self.log_writer.log(self.log_file,'Exception occured in is_null_present method of the Preprocessor class. Exception message:  ' + str(e))
            self.log_writer.log(self.log_file,'Finding missing values failed. Exited the is_null_present method of the Preprocessor class')
            raise Exception()
           
    def impute_missing_values(self,data):
        
        self.log_writer.log(self.log_file, 'Entered the impute_missing_values method of the Preprocessor class')
        self.data= data

        try:
            imputer=KNNImputer(n_neighbors=3, weights='uniform',missing_values=np.nan)
            self.new_array=imputer.fit_transform(self.data) # impute the missing values

            # convert the nd-array returned in the step above to a Dataframe
            self.new_data=pd.DataFrame(data=self.new_array, columns=self.data.columns)
            self.log_writer.log(self.log_file, 'Imputing missing values Successful. Exited the impute_missing_values method of the Preprocessor class')
            return self.new_data

        except Exception as e:
            self.log_writer.log(self.log_file,'Exception occured in impute_missing_values method of the Preprocessor class. Exception message:  ' + str(e))
            self.log_writer.log(self.log_file,'Imputing missing values failed. Exited the impute_missing_values method of the Preprocessor class')

            raise Exception()

    def get_columns_with_zero_std_deviation(self,data):
        self.log_writer.log(self.log_file, 'Entered the get_columns_with_zero_std_deviation method of the Preprocessor class')

        self.columns=data.columns
        self.data_n = data.describe()
        self.col_to_drop=[]

        try:
            for x in self.columns:
                if (self.data_n[x]['std'] == 0): # check if standard deviation is zero
                    self.col_to_drop.append(x)   # prepare the list of columns with standard deviation zero
            
            self.log_writer.log(self.log_file, 'Column search for Standard Deviation of Zero Successful. Exited the get_columns_with_zero_std_deviation method of the Preprocessor class')
            return self.col_to_drop

        except Exception as e:
            self.log_writer.log(self.log_file,'Exception occured in get_columns_with_zero_std_deviation method of the Preprocessor class. Exception message:  ' + str(e))
            self.log_writer.log(self.log_file, 'Column search for Standard Deviation of Zero Failed. Exited the get_columns_with_zero_std_deviation method of the Preprocessor class')

            raise Exception()