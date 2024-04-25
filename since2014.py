from chembl_webresource_client.new_client import new_client
from collections import defaultdict

def get_protein_targets(drug_chembl_id):
    # Using ChEMBL Web Service Client to retrieve protein targets for the drug
    targets = new_client.mechanism.filter(molecule_chembl_id=drug_chembl_id)
    # Extract UniProt IDs from the targets data
    uniprot_ids = []
    for target in targets:
        if 'target_chembl_id' in target and target['target_chembl_id']:
            # Extract UniProt ID from the ChEMBL ID (assuming it follows the pattern 'CHEMBLXXXXXXX')
            uniprot_id = target['target_chembl_id'].replace('CHEMBL', '')
            uniprot_ids.append(uniprot_id)
    return uniprot_ids



def calculate_average_targets_per_compound(drugs):
    total_targets = 0
    for i, drug in enumerate(drugs, start=1):
        drug_chembl_id = drug['molecule_chembl_id']
        # Get protein targets associated with the drug
        targets = get_protein_targets(drug_chembl_id)
        total_targets += len(targets)
        print("Processed drug {} out of {}: {} targets".format(i, len(drugs), len(targets)))
    # Calculate the average number of protein targets per compound
    average_targets_per_compound = total_targets / len(drugs)
    return average_targets_per_compound

if __name__ == "__main__":
    # Retrieve all approved drugs since 2014
    approved_drugs = new_client.drug.filter(max_phase=4, first_approval_year__gte=2014)
    # Calculate the average number of protein targets per compound
    average_targets = calculate_average_targets_per_compound(approved_drugs)
    print("Average number of protein targets per compound: {:.2f}".format(average_targets))
