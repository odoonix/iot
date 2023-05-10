import cups
conn = cups.Connection()
printers = conn.getPrinters()
printer_name = list(printers.keys())[0]


#print(printers)


#print(printer_name)
#printid = conn.printFile(printer_name,'/home/sanaz/viraweb123/odoo-iot/vw-gateway/extensions/printer/cups/a.txt','' , {})
#print(printers.keys())


#print(cups.IPPError)
#print(cups.__dict__)
#print(conn)
#off 
# printer-state-message  Unplugged or turned off
# printer-state  5

#on
# printer-state  3


