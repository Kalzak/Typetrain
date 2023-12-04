import json

def extract_error_data(filename):
    with open(filename, 'r') as file:
        data = json.load(file)
    
    error_sets = []

    # Iterate through all the failed words and their details
    for word, fail_details in data['fail_words'].items():
        for fail in fail_details:
            error_letter = fail['letter']
            correct_letter = word[fail['index']]
            preceding_letters = word[:fail['index']]

            error_sets.append({
                'expected_letter': correct_letter,
                'typed_letter': error_letter,
                'preceding_letters': preceding_letters
            })

    return data, error_sets

def find_most_common_leading_sequences(data, errors):
    error_frequency = {}
    
    # Extract success data
    success_data = {}
    for word, success_list in data['success_words'].items():
        for success in success_list:
            for i in range(len(word)):
                key = word[:i]
                if len(key) > 3:
                    key = key[-3:]
                if key not in success_data:
                    success_data[key] = 0
                success_data[key] += 1

    for error in errors:
        key = error['preceding_letters']
        if len(key) > 3:
            key = key[-3:]

        if key not in error_frequency:
            error_frequency[key] = {
                "frequency": 0,
                "actual_letter": {},
                "success_count": success_data.get(key, 0)  # Added success count
            }
        error_frequency[key]['frequency'] += 1
        if error['expected_letter'] not in error_frequency[key]['actual_letter']:
            error_frequency[key]['actual_letter'][error['expected_letter']] = 0
        error_frequency[key]['actual_letter'][error['expected_letter']] += 1

    # Sort by total errors
    #sorted_error_frequency = dict(sorted(error_frequency.items(), key=lambda x: x[1]['frequency'], reverse=False))
    # Sort by error rate 
    sorted_error_frequency = dict(sorted(error_frequency.items(), key=lambda x: x[1]['frequency'] / (x[1]['frequency'] + x[1]['success_count']), reverse=False))

    filtered_error_frequency = {k: v for k, v in sorted_error_frequency.items() if v['frequency'] >= 5}

    total_frequency = 0

    # Print the sorted data as specified
    for key, value in filtered_error_frequency.items():
        total_frequency += value['frequency']
        error_rate = value['frequency'] / (value['frequency'] + value['success_count'])  # Calculate error rate
        print(key, value['frequency'], "Error Rate:", error_rate * 100, "%")
        for actual_letter, frequency in value['actual_letter'].items():
            print("    ", actual_letter, ":", frequency)
        print()  # Add a newline between keys

    print(total_frequency)
    print(total_frequency-400)
    

if __name__ == "__main__":
    filename = "userdata.json"
    data, errors = extract_error_data(filename)
    
    # Print the error sets
    for error in errors:
        print(error)

    find_most_common_leading_sequences(data, errors)
