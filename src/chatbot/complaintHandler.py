import sqlshit as sql


def printComplaints():
    complaints = sql.getComplaints()
    for complaint in complaints:
        print(complaint[0])
