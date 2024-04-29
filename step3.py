from chembl_webresource_client.new_client import new_client
import requests
from collections import defaultdict
from operator import itemgetter

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
                        uniprot_id = component['accession']
                        uniprot_ids.append(uniprot_id)
                        print(f"Found UniProt ID: {uniprot_id} for target: {mechanism['target_chembl_id']}")
    return uniprot_ids

def get_uniprot_keywords(uniprot_ids):
    uniprot_keywords = defaultdict(int)
    print("Starting keyword retrieval from UniProt...")
    for uniprot_id in uniprot_ids:
        print(f"Fetching keywords for UniProt ID: {uniprot_id}")
        response = requests.get(f"https://www.ebi.ac.uk/proteins/api/proteins/{uniprot_id}")
        if response.ok:
            protein_data = response.json()
            keywords = protein_data.get('keywords', [])
            for keyword_entry in keywords:
                keyword = keyword_entry['value']
                uniprot_keywords[keyword] += 1
                print(f"Keyword '{keyword}' found for UniProt ID: {uniprot_id}")
        else:
            print(f"Failed to fetch data for UniProt ID: {uniprot_id}. HTTP Status: {response.status_code}")
    print("Completed keyword retrieval.")
    return uniprot_keywords

if __name__ == "__main__":
    # Retrieve all approved drugs since 2012
    print("Retrieving approved drugs since 2012...")
    approved_drugs = new_client.drug.filter(max_phase=4, first_approval__gte=2012).only('molecule_chembl_id')
    approved_drugs = list(approved_drugs)
    print(f"Number of approved drugs found: {len(approved_drugs)}")

    # Collect all UniProt IDs for approved drugs
    all_uniprot_ids = []
    for drug in approved_drugs:
        uniprot_ids = get_protein_targets(drug['molecule_chembl_id'])
        all_uniprot_ids.extend(uniprot_ids)
    print(f"Total UniProt IDs collected: {len(all_uniprot_ids)}")

    # Get UniProt keywords for all targets
    keywords_dict = get_uniprot_keywords(all_uniprot_ids)

    # Sort keywords by frequency and get top 5
    top_keywords = sorted(keywords_dict.items(), key=itemgetter(1), reverse=True)[:5]
    print("Top 5 keywords associated with the most drugs since 2012:")
    for keyword, count in top_keywords:
        print(f"{keyword}: {count}")
