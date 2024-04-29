#USAGE : python id_replace.py <gff_filename>  <eggnog_filename> 
#The results are always saved in a file called eggnog_emapper.modified_annotations

# Step 1: Parse the GFF file to extract protein to transcript mapping
import sys
protein_to_transcript = {}
gff_file = sys.argv[1]
with open(gff_file, 'r') as gff_file:
    for line in gff_file:
        if 'Name' and 'Parent' in line:
            parts = line.split(';')            
            protein_id = parts[3].split('=')[1] # Extract protein ID
            
            transcript_id = [part for part in parts if 'Parent' in part][0].split('=')[1]
            #extract transcript_id
            protein_to_transcript[protein_id] = transcript_id
# print(protein_to_transcript)

# Step 2: Parse the EggNOG emapper annotations file and replace protein IDs with transcript IDs

#take the name of the eggnog emapper annotation file from the commandline
eggnog_file = sys.argv[2]
with open(eggnog_file, 'r') as annotations_file:
    lines = annotations_file.readlines()

modified_lines = []
for line in lines:
    parts = line.strip().split('\t')
    query_protein_id = parts[0]
    transcript_id = protein_to_transcript.get(query_protein_id, query_protein_id)  # Use protein ID if no mapping found
    parts[0] = transcript_id
    modified_lines.append('\t'.join(parts))

# Step 3: Write the modified annotations to a new file
with open('eggnog_emapper.modified_annotations', 'w') as output_file:
    output_file.write('\n'.join(modified_lines))
