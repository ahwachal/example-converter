#!/usr/bin/python
#Andrew Wachal
import cgi
import cgitb 

convTable = [["usdollar", "euro", .88],
             ["usdollar", "xarn", 26.2],
             ["usdollar", "icekrona", 119.88],
             ["xarn", "polandzloty", .1434198],
             ["icekrona", "galacticrock", .001029839],
             ["parsec", "lightyear", 3.26],
             ["lightyear", "kilometer", 95000000000000],
             ["lightyear", "mile", 5886000000000],
             ["xlarn", "parsec", 7.3672],
             ["galacticyear", "terrestrialyear", 250000000],
             ["xarnyear", "terrestrialyear", 1.2579],
             ["terrestrialyear", "terrestrialminute", 525600],
             ["bar", "kilopascal", 100],
             ["torr", "kilopascal", 0.1333223684211],
             ["psi", "torr", 51.71487786825],
             ["hour", "second", 3600],
             ["day", "hour", 24],
             ["hour", "minute", 60]]
#declaration of global constants
global unknown
unknown = '<p style="background-color:Blue;">unknown choice</p>'
global NOPATH
NOPATH = '<p style="color:Red;">NOPATH</p>'
global missing
missing = '<p style="color:Red;">missing</p>'
global nothingsub
nothingsub = "nothing submitted, nothing returned"
global noconv
noconv = "no conversion found"

#convert between two units given a number
def convert(inamount, myin, myout):
    #do nothing if nothing is input, will be handled elsewhere
    if inamount is None or myin is None or myout is None:
        return 0
    conversion = 0
    if myin == myout:
        conversion = 1
        return inamount
    for i in range(len(convTable)):
        if myin == convTable[i][0] and  myout == convTable[i][1]:
                conversion = convTable[i][2]
        elif myout == convTable[i][0] and  myin == convTable[i][1]:
                conversion = 1/convTable[i][2]
        elif myin == myout and (myin == convTable[i][0] or myin == convTable[i][1]):
            conversion = 1
    answer = inamount * conversion
    return answer

#find an array of rows where a given unit is found
def find(input, column):
    row = []
    row.append(-1)
    for i in range(len(convTable)):
        if input == convTable[i][column]:
            if -1 in row: 
                row.remove(-1)
            row.append(i)
    return row 

#find a path between two units
def ispath(maybein, maybeout):
    prev = NOPATH
    if maybein is None or maybeout is None:
        return prev
    elif maybein == maybeout:
        prev = maybein
        return prev
    #this is to do it both left to right and right to left
    for direction in range(2):
        if direction == 0:
            col0 = 0
            col1 = 1
        else:
            col0 = 1
            col1 = 0
        current = maybein
        #start from a different place in the table each time so the same path isn't followed
        starti = 0
        while current != maybeout and starti < len(convTable):
            i = starti
            current = maybein
            while i < len(convTable): 
                if current == convTable[i][col0]:
                    row = find(convTable[i][col1], col0)
                    if convTable[i][col1] == maybeout:
                        current = convTable[i][col1]
                        prev = convTable[i][col0]
                        ispath(current, maybeout)
                        #if the unit is found
                    elif row[0] != -1:
                        current = convTable[i][col1]
                        i = row[0]
                        #after trying that row, delete it from the array
                        if len(row) > 1:
                            del row[0]
                    else:
                        i += 1
                else: 
                    i += 1
            starti += 1
        #if it didn't work the first time, try iterating from bottom to top of table
        if prev == NOPATH:
            startj = len(convTable) - 1
            current = maybein
            while current != maybeout and startj > 0:
                j = startj
                current = maybein
                while j > 0:
                    if current == convTable[j][col0]:
                        row = find(convTable[j][col1], col0)
                        if convTable[j][col1] == maybeout:
                            current = convTable[i][col1]
                            prev = convTable[j][col0]
                            ispath(current, maybeout)
                        elif row[0] != -1:
                            current = convTable[j][col1]
                            j = row[0]
                            if len(row) > 1:
                                del row[0]
                        else:
                            j -= 1
                    else:
                        j -= 1
                startj -=1
                            
    return prev

#print table for part 1
def printTable1(myin, myout, inamount, answer):
    if myin is None:
        myin = missing
    if myout is None: 
        myout = missing
    if inamount is None:
        inamount = missing
    print '<table style="width:50%">'
    print "<tr>"
    print "<th>IN</th>"
    print "<th>OUT</th>"
    print "<th>QUANITY</th>"
    print "<th>ACTION</th>"
    print "<th>ANSWER/ERROR</th>"
    print "</tr>"
    print "<tr>"
    print "<td>",myin,"</td>"
    print "<td>",myout,"</td>"
    print "<td>",inamount,"</td>"
    print "<td>","        ","</td>"
    print "<td>",answer,"</td>"
    print "</tr>"
    print "</table>"

#print table for part 2
def printTable2(maybein, maybeout, path):
    if maybein is None:
        maybein = missing
    if maybeout is None:
        maybeout = missing
    print '<table style="width:50%">'
    print "<tr>"
    print "<th>MAYBEIN</th>"
    print "<th>MAYBEOUT</th>"
    print "<th>ANSWER/NOPATH</th>"
    print "</tr>"
    print "<tr>"
    print "<td>",maybein,"</td>"
    print "<td>",maybeout,"</td>"
    print "<td>",path,"</td>"
    print "</tr>"
    print "</table>"

#check that something was input and make it lowercase
def checkInput(input):
    if input is not None:
        input = input.lower()
        if findGen(input) == 0:
            input = unknown
        return input

#check to see if some unit is in the table in general
def findGen(input):
    found = 0
    for i in range(len(convTable)):
        if input == convTable[i][0] or input == convTable[i][1]:
            found = 1
    return found

#taken from https://stackoverflow.com/questions/379906/how-do-i-parse-a-string-to-a-float-or-int
#checks if a value can be converted to float, then converts if possible
def is_float(value):
    try:
        float(value)
        return True
    except:
        return False

def main():
    cgitb.enable()
    print "Content-type: text/html\n\n"
    print "<html>"
    print "<head>"
    print "<style>"
    print "table, th, td{"
    print "border: 1px solid black;"
    print "border-collapse: collapse;"
    print "</style>"
    print "</head>"
    print "<body>"
    form = cgi.FieldStorage()
    #if the first button is pushed
    button1 = form.getvalue("submit1")
    if button1 == "Make it so":
        #check inamount
        inamount = form.getvalue('inamount')
        inamountError = False
        if inamount is not None:
            if is_float(inamount) == True:
                inamount = float(inamount)
            else:
                inamount = '<p style="color:Green;">'+inamount+'</p>'
                inamountError = True
        myin = form.getvalue('myin')
        myin = checkInput(myin)
        myout = form.getvalue('myout')
        myout = checkInput(myout)
        if inamount is None and myin is None and myout is None:         #if nothing is input
            printTable1(" "," ", " ", "nothing submitted, nothing returned")
        elif myin == unknown or myout == unknown or inamount == unknown:    #unknowns submit
            printTable1(myin, myout, inamount, "unknown choice")
        elif inamountError == True:                                 #inamount is wrong
            printTable1(myin, myout, inamount, "invalid amount")
        else: 
            answer = convert(inamount, myin, myout)
            if answer == 0:
                answer = noconv
            printTable1(myin, myout, inamount, answer)
        
    #if the second button is pushed
    button2 = form.getvalue("submit2")
    if button2 == "Is path?":
        maybein = form.getvalue('maybein')
        maybein = checkInput(maybein)
        maybeout = form.getvalue('maybeout')
        maybeout = checkInput(maybeout)
        if maybein is None and maybeout is None:
            printTable2(" ", " ", nothingsub)
        elif maybein is None or maybeout is None:
            printTable2(maybein, maybeout, NOPATH)
        elif maybein == unknown or maybeout == unknown:
            printTable2(maybein, maybeout, "unknown choice")
        else:
            pathFound = False
            path = ispath(maybein, maybeout)
            printTable2(maybein, maybeout, path)
    print "</body>"
    print "</html>"
main()
