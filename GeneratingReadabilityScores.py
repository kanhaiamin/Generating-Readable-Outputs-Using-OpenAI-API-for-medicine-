import csv
import textstat

#Add how may prompts you used. 
header = [
    "P1",
    "P2",
    "P3",
    "P4",
    "P5",
    "P6",
    "P7",
    "P8",
    "P9",
    "P10",
    "P11",
    "P12",
    "P13",
    "P14",
    "P15",
    "P16",
    "P17",
    "P18",
    "P19",
    "P20",
    "P21",
    "P22",
    "P23",
    "P24",
    "P25",
    "P26",
    "P27",
    "P28",
    "P29",
    "P30",
    "P31",
    "P32",

]

fields = ["Type", "Condition"]

for h in header:
    fields.append(h + " GF")
    fields.append(h + " FK")
    fields.append(h + " AR")
    fields.append(h + " CL")
    fields.append(h + " AVG")  # New column for average score

rows = []

with open('overall.csv', newline='') as csvfile:
    reader = csv.DictReader(csvfile)
    i = 0
    for row in reader:
        typ = row["Type"]
        report = row["Condition"]

        rowscores = [typ, report]

        for h in header:
            # Compute readability scores
            gf = textstat.gunning_fog(row[h])
            fk = textstat.flesch_kincaid_grade(row[h])
            ar = textstat.automated_readability_index(row[h])
            cl = textstat.coleman_liau_index(row[h])
            
            # Calculate average of the scores
            avg = (gf + fk + ar + cl) / 4.0

            # Append scores
            rowscores.extend([gf, fk, ar, cl, avg])  # Include average score

        rows.append(rowscores)
        print(i)
        i += 1

# Write the data to a new CSV
with open('trendsscores.csv', 'w') as csvfile:
    csvwriter = csv.writer(csvfile)
    csvwriter.writerow(fields)
    csvwriter.writerows(rows)
