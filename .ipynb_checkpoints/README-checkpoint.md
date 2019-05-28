# Pyspark code to clusterize a lambda dataset



## [clustering.py]


Inputs : a json file path (works with a path towards an s3) towards a dataset we want to clusterize, a json file path which corresponds to where we want to store the ouput of the clustering (works also on a s3 path), and k the number of clusters we want to create

Here are the 3 main steps of this code / every thing is computed in a distributed computation way :

### Step1

- Remove every columns in which more than half of the values are missing and then replace
- For every numerical columns replace missing values with mean
- For every non-numerical columns replace missing values with 'None'

### Step2

- One hot encoding of every non-numerical columns with pyspark.ml OneHotEncoder

### Step3

- Create the actual vector to be sent to the clustering algorithm with pyspar.ml VectorAssembler
- Perform K-means



## [terraform-as-emr-cluster]

The terraform code can launch the the clustering code on every dataset stored as a json in an s3 by deploying an EMR on which it wil run.

