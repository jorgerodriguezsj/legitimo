import re

regex = r"([A-Z]{2}[ \-]?[0-9]{2})(?=(?:[ \-]?[A-Z0-9]){9,30}$)((?:[ \-]?[A-Z0-9]{3,5}){2,7})([ \-]?[A-Z0-9]{1,3})?"

test_str = ("Factura VEN/2020/1507\n"
	"Número: FVT202005/011\n\n"
	"Dígitos IBAN: ES74 2100 4479 1002 0009 5616\n"
	"IBAN N°: ES3414740000150011760007\n"
	"IBAN ES81 0049 5010 7125 1725 6169\n"
	"IBAN ES1601822370410201504071\n"
	"XX00 1234 5678 9012 3456 7890 1234 5678 90\n"
	"YY00123456789012345678901234567890")

matches = re.finditer(regex, test_str, re.MULTILINE)

for matchNum, match in enumerate(matches, start=1):
    
    print ("Match {matchNum} was found at {start}-{end}: {match}".format(matchNum = matchNum, start = match.start(), end = match.end(), match = match.group()))
    
    for groupNum in range(0, len(match.groups())):
        groupNum = groupNum + 1
        
        print ("Group {groupNum} found at {start}-{end}: {group}".format(groupNum = groupNum, start = match.start(groupNum), end = match.end(groupNum), group = match.group(groupNum)))
