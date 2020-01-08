# Extracting-Smiles-from-Pubchem

Vrinda Singhal - 4th December,2019 getting smiles from pubChem for compound names, using pubChem API.

Input File: List of ligands, with each ligand in new line.
Output File: <Ligand> , <Canonical_SMILES> , # Smile is left empty in case, not found

Please Note-
Remove multiple names for the same compound, i.e Donot include common name and IUPAC name together
For eg- ocean propanal (helional)- Either use helional or ocean propanol

Remove the solvent if mentioned. 
For eg: Ethylenedichloride (benzene) --> Ethylenedichloride

Remove any confusing optical information: 
For eg- dextro(r/(+))-limonene ---> limonene
