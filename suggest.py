from pprint import pprint

import requests


# DONE: get total usage of each care type from invoice table (DB2)
# DONE: get current_insurance (name and coverage) from policy table (DB1)

# TODO: input the data to main function (suggest)
# TODO: create an endpoint for frontend
# TODO: write test cases to guarantee 100% coverage


def get_sum_per_caretype_from_api(customer_id):
    response = requests.get(f"http://localhost:5000/api/sum_per_caretype/{customer_id}")
    if response.status_code != 200:
        raise ValueError(response.text)
    data = response.json()
    results = []
    for e in data.get('results'):
        results.append(e)

    if len(results) < 2:
        results.append({'caretype': 'none', 'total': 'none'})

    return results


def get_insurance_coverage_from_api(customer_id):
    response =  requests.get(f"https://zi-webapp.azurewebsites.net/api/Customers/{customer_id}")
    if response.status_code != 200:
        raise ValueError(response.text)
    data = response.json()
    results = []
    insurance_name = (data.get('policies')[0]
               .get('additional_insurances')[0]
               .get('name')
    )
    coverage = (data.get('policies')[0]
               .get('additional_insurances')[0]
               .get('max_coverage')
    )
    results.append({"insurance_name": insurance_name, "coverage": coverage})

    if len(results) < 2:
        results.append({"insurance_name": "none", "coverage": "none"})

    return results


def suggest(usage, coverage, current_insurance, available_insurances):
    if not usage and not coverage:
        return "No suggestion."

    if not usage and coverage:
        return f"Maybe you don't need {current_insurance}."

    if usage <= coverage:
        return f"keep using {current_insurance}"

    for insurance in available_insurances:
        if usage <= insurance["coverage"]:
            return insurance

    return "Please contact us for advices."


def create_suggestion(customer_id):
    available_insurances = [
        {"name": "Tand 1", "coverage": 250, "cost": 10},
        {"name": "Tand 2", "coverage": 500, "cost": 20},
        {"name": "Tand 3", "coverage": 750, "cost": 30},
        {"name": "Fysiotherapie 1", "coverage": 250, "cost": 10},
        {"name": "Fysiotherapie 2", "coverage": 500, "cost": 20},
        {"name": "Fysiotherapie 3", "coverage": 750, "cost": 30},
    ]
    invoice_data = get_sum_per_caretype_from_api(customer_id)
    insurance_data = get_insurance_coverage_from_api(customer_id)
    for e in invoice_data:



def main():

    cid = 1
    pprint(get_sum_per_caretype_from_api(cid))
    pprint(get_insurance_coverage_from_api(cid))
    print('---------')
    return

    available_insurances = [
        {"name": "tand1", "coverage": 250, "cost": 10},
        {"name": "tand2", "coverage": 500, "cost": 20},
        {"name": "tand3", "coverage": 750, "cost": 30},
        {"name": "fysio1", "coverage": 250, "cost": 10},
        {"name": "fysio2", "coverage": 500, "cost": 20},
        {"name": "fysio3", "coverage": 750, "cost": 30},
    ]

    testcases = [
        {
            "current_insurance": "tand1",
            "usage": 325,
            "coverage": 250,
        },
        {
            "current_insurance": "tand1",
            "usage": 500,
            "coverage": 250,
        },
        {
            "current_insurance": "tand1",
            "usage": 750,
            "coverage": 250,
        },
        {
            "current_insurance": "tand1",
            "usage": 0,
            "coverage": 250,
        },
        {
            "current_insurance": "none",
            "usage": 0,
            "coverage": 0,
        },
        {
            "current_insurance": "none",
            "usage": 100,
            "coverage": 0,
        },
        {
            "current_insurance": "tand1",
            "usage": 10000,
            "coverage": 250,
        },
    ]

    for kwargs in testcases:
        print(suggest(**kwargs, available_insurances=available_insurances))


if __name__ == '__main__':
    main()
