import pandas

googleSheetId = '12MX7va9uq9Uy99Ev7qNIqDKmAFwNTbLGt7DNfyB83Nk'
worksheetName = 'Sheet1'
URL = 'https://docs.google.com/spreadsheets/d/{0}/gviz/tq?tqx=out:csv&sheet={1}'.format(
	googleSheetId,
	worksheetName
)

df = pandas.read_csv(URL)
print(df)