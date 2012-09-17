#!/usr/bin/env python3

#    Universitas
#    Copyright (C) 2009-2012, Carlo Stemberger
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.

"""A simple program to manage one's university transcript."""

import pickle
import datetime
#from lxml import etree

def ReadExams():
    try:
        f = open("exams.pck", "rb")
        list_of_exams = pickle.load(f)
        f.close()
        #print(list_of_exams) # NOTE: only for debugging
        #tree = etree.parse("test.xml")
        #print(etree.tostring(tree))
        return list_of_exams
    except:
        return 0

def WriteExams(list_of_exams):
    f = open("exams.pck", "wb")
    pickle.dump(list_of_exams, f)
    f.close()

def PrintTranscript():
    Separator = "-"*78
    print(Separator)
    print("   %-45s %-9s %-12s %s" % ("Exam", "Credits", "Date", "Mark"))
    print(Separator)
    ListOfExams = ReadExams()
    if ListOfExams:
        Number = 0
        for Exam in ListOfExams:
            Number += 1
            Name = Exam[0]
            Credits = Exam[1]
            Date = Exam[2].strftime("%d-%m-%Y")
            Mark = Exam[3]
            CumLaude = Exam[4]
            print("%-2d %-45s %-9d %-12s %2d%2s" % (Number, Name, Credits, Date, Mark, CumLaude))
    print(Separator)
    print("Avarage: %2.1f" % WeightedMean(ListOfExams))
    print(Separator)
    print()

def AddExam():
    name = input("Name: ")

    raw_credits = input("Credits: ")
    credits = ElaborateCredits(raw_credits)
    if credits == 0:
        print("Not valid value")
        print()
        return

    raw_date = input("Date (DDMMYYYY): ")
    date = ElaborateDate(raw_date)
    if date == 0:
        print("Not valid date")
        print()
        return

    raw_mark = input("Mark: ")
    mark = ElaborateMark(raw_mark)
    if mark == 0:
        print("Not valid value")
        print()
        return

    cum_laude = Laude(mark)

    list_of_exams = []
    if ReadExams():
        list_of_exams[0:0] = ReadExams()
    list_of_exams[len(list_of_exams):len(list_of_exams)] = [[name, credits, date, mark, cum_laude]]
    #print(list_of_exams) # NOTE: DEBUGGING
    WriteExams(list_of_exams)
    print()

def ModifyExam():
    ListOfExams = ReadExams()
    if ListOfExams:
        RawExam = input("Exam to modify: ")
        try:
            Exam = int(RawExam)-1
        except:
            print("Not valid value")
            print()
            return
        if Exam < len(ListOfExams):
            ListOfExams[Exam][0] = input("Name: ")

            RawCredits = input("Credits: ")
            Credits = ElaborateCredits(RawCredits)
            if Credits == 0:
                print("Not valid value")
                print()
                return
            ListOfExams[Exam][1] = Credits

            RawDate = input("Date (DDMMYYYY): ")
            Date = ElaborateDate(RawDate)
            if Date == 0:
                print("Not valid date")
                print()
                return
            ListOfExams[Exam][2] = Date

            RawMark = input("Mark: ")
            Mark = ElaborateMark(RawMark)
            if Mark == 0:
                print("Not valid value")
                print()
                return
            ListOfExams[Exam][3] = Mark

            ListOfExams[Exam][4] = Laude(ListOfExams[Exam][3])

            WriteExams(ListOfExams)
        else:
            print("Not valid value")
    else:
        print("No data to modify")
    print()

def DelExam():
    ListOfExams = ReadExams()
    if ListOfExams:
        RawExam = input("Exam to cancel: ")
        try:
            Exam = int(RawExam)-1
        except:
            print("Not valid value")
            print()
            return
        if Exam < len(ListOfExams):
            del ListOfExams[Exam]
            WriteExams(ListOfExams)
        else:
            print("Not valid value")
    else:
        print("No data to cancel")
    print()

def MoveExam():
    ListOfExams = ReadExams()
    if ListOfExams:
        RawExamPosition = input("Exam to move: ")
        try:
            ExamPosition = int(RawExamPosition)-1
        except:
            print("Not valid value")
            print()
            return
        RawNewPosition = input("New position: ")
        try:
            NewPosition = int(RawNewPosition)-1
        except:
            print("Not valid value")
            print()
            return
        if NewPosition == ExamPosition:
            return
        if ExamPosition < len(ListOfExams) and NewPosition < len(ListOfExams):
            if NewPosition < ExamPosition:
                ListOfExams[NewPosition:NewPosition] = [ListOfExams[ExamPosition]]
                del ListOfExams[ExamPosition+1]
            else:
                ListOfExams[NewPosition+1:NewPosition+1] = [ListOfExams[ExamPosition]]
                del ListOfExams[ExamPosition]
            WriteExams(ListOfExams)
        else:
            print("Not valid value")
    else:
        print("No data to move")
    print()

def TestNumbers(String):
    for Char in String:
        if Char < '0' or Char > '9':
            return 0
    return 1

def ElaborateCredits(RawCredits):
    Test = TestNumbers(RawCredits)
    if len(RawCredits) > 2 or Test == 0:
        return 0
    return int(RawCredits)

def ElaborateDate(RawDate):
    Test = TestNumbers(RawDate)
    if len(RawDate) != 8 or Test == 0:
        return 0
    Day = int(RawDate[:2])
    Month = int(RawDate[2:4])
    Year = int(RawDate[4:])
    try:
        return datetime.date(Year,Month,Day)
    except:
        return 0

def ElaborateMark(RawMark):
    Test = TestNumbers(RawMark)
    if Test == 0:
        return 0
    return int(RawMark)

def Laude(mark):
    cum_laude = ""
    if mark == 30:
        question = input("Cum laude (y/n)? ")
        if question == "y":
            cum_laude = "+l"
    return cum_laude

def WeightedMean(ListOfExams):
    if ListOfExams != 0:
        SumOfWeightedMark = 0
        SumOfCredits = 0
        for Exam in ListOfExams:
            SumOfWeightedMark = SumOfWeightedMark + (Exam[1]*Exam[3])
            SumOfCredits = SumOfCredits + Exam[1]
        return float(SumOfWeightedMark)/SumOfCredits
    else:
        return 0.0

if __name__ == "__main__":
    Switch = 1
    while Switch:
        Test = input("""\
    1. Show transcript
    2. Add exam
    3. Modify exam
    4. Delete exam
    5. Move exam
    6. Exit\n=> """)
        try:
            exec({'1': 'PrintTranscript()',
                  '2': 'AddExam()',
                  '3': 'ModifyExam()',
                  '4': 'DelExam()',
                  '5': 'MoveExam()',
                  '6': 'Switch = 0'}[Test])
        except:
            print("Not valid value")
            print()
