# Converts CSV files to a format understood by YNAB4. The
# following banks are supported:
#
# 1) ROGERS Bank
# 2) PC Financial

import sys
import re
import datetime

def main():
	if (len(sys.argv) <= 1):
		print("Not enough arguments.");
		print("Usage: python csv_fixer.py FILENAME.csv");
		sys.exit();
	
	try:
		in_file = open(sys.argv[1], 'r');
		out_file = open("output.csv", 'w');
		
		bank = "";
		for line in in_file:
			# Delete instances of double quotations as this is not standard.
			modified_line = line.replace('"', '');
			
			# Strip the individual fields out of the line.
			fields = modified_line.split(',');

			# For the header, rename "Merchant Name" with Payee so it gets correctly imported into YNAB4.
			if (fields[0] == "Date"):
				bank = "ROGERS"
				modified_line = modified_line.replace("Merchant Name", "Payee");
			elif (fields[0] == "Merchant Name"):
				bank = "PCFINANCIAL"
				modified_line = modified_line.replace("Merchant Name", "Payee");
			elif (fields[0] == "Description"):
				bank = "PCFINANCIAL2"
				modified_line = modified_line.replace("Description", "Payee");
				
			# For transactions, convert the date from YYYY-MM-DD to MM/DD/YY.
			else:
				if (bank == "ROGERS"):
					date = datetime.datetime.strptime(fields[0], '%Y-%m-%d').strftime('%m/%d/%y')
					modified_line = modified_line.replace(fields[0], date);
					
					# Replace PAYMENT, THANK YOU with PAYMENT because ROGERS puts commas in CSV fields.
					modified_line = modified_line.replace("PAYMENT, THANK YOU", "PAYMENT");
				
				# CSV incorrectly lists outflows as positive. Mark all outflow value as negative.
				outflow_list = re.findall("[+-]?\d+\.\d+", modified_line);
				
				if (len(outflow_list) == 1):
					outflow = outflow_list[0];
					outflow_corrected = float(outflow) * -1;
					outflow_corrected = "%.2f" % outflow_corrected;
					modified_line = modified_line.replace(outflow, outflow_corrected);
			
			print "Modified Line:", modified_line;
			out_file.write(modified_line);
	
		in_file.close();
		out_file.close();
		
		print("Output file: output.csv");
		
	except:
		print "Could not open file", sys.argv[1];
	

main()