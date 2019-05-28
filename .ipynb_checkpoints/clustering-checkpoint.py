
import pandas as pd
import numpy as np
import pyspark
from pyspark import SparkContext
from pyspark.sql import SQLContext
from pyspark.sql.functions import avg
from pyspark.ml.feature import OneHotEncoder, StringIndexer
from pyspark.ml.feature import VectorAssembler
from pyspark.ml.clustering import KMeans


if __name__ == "__main__":

    """
    constants
    """
    
    inputFile = sys.argv[1] if len(sys.argv)>1 else 's3://seedingflow-usecase/cases.json'
    outputFile = sys.argv[2] if len(sys.argv)>2 else 's3://seedingflow-usecase/output.json'
    k = int(sys.argv[3]) if len(sys.argv)>3 else 5

    """
    STEP0
    Read file from S3
    """


    sc = SparkContext.getOrCreate()
    sqlContext = SQLContext(sc)
    df  = sqlContext.read.json(inputFile)

    """
    STEP1
    Handle Missing data
    """

    columns = list(df.schema)
    l = len(columns)
    names = map(lambda x : x.name,columns)
    numerical = filter(lambda x : str(x.dataType)!='StringType',columns)
    nonnumerical = filter(lambda x : str(x.dataType)=='StringType',columns)

    counts = map(lambda name : int(df.describe([name]).first()[1]) ,names)
    n = np.max(counts)

    tuples = [(counts[i],names[i]) for i in range(l)]

    indexesToKeep = [tuples[i][1] for i in range(l) if tuples[i][0]>0.5*n]

    df = df.select(indexesToKeep)

    columns = list(df.schema)
    names = map(lambda x : x.name,columns)
    numerical = filter(lambda x : str(x.dataType)!='StringType',columns)
    nonnumerical = filter(lambda x : str(x.dataType)=='StringType',columns)

    for name in map(lambda x : x.name,numerical):
        removeAllDf = df.na.drop(how = 'any', subset=[name])
        meanValue = removeAllDf.agg(avg(name)).first()[0]
        df = df.na.fill(meanValue,[name])
        
    for name in map(lambda x : x.name,nonnumerical):
        df = df.na.fill('None',[name])

    """
    STEP2
    One hot encoding
    """

    inputColumns = map(lambda x : x.name,numerical)
    for name in map(lambda x : x.name,nonnumerical):
        if(df.select([name]).distinct().count()>1):
            model = StringIndexer(inputCol=name, outputCol=name+" Index").fit(df)
            indexed = model.transform(df)

            encoder = OneHotEncoder(inputCol=name+" Index", outputCol=name+" Vec")
            df = encoder.transform(indexed)

            inputColumns.append(name+" Vec")

    """
    STEP3
    Clustering
    """

    assembler = VectorAssembler().setInputCols(inputColumns).setOutputCol("features")
    kmeans = KMeans().setK(k).setFeaturesCol("features").setPredictionCol("prediction")

    df = assembler.transform(df)
    clusters = kmeans.fit(df).transform(df)

    """
    STEP4
    Write file to S3
    """

    clusters.write.json(outputFile)