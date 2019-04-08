import PyPDF2
import re
import pprint

csv = open("output.csv", "w")
csv.write('Description, Date Sold, Sales Proceeds, Date Acquired, Cost, Washed Sale, Adjustment Amount\n')

pdfFileObj = open('1099-combo-Statement.pdf', 'rb')


# creating a pdf reader object
pdfReader = PyPDF2.PdfFileReader(pdfFileObj)

# printing number of pages in pdf file
print(pdfReader.numPages)

for j in range(8, 13):

# creating a page object
    pageObj = pdfReader.getPage(j)

    # extracting text from page
    t = pageObj.extractText()
    cusps = t.split("CUSIP:")

    header_junk = cusps.pop(0)
    for c in cusps:
        sales = []
        description = re.search(r":([\w, \(\)\.]*)\d+", c).groups()[0][:-1]
        description = description[5:]
        print(description)

        r_start = c.find(description) + len(description)

        if(re.search(r"[a-zA-Z]+",c[r_start:])):

            r_end = re.search(r"[a-zA-Z]+",c[r_start:]).start() + r_start
            records = c[r_start:r_end].split(' ')
        else:
            records = c[r_start:].split(' ')

        for (i, r) in zip(range(len(records)), records):

            sale = {"Description": "",
                    "Date Sold": "",
                    "Sales Proceeds":"",
                    "Date Acquired":"",
                    "Cost":"",
                    "Washed Sale":"",
                    "Adjustment Amount": ""
                    }

            parts = r.split('$')
            if len(parts) > 1:

                if i==0:

                    num_shares_decimal = records[i + 1].find('.')
                    sale["Description"] = description + ' ' + records[i + 1][:num_shares_decimal+4]
                    sale[ "Date Sold"] = parts[0][:8]
                    sale["Date Acquired"] =  parts[0][8:]

                else:
                    sale["Description"] = description + ' ' + records[i + 1][:5]
                    decimal = parts[0].find('.')
                    sale["Date Acquired"] = parts[0][decimal+4:decimal+4+8]
                    sale["Date Sold"] = parts[0][decimal+4+8:]

                sale["Sales Proceeds"] = parts[1].replace(',','')
                sale['Cost'] = parts[2].replace(',','')

                if parts[4]!= "0.00" and parts[4] != "0.00(":
                    sale["Washed Sale"] = "W"
                    sale["Adjustment Amount"] = parts[4].replace("(", '').replace(',','')

                sales.append(sale)

                csv.write(

                            sale["Description"] + ',' +
                            sale[ "Date Sold"] + ',' +
                            sale["Sales Proceeds"] + ',' +
                            sale["Date Acquired"] + ',' +
                            sale['Cost'] + ',' +
                            sale["Washed Sale"] + ',' +
                            sale["Adjustment Amount"] + '\n'
                )

        pprint.pprint(sales)



# closing the pdf file object
pdfFileObj.close()
csv.close()
