from functions import get_airtable_records, create_empty_folders, create_pdf
from data import BASE_KEY, TABLE_NAME, CLASS


division_map = {
    'X': ['A','B','C','D','E','F','G'],
    'XI': ['A','B','C','D','E','F']
}

try:
    submissions = get_airtable_records(BASE_KEY, TABLE_NAME)
    create_empty_folders(division_map[CLASS])
    print('Number of files:' , len(submissions))
    
    print('Converting data...')

    fault_count = 0
    for test in submissions:  
        if not create_pdf(test):
            fault_count += 1
    print("Fault count:", fault_count)

except Exception as e:
    print(e)