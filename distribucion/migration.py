from pyspark.sql import SparkSession
import pandas

spark = SparkSession.builder.appName("Test").getOrCreate()

sheets = ['SEM-1', 'SEM-2']
file_names = ['notas_2019-2020.xlsx', 'notas_2017-2018-2.xlsx']

data_frames = []

count = 0
for file_name in file_names:
    for sheet in sheets:
        print(file_name)
        pandas_frame = pandas.read_excel(file_name, sheet_name=sheet, inferSchema='true')
        data_frame = spark.createDataFrame(pandas_frame)
        data_frame = data_frame.replace(float('nan'), 0)
        grades = data_frame.select("CURSO", "A", "B", "C", "D", "F", "IA", "IB", "IC", "ID", "IF", "TOTAL").groupBy('CURSO').sum()
        grades = grades.withColumn(f"avg_{count}", (grades["sum(A)"]*4 + grades["sum(B)"]*3 + grades["sum(C)"]*2 + grades["sum(D)"]*1)/(grades["sum(TOTAL)"] - grades["sum(IA)"] - grades["sum(IB)"] - grades["sum(IC)"] - grades["sum(ID)"] - grades["sum(IF)"]))

        grades = grades.withColumnRenamed('sum(A)', f'A_{count}').withColumnRenamed('sum(B)', f'B_{count}').\
            withColumnRenamed('sum(C)', f'C_{count}').withColumnRenamed('sum(D)', f'D_{count}').\
            withColumnRenamed('sum(F)', f'F_{count}').withColumnRenamed('sum(TOTAL)', f'TOTAL_{count}').\
            withColumnRenamed('sum(W)', f'W_{count}')

        data_frames.append(grades)
        count += 1
joined = data_frames[0]
count = 0
for index in range(1, len(data_frames)):
    joined = joined.join(data_frames[index], on=["CURSO"], how='left')
    count += 1

joined = joined.na.fill(0)
joined = joined.withColumn("avg_avg", sum(joined[col] for col in joined.columns if "avg" in col)/len(data_frames))

joined.toPandas().to_csv('avg_avg.csv')
