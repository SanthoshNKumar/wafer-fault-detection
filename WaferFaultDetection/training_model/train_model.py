from sklearn.model_selection import train_test_split
from file_operations.read_json import GetJsonData
from object_creator import GetObject

class TrainModel:
    def __init__(self):

        self.log_path = GetJsonData().read_data_json("LogPath")["training"]
        self.get_object = GetObject(self.log_path)

    def training_model(self):

        try:
            self.get_object.log_writer.log(self.get_object.log_file, 'Start of Training')

            self.get_object.dataloader.set_object(self.get_object.log_file,self.get_object.log_writer)

            data = self.get_object.dataloader.get_data(self.get_object.training_file)

            if data.__len__()==0:
                self.get_object.log_writer.log(self.get_object.log_file,"No record found to train model")
                return 0

            """doing the data preprocessing"""

            self.get_object.preprocessor.set_object(self.get_object.log_file,self.get_object.log_writer)
            data = self.get_object.preprocessor.remove_columns(data,['Wafer'])

            # create separate features and labels to be continue from here evening
            X,Y = self.get_object.preprocessor.separate_label_feature(data,label_column_name='Output')

            # check if missing values are present in the dataset
            is_null_present=self.get_object.preprocessor.is_null_present(X)

            if(is_null_present):
                X = self.get_object.preprocessor.impute_missing_values(X) # missing value imputation

            # check further which columns do not contribute to predictions
            # if the standard deviation for a column is zero, it means that the column has constant values
            # and they are giving the same output both for good and bad sensors
            # prepare the list of such columns to drop

            cols_to_drop=self.get_object.preprocessor.get_columns_with_zero_std_deviation(X)

            # drop the columns obtained above
            X = self.get_object.preprocessor.remove_columns(X,cols_to_drop)

            #kmeans = KMeansClustering() # object initialization.
            self.get_object.cluster.set_object(self.get_object.log_file,self.get_object.log_writer,self.get_object.file_operation)
            self.get_object.file_operation.set_object(self.get_object.log_file,self.get_object.log_writer)

            number_of_clusters=self.get_object.cluster.elbow_plot(X)  #  using the elbow plot to find the number of optimum clusters

             # Divide the data into clusters
            X = self.get_object.cluster.create_clusters(X,number_of_clusters)

            #create a new column in the dataset consisting of the corresponding cluster assignments.
            X['Labels'] = Y

            # getting the unique clusters from our dataset
            list_of_clusters=X['Cluster'].unique()

            self.get_object.model_finder.set_object(self.get_object.log_file,self.get_object.log_writer)

            for i in list_of_clusters:
                cluster_data=X[X['Cluster']==i] # filter the data for one cluster

                # Prepare the feature and Label columns
                cluster_features=cluster_data.drop(['Labels','Cluster'],axis=1)
                cluster_label= cluster_data['Labels']

                # splitting the data into training and test set for each cluster one by one
                x_train, x_test, y_train, y_test = train_test_split(cluster_features, cluster_label, test_size=1 / 3, random_state=355)

                #getting the best model for each of the clusters
                best_model_name,best_model=self.get_object.model_finder.get_best_model(x_train,y_train,x_test,y_test)

                #saving the best model to the directory.
                save_model=self.get_object.file_operation.save_model(best_model,best_model_name+str(i))

            # logging the successful Training
            self.get_object.log_writer.log(self.get_object.log_file, 'Successful End of Training')
            self.get_object.log_file.close()

        except Exception as e:
            self.get_object.log_writer.log(self.get_object.log_file, 'Unsuccessful End of Training')
            self.get_object.log_file.close()
            raise Exception