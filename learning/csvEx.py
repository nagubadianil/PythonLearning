import csv

with open ('persons.csv', newline='') as f:
    csvfile = csv.reader(f)

    for row in csvfile:
        print(row)

# Open the file in write mode
with open("output.csv", "w") as csv_file:
    # Create a writer object
    csv_writer = csv.writer(csv_file)
    # Write the data to the file
    csv_writer.writerow(["Name", "Age", "Country"])
    csv_writer.writerow(["John Doe", 30, "United States"])
    csv_writer.writerow(["Jane Doe", 28, "Canada"])
    
# using CSV dialect
with open("output.csv", "w", newline="") as csv_file:
    # Create a writer object, using the `excel` dialect
    csv_writer = csv.writer(csv_file, dialect="excel")

# Define the custom dialect
csv.register_dialect("my_dialect",
        delimiter=";",
        quotechar='"',
        quoting=csv.QUOTE_MINIMAL
    )


                    