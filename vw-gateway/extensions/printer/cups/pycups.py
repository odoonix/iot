import cups
conn = cups.Connection()
printers = conn.getPrinters()
printer_name = list(printers.keys())[1]

print(printer_name)

#printid = conn.printFile(printer_name, '/home/sanaz/working_dir/IOT_Odoo/extensions/printer/cups/a.txt','' , {})
c = conn.getJobs(which_jobs='all')

print(len(c))
