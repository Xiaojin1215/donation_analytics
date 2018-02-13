#!/usr/bin/python
#
#python ./src/donation-analytics.py ./input/itcont.txt ./input/percentile.txt ./output/repeat_donors.txt
#Author: Xiaojin Liu
#For Insight Data Science -- Data Engineer -- Code Challenge
#Date: 02/11/2018
import sys
import argparse
import numpy as np
import time
import decimal as decimal

def check_cmte(cmte_id):
	""" Check cmte_id """
	if cmte_id is None:
		return False
	else:
		return True		
def check_name(name):
	""" Check name """
	if name is None:
		return False
	else:
		return True
def check_zip(zip_code):
	""" Check zip_code """
	if (zip_code is None or len(zip_code) < 5):
		return False
	else:
		return True

def check_date(trans_dt):
	if (trans_dt is None):
		return False
	else:
		try:
			""" Check the date format """
			time.strptime(trans_dt, "%m%d%Y")
			return True
		except:
			return False
def check_amount(trans_amt):
	if (trans_amt is None):
		return False
	else:
		return True

def check_other(other_id):
	if (other_id is None or other_id == ''):
		return True
	else:
		return False

def gen_res(recip_id, amt_list,first_line):
	""" recip_id : cmte_id|zip_code|year """
	""" output: cmte_id|zip_code|year|percentile|total_amt|total_num """
	amt_sum = sum(amt_list)
	amt_num = len(amt_list)
	""" percentile calculation """
	amt_array = np.array(amt_list)
	q = read_perc(args.percentile_file)
	prec_res = np.percentile(amt_array, int(q), overwrite_input = True, interpolation='nearest')
	prec_res = int(round(prec_res))
	final_res = recip_id+'|'+str(prec_res)+'|'+str(amt_sum)+'|'+str(amt_num)
	if (first_line == 1):
		with open(args.output_file,'w') as f:
			f.write(final_res)
			f.write("\n")
	else:
		with open(args.output_file,'a') as f:
			f.write(final_res)
			f.write("\n")

def read_perc(perc_file):
	with open(perc_file, 'r') as fh:
		for line in fh:
			perc_value = line.strip()
	return perc_value
	

if __name__ == "__main__":
	parse = argparse.ArgumentParser(description = 'Repeat Donors Data Information', formatter_class=argparse.ArgumentDefaultsHelpFormatter)
	parse.add_argument('input_file', help='Input file name')
	parse.add_argument('percentile_file', help='Input percentile file')
	parse.add_argument('output_file', help='Output file name')
	args = parse.parse_args()
	donors = {}
	recipient = {}
	first_line = 0
	""" Open input_file, read data line by line """
	with open(args.input_file, 'r') as fh:
		for line in fh:
			segs = line.strip().split('|')
			if (len(segs) < 21):
				print "Error: There is no enough features"
				continue
			cmte_id = segs[0]
			name = segs[7]
			zip_code = segs[10]
			trans_dt = segs[13]
			trans_amt = segs[14]
			other_id = segs[15]
			""" Check is this columns are qualified """
			if (check_cmte(cmte_id) and check_name(name) and check_zip(zip_code) and check_date(trans_dt) and check_amount(trans_amt) and check_other(other_id)):
				""" get first five digit in zip_code """
				zip_code = zip_code[:5]
				donor_id = name+"|"+zip_code
				date_tuple = time.strptime(trans_dt,"%m%d%Y")
				year = date_tuple.tm_year
				#time_stamp = time.mktime(date_tuple)
				""" Check if this donor donated before"""
				if not donors.has_key(donor_id):
					""" Not a repeat donor. Save the donor_id and year in donors dict """
					#not a repeat donor --> save the donor_id, and time_stamp in donors dictionary
					donors[donor_id] = year
				else:
					""" Donated before. Check if the donated year is the prior calendar year """
					if donors[donor_id] < year:
						recip_id = cmte_id + '|' + zip_code + '|' + str(year)
						""" Check if the recipient had record before """
						if not recipient.has_key(recip_id):
							amt_list= [decimal.Decimal(trans_amt)]
						else:
							amt_list = recipient[recip_id]
							amt_list.append(decimal.Decimal(trans_amt))
						recipient[recip_id] = amt_list
						""" Generate output data """
						if (first_line == 0):
							first_line = 1
						else:
							first_line = -1
						out_str = gen_res(recip_id, amt_list,first_line)
					else:
						""" The donor donated before, but the year is posterior, updated the year information """
						donors[donor_id] = year
