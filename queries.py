import psycopg2

from CurriculumAlgorithmWebApp import settings
from curriculum_algorithm.models import Course


def get_course_difficulty(course):
    conn = psycopg2.connect("dbname=curriculum_algorithm user=postgres password=12345678")

    cursor = conn.cursor()

    cursor.execute('SELECT  "CURSO",'
                   ' Round(((sum(coalesce("W", 0)) + sum(coalesce("F", 0)))*1.'
                   ' + (sum(coalesce("C", 0)) + sum(coalesce("D", 0)))*2. '
                   ' + (sum(coalesce("B", 0)) + sum(coalesce("A", 0)))*3.)'
                   ' /(sum(coalesce("Total", 0)) '
                   ' - sum(coalesce("IF", 0)) '
                   ' - sum(coalesce("ID", 0)) '
                   ' - sum(coalesce("IC", 0))'
                   ' - sum(coalesce("IB", 0))'
                   ' - sum(coalesce("IA", 0))'
                   ' - sum(coalesce("ASTERISCO", 0))), 0)  as avg_grade, sum("Total") as student_total '
                   ' FROM curriculum_algorithm.public.notas_2018_2019 '
                   ' where "CURSO" = \'%s %s\' ' 
                   ' group by  "CURSO" ' % (course.department, course.code))

    column_names = [desc[0] for desc in cursor.description]
    for row in cursor.fetchall():
        row = dict(zip(column_names, row))
        return int(row['avg_grade']) if row['avg_grade'] else 1
    return 1


def migrate_courses():
    conn = psycopg2.connect("dbname=curriculum_algorithm user=postgres password=12345678")
    cursor = conn.cursor()
    cursor.execute(" SELECT DISTINCT CURSO"
                   " FROM curriculum_algorithm.public.notas_2018_2019 ")
    column_names = [desc[0] for desc in cursor.description]
    for row in cursor.fetchall():
        row = dict(zip(column_names, row))
        Course(code=int(row['CURSO'][4:]), season='0', department=row['CURSO'][0:4], credit_hours=3).save()