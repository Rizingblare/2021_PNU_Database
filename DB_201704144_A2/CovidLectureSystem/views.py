from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.db import connection
import json

def display(request):
    return render(request, 'CovidLectureSystem/201704144_INDEX.html')

# Each addFunction has a QUERY 5 Time Check mark.
def addStu(request):
    if request.method == "POST":
        addStu = json.loads(request.body)
        outputQuery1 = []
        outputQuery2 = []
        outputQuery3 = []
        outputQuery4 = []
        outputQuery5 = []
    with connection.cursor() as cursor:
        sql_query = "INSERT INTO students VALUES ('{0}', '{1}', '{2}', '{3}');"\
            .format(addStu['stu_ID'], addStu['stu_name'], float(addStu['stu_score']), addStu['stu_county'])
        cursor.execute(sql_query)
        sql_query = "SELECT county,AVG(score) FROM students GROUP BY county;"
        cursor.execute(sql_query)
        fetchQuery1 = cursor.fetchall()
        sql_query = "SELECT city, AVG(score) FROM students Stu INNER JOIN counties Cnt ON Stu.county = Cnt.countyName GROUP BY city;"
        cursor.execute(sql_query)
        fetchQuery2 = cursor.fetchall()
        sql_query = """
                    CREATE VIEW vTemp AS
                    SELECT Stu.county AS CntName, Stu.name AS StuName, Stu.score AS StuScore, Prof.name AS ProfName, Prof.age AS ProfAge
                    FROM Students Stu INNER JOIN Professors Prof ON Stu.county = Prof.county;
                    """
        cursor.execute(sql_query)
        sql_query = """
                    SELECT ProfName, StuName
                    FROM vTemp, (SELECT CntName, MAX(StuScore) AS CntScore, MAX(ProfAge) AS CntAge FROM vTemp GROUP BY CntName) CntMax
                    WHERE vTemp.CntName = CntMax.CntName AND StuScore = CntScore AND ProfAge = CntAge;
                    """
        cursor.execute(sql_query)
        fetchQuery3 = cursor.fetchall()
        sql_query = """
                    DROP VIEW vTemp;
                    """
        cursor.execute(sql_query)

        sql_query = """
                    CREATE VIEW vTemp AS
                    SELECT StuCity.city AS CityName, StuCity.name AS StuName, StuCity.score AS StuScore, ProfCity.name AS ProfName, ProfCity.age AS ProfAge
                    FROM (SELECT * FROM Students Stu INNER JOIN Counties Cnt ON Stu.county = Cnt.countyName) StuCity INNER JOIN (SELECT * FROM Professors Prof INNER JOIN Counties Cnt ON Prof.county = Cnt.countyName) ProfCity
                    ON StuCity.city = ProfCity.city;
                    """
        cursor.execute(sql_query)
        sql_query = """
                    SELECT ProfName, StuName
                    FROM vTemp, (SELECT CityName, MAX(StuScore) AS CityScore, MAX(ProfAge) AS CityAge FROM vTemp GROUP BY CityName) CityMax
                    WHERE vTemp.CityName = CityMax.CityName AND StuScore = CityScore AND ProfAge = CityAge;
                    """
        cursor.execute(sql_query)
        fetchQuery4 = cursor.fetchall()
        sql_query = """
                    DROP VIEW vTemp;
                    """
        cursor.execute(sql_query)

# - - - - - Query5 TIME START (201704144) - - - - -
        sql_query = """
                    CREATE VIEW vTemp AS
                    SELECT TotalList.city AS DangerCity
                    FROM
                    (SELECT city, COUNT(*) AS CityAll FROM (SELECT studentID,Cnt.city FROM Students Stu INNER JOIN Counties Cnt ON Stu.county = Cnt.countyName UNION SELECT facultyID,Cnt.city FROM Professors Prof INNER JOIN Counties Cnt ON Prof.county = Cnt.countyName UNION SELECT patientID, COVID.city FROM COVID INNER JOIN Counties Cnt ON COVID.city = Cnt.city) A GROUP BY city) TotalList,
                    (SELECT Cnt.city, COUNT(DISTINCT patientID) AS CityPatients FROM COVID INNER JOIN Counties Cnt ON COVID.city = Cnt.city GROUP BY Cnt.city) PatientsList
                    WHERE TotalList.city = PatientsList.city
                    ORDER BY CityPatients/CityAll DESC LIMIT 3;
                    """
        cursor.execute(sql_query)
        sql_query = """
                    SELECT name, city
                    FROM Students Stu INNER JOIN Counties Cnt ON Stu.county = Cnt.countyName
                    WHERE EXISTS (SELECT * FROM vTemp WHERE Cnt.city = DangerCity)
                    ORDER BY city;
                    """
        cursor.execute(sql_query)
# - - - - - Query5 TIME END (201704144) - - - - -
        fetchQuery5 = cursor.fetchall()
        sql_query = """
                    DROP VIEW vTemp;
                    """
        cursor.execute(sql_query)

        connection.commit()
        connection.close()

    for tmp in fetchQuery1:
        eachRow = {'countyName': tmp[0], 'averageScore': tmp[1]}
        outputQuery1.append(eachRow)

    for tmp in fetchQuery2:
        eachRow = {'cityName': tmp[0], 'averageScore': tmp[1]}
        outputQuery2.append(eachRow)

    for tmp in fetchQuery3:
        eachRow = {'professorName': tmp[0], 'studentName': tmp[1]}
        outputQuery3.append(eachRow)

    for tmp in fetchQuery4:
        eachRow = {'professorName': tmp[0], 'studentName': tmp[1]}
        outputQuery4.append(eachRow)

    for tmp in fetchQuery5:
        eachRow = {'studentName': tmp[0], 'cityName': tmp[1]}
        outputQuery5.append(eachRow)

    result = {
        "Query1": outputQuery1,
        "Query2": outputQuery2,
        "Query3": outputQuery3,
        "Query4": outputQuery4,
        "Query5": outputQuery5
    }
    return JsonResponse(result)

def addProf(request):
    if request.method == "POST":
        addProf = json.loads(request.body)
        outputQuery3 = []
        outputQuery4 = []
        outputQuery5 = []
    with connection.cursor() as cursor:
        sql_query = "INSERT INTO professors VALUES ('{0}', '{1}', '{2}', '{3}');"\
            .format(addProf['prof_ID'], addProf['prof_name'], int(addProf['prof_age']), addProf['prof_county'])
        cursor.execute(sql_query)
        sql_query = """
                    CREATE VIEW vTemp AS
                    SELECT Stu.county AS CntName, Stu.name AS StuName, Stu.score AS StuScore, Prof.name AS ProfName, Prof.age AS ProfAge
                    FROM Students Stu INNER JOIN Professors Prof ON Stu.county = Prof.county;
                    """
        cursor.execute(sql_query)
        sql_query = """
                    SELECT ProfName, StuName
                    FROM vTemp, (SELECT CntName, MAX(StuScore) AS CntScore, MAX(ProfAge) AS CntAge FROM vTemp GROUP BY CntName) CntMax
                    WHERE vTemp.CntName = CntMax.CntName AND StuScore = CntScore AND ProfAge = CntAge;
                    """
        cursor.execute(sql_query)
        fetchQuery3 = cursor.fetchall()
        sql_query = """
                    DROP VIEW vTemp;
                    """
        cursor.execute(sql_query)
        sql_query = """
                    CREATE VIEW vTemp AS
                    SELECT StuCity.city AS CityName, StuCity.name AS StuName, StuCity.score AS StuScore, ProfCity.name AS ProfName, ProfCity.age AS ProfAge
                    FROM (SELECT * FROM Students Stu INNER JOIN Counties Cnt ON Stu.county = Cnt.countyName) StuCity INNER JOIN (SELECT * FROM Professors Prof INNER JOIN Counties Cnt ON Prof.county = Cnt.countyName) ProfCity
                    ON StuCity.city = ProfCity.city;
                    """
        cursor.execute(sql_query)
        sql_query = """
                    SELECT ProfName, StuName
                    FROM vTemp, (SELECT CityName, MAX(StuScore) AS CityScore, MAX(ProfAge) AS CityAge FROM vTemp GROUP BY CityName) CityMax
                    WHERE vTemp.CityName = CityMax.CityName AND StuScore = CityScore AND ProfAge = CityAge;
                    """
        cursor.execute(sql_query)
        fetchQuery4 = cursor.fetchall()
        sql_query = """
                    DROP VIEW vTemp;
                    """
        cursor.execute(sql_query)

# - - - - - Query5 TIME START (201704144) - - - - -
        sql_query = """
                    CREATE VIEW vTemp AS
                    SELECT TotalList.city AS DangerCity
                    FROM
                    (SELECT city, COUNT(*) AS CityAll FROM (SELECT studentID,Cnt.city FROM Students Stu INNER JOIN Counties Cnt ON Stu.county = Cnt.countyName UNION SELECT facultyID,Cnt.city FROM Professors Prof INNER JOIN Counties Cnt ON Prof.county = Cnt.countyName UNION SELECT patientID, COVID.city FROM COVID INNER JOIN Counties Cnt ON COVID.city = Cnt.city) A GROUP BY city) TotalList,
                    (SELECT Cnt.city, COUNT(DISTINCT patientID) AS CityPatients FROM COVID INNER JOIN Counties Cnt ON COVID.city = Cnt.city GROUP BY Cnt.city) PatientsList
                    WHERE TotalList.city = PatientsList.city
                    ORDER BY CityPatients/CityAll DESC LIMIT 3;
                    """
        cursor.execute(sql_query)
        sql_query = """
                    SELECT name, city
                    FROM Students Stu INNER JOIN Counties Cnt ON Stu.county = Cnt.countyName
                    WHERE EXISTS (SELECT * FROM vTemp WHERE Cnt.city = DangerCity)
                    ORDER BY city;
                    """
        cursor.execute(sql_query)
# - - - - - Query5 TIME END (201704144) - - - - -
        fetchQuery5 = cursor.fetchall()
        sql_query = """
                    DROP VIEW vTemp;
                    """
        cursor.execute(sql_query)

        connection.commit()
        connection.close()
    for tmp in fetchQuery3:
        eachRow = {'professorName': tmp[0], 'studentName': tmp[1]}
        outputQuery3.append(eachRow)

    for tmp in fetchQuery4:
        eachRow = {'professorName': tmp[0], 'studentName': tmp[1]}
        outputQuery4.append(eachRow)

    for tmp in fetchQuery5:
        eachRow = {'studentName': tmp[0], 'cityName': tmp[1]}
        outputQuery5.append(eachRow)


    result = {
        "Query3": outputQuery3,
        "Query4": outputQuery4,
        "Query5": outputQuery5
    }
    return JsonResponse(result)

def addCnt(request):
    if request.method == "POST":
        addCnt = json.loads(request.body)
        outputQuery2 = []
        outputQuery4 = []
        outputQuery5 = []
    with connection.cursor() as cursor:
        sql_query = "INSERT INTO counties VALUES ('{0}', '{1}', '{2}');"\
            .format(addCnt['cnt_name'], int(addCnt['cnt_population']), addCnt['cnt_city'])
        cursor.execute(sql_query)

        sql_query = "SELECT city, AVG(score) FROM students Stu INNER JOIN counties Cnt On Stu.county = Cnt.countyName GROUP BY city;"
        cursor.execute(sql_query)
        fetchQuery2 = cursor.fetchall()
        sql_query = """
                    CREATE VIEW vTemp AS
                    SELECT StuCity.city AS CityName, StuCity.name AS StuName, StuCity.score AS StuScore, ProfCity.name AS ProfName, ProfCity.age AS ProfAge
                    FROM (SELECT * FROM Students Stu INNER JOIN Counties Cnt ON Stu.county = Cnt.countyName) StuCity INNER JOIN (SELECT * FROM Professors Prof INNER JOIN Counties Cnt ON Prof.county = Cnt.countyName) ProfCity
                    ON StuCity.city = ProfCity.city;
                    """
        cursor.execute(sql_query)
        sql_query = """
                    SELECT ProfName, StuName
                    FROM vTemp, (SELECT CityName, MAX(StuScore) AS CityScore, MAX(ProfAge) AS CityAge FROM vTemp GROUP BY CityName) CityMax
                    WHERE vTemp.CityName = CityMax.CityName AND StuScore = CityScore AND ProfAge = CityAge;
                    """
        cursor.execute(sql_query)
        fetchQuery4 = cursor.fetchall()
        sql_query = """
                    DROP VIEW vTemp;
                    """
        cursor.execute(sql_query)

# - - - - - Query5 TIME START (201704144) - - - - -
        sql_query = """
                    CREATE VIEW vTemp AS
                    SELECT TotalList.city AS DangerCity
                    FROM
                    (SELECT city, COUNT(*) AS CityAll FROM (SELECT studentID,Cnt.city FROM Students Stu INNER JOIN Counties Cnt ON Stu.county = Cnt.countyName UNION SELECT facultyID,Cnt.city FROM Professors Prof INNER JOIN Counties Cnt ON Prof.county = Cnt.countyName UNION SELECT patientID, COVID.city FROM COVID INNER JOIN Counties Cnt ON COVID.city = Cnt.city) A GROUP BY city) TotalList,
                    (SELECT Cnt.city, COUNT(DISTINCT patientID) AS CityPatients FROM COVID INNER JOIN Counties Cnt ON COVID.city = Cnt.city GROUP BY Cnt.city) PatientsList
                    WHERE TotalList.city = PatientsList.city
                    ORDER BY CityPatients/CityAll DESC LIMIT 3;
                    """
        cursor.execute(sql_query)
        sql_query = """
                    SELECT name, city
                    FROM Students Stu INNER JOIN Counties Cnt ON Stu.county = Cnt.countyName
                    WHERE EXISTS (SELECT * FROM vTemp WHERE Cnt.city = DangerCity)
                    ORDER BY city;
                    """
        cursor.execute(sql_query)
# - - - - - Query5 TIME END (201704144) - - - - -
        fetchQuery5 = cursor.fetchall()
        sql_query = """
                    DROP VIEW vTemp;
                    """
        cursor.execute(sql_query)

        connection.commit()
        connection.close()

    for tmp in fetchQuery2:
        eachRow = {'cityName': tmp[0], 'averageScore': tmp[1]}
        outputQuery2.append(eachRow)
    for tmp in fetchQuery4:
        eachRow = {'professorName': tmp[0], 'studentName': tmp[1]}
        outputQuery4.append(eachRow)
    for tmp in fetchQuery5:
        eachRow = {'studentName': tmp[0], 'cityName': tmp[1]}
        outputQuery5.append(eachRow)

    result = {
        "Query2": outputQuery2,
        "Query4": outputQuery4,
        "Query5": outputQuery5
    }
    return JsonResponse(result)

def addCovid(request):
    if request.method == "POST":
        addCovid = json.loads(request.body)
        outputQuery5 = []
    with connection.cursor() as cursor:
        sql_query = "INSERT INTO covid VALUES ('{0}', '{1}');"\
            .format(addCovid['covid_id'], addCovid['covid_city'])
        cursor.execute(sql_query)

# - - - - - Query5 TIME START (201704144) - - - - -
        sql_query = """
                    CREATE VIEW vTemp AS
                    SELECT TotalList.city AS DangerCity
                    FROM
                    (SELECT city, COUNT(*) AS CityAll FROM (SELECT studentID,Cnt.city FROM Students Stu INNER JOIN Counties Cnt ON Stu.county = Cnt.countyName UNION SELECT facultyID,Cnt.city FROM Professors Prof INNER JOIN Counties Cnt ON Prof.county = Cnt.countyName UNION SELECT patientID, COVID.city FROM COVID INNER JOIN Counties Cnt ON COVID.city = Cnt.city) A GROUP BY city) TotalList,
                    (SELECT Cnt.city, COUNT(DISTINCT patientID) AS CityPatients FROM COVID INNER JOIN Counties Cnt ON COVID.city = Cnt.city GROUP BY Cnt.city) PatientsList
                    WHERE TotalList.city = PatientsList.city
                    ORDER BY CityPatients/CityAll DESC LIMIT 3;
                    """
        cursor.execute(sql_query)
        sql_query = """
                    SELECT name, city
                    FROM Students Stu INNER JOIN Counties Cnt ON Stu.county = Cnt.countyName
                    WHERE EXISTS (SELECT * FROM vTemp WHERE Cnt.city = DangerCity)
                    ORDER BY city;
                    """
        cursor.execute(sql_query)
# - - - - - Query5 TIME END (201704144) - - - - -
        fetchQuery5 = cursor.fetchall()
        sql_query = """
                    DROP VIEW vTemp;
                    """
        cursor.execute(sql_query)

        connection.commit()
        connection.close()

    for tmp in fetchQuery5:
        eachRow = {'studentName': tmp[0], 'cityName': tmp[1]}
        outputQuery5.append(eachRow)

    result = {
        "Query5": outputQuery5
    }
    return JsonResponse(result)

def clearStu(request):
    if request.method == "DELETE":
        with connection.cursor() as cursor:
            sql_query = "DELETE FROM students;"
            cursor.execute(sql_query)
            connection.commit()
            connection.close()
    return HttpResponse()

def clearProf(request):
    if request.method == "DELETE":
        with connection.cursor() as cursor:
            sql_query = "DELETE FROM professors;"
            cursor.execute(sql_query)
            connection.commit()
            connection.close()
    return HttpResponse()

def clearCnt(request):
    if request.method == "DELETE":
        with connection.cursor() as cursor:
            sql_query = "DELETE FROM counties;"
            cursor.execute(sql_query)
            connection.commit()
            connection.close()
    return HttpResponse()

def clearCovid(request):
    if request.method == "DELETE":
        with connection.cursor() as cursor:
            sql_query = "DELETE FROM covid;"
            cursor.execute(sql_query)
            connection.commit()
            connection.close()
    return HttpResponse()