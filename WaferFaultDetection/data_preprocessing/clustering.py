import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
from kneed import KneeLocator

class KMeansClustering:

    def __init__(self):

        self.log_file = ""
        self.log_writer = ""

        self.file_op = ""

    def set_object(self,log_file,log_writer,file_operation):
        self.log_file = log_file
        self.log_writer = log_writer
        self.file_op = file_operation

    def elbow_plot(self,data):
        self.log_writer.log(self.log_file, 'Entered the elbow_plot method of the KMeansClustering class')
        wcss=[] # initializing an empty list

        try:
            for i in range (1,11):
                kmeans=KMeans(n_clusters=i,init='k-means++',random_state=42) # initializing the KMeans object
                kmeans.fit(data) # fitting the data to the KMeans Algorithm
                wcss.append(kmeans.inertia_)

            plt.plot(range(1,11),wcss) # creating the graph between WCSS and the number of clusters
            plt.title('The Elbow Method')
            plt.xlabel('Number of clusters')
            plt.ylabel('WCSS')
            #plt.show()
            plt.savefig('preprocessing_data/K-Means_Elbow.PNG') # saving the elbow plot locally

            # finding the value of the optimum cluster programmatically
            self.kn = KneeLocator(range(1, 11), wcss, curve='convex', direction='decreasing')

            self.log_writer.log(self.log_file, 'The optimum number of clusters is: '+str(self.kn.knee)+' . Exited the elbow_plot method of the KMeansClustering class')

            return self.kn.knee

        except Exception as e:
            self.log_writer.log(self.log_file,'Exception occured in elbow_plot method of the KMeansClustering class. Exception message:  ' + str(e))
            self.log_writer.log(self.log_file,'Finding the number of clusters failed. Exited the elbow_plot method of the KMeansClustering class')
            raise Exception()

    def create_clusters(self,data,number_of_clusters):

        self.log_writer.log(self.log_file, 'Entered the create_clusters method of the KMeansClustering class')
        self.data=data

        try:

            self.kmeans = KMeans(n_clusters=number_of_clusters, init='k-means++', random_state=42)

            #self.data = self.data[~self.data.isin([np.nan, np.inf, -np.inf]).any(1)]
            self.y_kmeans=self.kmeans.fit_predict(data) #  divide data into clusters

            self.save_model = self.file_op.save_model(self.kmeans, 'KMeans') # saving the KMeans model to directory

            self.data['Cluster']=self.y_kmeans  # create a new column in dataset for storing the cluster information
            self.log_writer.log(self.log_file, 'succesfully created '+str(self.kn.knee)+ 'clusters. Exited the create_clusters method of the KMeansClustering class')

            return self.data

        except Exception as e:
            self.log_writer.log(self.log_file,'Exception occured in create_clusters method of the KMeansClustering class. Exception message:  ' + str(e))
            self.log_writer.log(self.log_file,'Fitting the data to clusters failed. Exited the create_clusters method of the KMeansClustering class')

            raise Exception()