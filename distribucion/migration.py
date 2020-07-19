from pyspark.sql import SparkSession
import pandas
from pyspark.sql.dataframe import DataFrame

spark = SparkSession.builder.appName("Test").getOrCreate()

sheets = ['VER-1', 'SEM-1', 'SEM-2']
file_names = ['notas_2019-2020.xlsx']

data_frames = []

for file_name in file_names:
    for sheet in sheets:
        pandas_frame = pandas.read_excel(file_name, sheet_name=sheet, inferSchema='true')
        data_frame = spark.createDataFrame(pandas_frame)
        data_frame = data_frame.replace(float('nan'), 0)
        grades = data_frame.select('CURSO', 'A', 'B', 'C', 'D', 'F', 'W', 'TOTAL').groupBy('CURSO').sum()
        grades.withColumn("avg", (grades["sum(A)"]*4 + grades["sum(B)"]*3 + grades["sum(C)"]*2 + grades["sum(D)"]*1)/grades["sum(TOTAL)"])
        data_frames.append(grades)

joined = data_frames[0]
count = 0
for index in range(1, len(data_frames)):
    joined = joined.join(data_frames[index], on=["CURSO"], how='inner')
    count += 1

joined.show()

