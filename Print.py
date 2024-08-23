import cups
conn = cups.Connection()
printers = conn.getPrinters()

printer_name = list(printers.keys())[0]
print(printer_name)
test_page = '/home/temurbek/PycharmProjects/Chop/File.pdf'
job_id = conn.printFile(printer_name, test_page, "Test Print", {'page-ranges': '1'})
print(job_id)
# fileName = "bolprint.txt"
# conn.printFile(printer_name, fileName, " ", {})