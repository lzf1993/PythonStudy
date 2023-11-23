
import csv

with open('us.csv', 'r') as csv_file:
    csv_reader = csv.reader(csv_file)

    with open('us2.csv', 'w') as new_file:  # Open a new file named 'new_titanic.csv' under write mode
        csv_writer = csv.writer(new_file, delimiter=';')  # making use of write method
        for line in csv_reader:  # for each file in csv_reader
            csv_writer.writerow(line)  # writing out to a new file from each line of the original file

