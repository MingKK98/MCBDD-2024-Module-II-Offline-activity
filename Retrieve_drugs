from chembl_webresource_client.new_client import new_client

def retrieve_approved_drugs():
    # Using ChEMBL Web Service Client
    approved_drugs = new_client.drug
    # Retrieve all approved drugs
    approved_drugs = approved_drugs.filter(max_phase=4)
    # Sort drugs by approval year and name
    approved_drugs = approved_drugs.order_by(['first_approval_year', 'pref_name'])
    return approved_drugs

if __name__ == "__main__":
    drugs = retrieve_approved_drugs()
    print("Total number of approved drugs: {}".format(len(drugs)))
