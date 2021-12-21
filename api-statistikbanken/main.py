""" """

import json
import requests
from typing import *
from datetime import datetime
from collections import defaultdict


api_url = r"https://api.statbank.dk/v1/"

def get_all_subjects_metadata() -> Dict:

    body = {"recursive": True, "includeTables": True} 
    r = requests.get(api_url + "subjects", params = body)
    return r.json()



def get_index_of_fitting_subjects(parents, subjects, requirements, data):

    data = defaultdict(dict)
    
    for subject in subjects:

        # The current subject is a folder,
        # and not the inner-most child
        if subject["hasSubjects"]:
            nested_data = get_index_of_fitting_subjects(parents + [subject["description"]], subject["subjects"], requirements, data)
            data.update(nested_data)

        # The subject is the inner-most
        # child, representing a specific
        # dataset
        elif subject["tables"] != []:
            for dataset in subject["tables"]:

                # Ensure that the dataset has all required variables
                if not any([req not in dataset["variables"] for req in requirements]):
                    dataset.update({"parents": parents})

                    data[dataset["text"]] = dataset
        
    return data    


def get_updateable_datasets(subjects: List[Dict]) -> List[Dict]:
    
    updateable_subjects = list()

    for key, values in subjects.items():
        
        if "updated" not in values:
            print(" [WARNING] : Subject has no field 'updated', cannot ensure the data is up-to-date")
            continue


        # Get the newest metadata for a given table
        r = requests.get(api_url + f"tableinfo/{values['id']}?lang=en")
        new_subject = r.json()
        
        # Convert strings to compareable datetime objects
        old_datetime_obj = datetime.strptime(values["updated"], "%Y-%m-%dT%X")
        new_datetime_obj = datetime.strptime(new_subject["updated"], "%Y-%m-%dT%X")

        # We've found a table that is not up-to-date
        if new_datetime_obj > old_datetime_obj:
            print(f" [WARNING] : {key} could be updated!")
            updateable_subjects.append(subjects[key])

    return updateable_subjects
        

def extend_metadata_for_all_subjects(subjects: List[Dict]) -> List[Dict]:

    for key, values in subjects.items():
        r = requests.get(api_url + f"tableinfo/{values['id']}?lang=en")
        subjects[key] = r.json()
        
    return subjects
        
    
    
def get_data_for_each_region_in_subject(subject: Dict) -> Dict:
    
    r = requests.get(api_url + f"data")
    
    




requirements = ["område"]

subjects = get_all_subjects_metadata()

data = get_index_of_fitting_subjects([], subjects, requirements, defaultdict(dict))
#updateable = get_updateable_datasets(data)
data = extend_metadata_for_all_subjects(data)





json.dump(data, open("out2.json", 'w'))
