from chembl_webresource_client.new_client import new_client

def get_protein_targets(drug_chembl_id):
    print(f"Retrieving targets for drug: {drug_chembl_id}")
    mechanisms = new_client.mechanism.filter(molecule_chembl_id=drug_chembl_id)
    uniprot_ids = []
    for mechanism in mechanisms:
        if mechanism['target_chembl_id']:
            target_info = new_client.target.filter(target_chembl_id=mechanism['target_chembl_id']).only('target_components')
            if target_info:
                target_components = target_info[0].get('target_components', [])
                for component in target_components:
                    if 'accession' in component:
                        uniprot_ids.append(component['accession'])
                        print(f"Found UniProt ID: {component['accession']} for target: {mechanism['target_chembl_id']}")
    return uniprot_ids

def calculate_average_targets_per_compound(drugs):
    total_targets = 0
    print(f"Starting to process {len(drugs)} drugs.")
    for i, drug in enumerate(drugs, start=1):
        drug_chembl_id = drug['molecule_chembl_id']
        targets = get_protein_targets(drug_chembl_id)
        total_targets += len(targets)
        print(f"Processed drug {i}/{len(drugs)}. Found {len(targets)} target(s).")
    average_targets_per_compound = total_targets / len(drugs)
    print(f"Completed processing all drugs.")
    return average_targets_per_compound

if __name__ == "__main__":
    # Retrieve all approved drugs since 2014
    approved_drugs = new_client.drug.filter(max_phase=4, first_approval__gte=2014).only('molecule_chembl_id')
    approved_drugs = list(approved_drugs)
    average_targets = calculate_average_targets_per_compound(approved_drugs)
    print(f"Average number of protein targets per compound: {average_targets:.2f}")
