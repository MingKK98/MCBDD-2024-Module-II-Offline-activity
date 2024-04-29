from chembl_webresource_client.new_client import new_client

# Initialize the drug client
drug = new_client.drug

# Fetch all approved drugs
approved_drugs = drug.filter(max_phase=4)

# Count the number of approved drugs
number_of_approved_drugs = len(approved_drugs)

print(f"Total number of approved drugs: {number_of_approved_drugs}")
