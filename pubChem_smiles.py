""" Vrinda Singhal - 4th December,2019 getting smiles from pubChem for compound names, using pubChem API.

Input File: List of ligands, with each ligand in new line.
Output File: <Ligand> , <Canonical_SMILES> , # Smile is left empty in case, not found

Please Note-
Remove multiple names for the same compound, i.e Donot include common name and IUPAC name together
For eg- ocean propanal (helional)- Either use helional or ocean propanol

Remove the solvent if mentioned. 
For eg: Ethylenedichloride (benzene) --> Ethylenedichloride

Remove any confusing optical information: 
For eg- dextro(r/(+))-limonene ---> limonene
"""

import requests
from requests.exceptions import HTTPError
import re


input_file = open("input_file", "r+")
output_file= open("output_file", "w+")
success_counter=0
http_error = 0
other_err=0
list_of_ligands= input_file.readlines()

dict_of_edits= {'γ':'Gamma', 'β':'Beta','-b-':'-beta-','α': 'Alpha', ' butyryllactate':  'butyryl lactate', 'g-Caprolactone' :'Gamma-Caprolactone', '23-Hexanedione':'2,3-Hexanedione',  '34-Hexanedione':'3,4-Hexanedione', 'phenylacetate':'phenyl acetate', ' (benzene)': '', '(-)-2-Phenylbutyric acid':'2-Phenylbutyric acid', '(+)-2-Phenylbutyric acid':  '2-Phenylbutyric acid'}

for ligand_no in range(len(list_of_ligands)):
	list_of_ligands[ligand_no] = list_of_ligands[ligand_no].strip()
	ligand_name=list_of_ligands[ligand_no]
	for symbol in dict_of_edits:
		if symbol in list_of_ligands[ligand_no]:
			
			list_of_ligands[ligand_no]=list_of_ligands[ligand_no].replace(symbol, dict_of_edits[symbol])
	list_of_ligands[ligand_no]= re.sub('\([0-9]R,[0-9]S\)-', "", list_of_ligands[ligand_no])
	output= ligand_name+ " : "
	isomeric_url='https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/name/'+list_of_ligands[ligand_no]+'/property/isomericSMILES/TXT'
	canonical_url='https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/name/'+list_of_ligands[ligand_no]+'/property/CanonicalSMILES/TXT'
	
	try:
		response = requests.get(canonical_url)
		response.raise_for_status()
	except HTTPError as http_err:
		try:
			response= requests.get(isomeric_url)
			response.raise_for_status()
		except HTTPError as h:
			print(f'HTTP error occurred: {h} for ', list_of_ligands[ligand_no])
			output_file.write(output)
			output_file.write('\n')
			http_error+=1

		else:
			smile = response.text.split()[0]
			output= output + smile
			output_file.write(output)
			if not(smile.endswith("\n")):
				output_file.write("\n")
			success_counter+=1
	except Exception as err:
		print(f'Other error occurred: {err} for ', list_of_ligands[ligand_no])
		output_file.write(output)
		output_file.write('\n')
		other_err+=1

	else:
		smile = response.text.split()[0]
		output= output + smile

		output_file.write(output)
		if not(smile.endswith("\n")):
			output_file.write("\n")
		success_counter+=1

print('\n\n\n' +'\033[92m'+'No of Success: ' + str(success_counter)+ "\nHTTP Error: " + str(http_error) + "\nOther Error: " + str(other_err)+'\x1b[0m'+'\n')
