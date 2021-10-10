from flask import Flask
from flask_cors import CORS
import requests
import time

app = Flask(__name__)
CORS(app)

@app.route('/')
def hello_world():  # put application's code here
    return 'Hello World!'

@app.route('/mygov/vaccination-stats')
def vaccination_stats():
    ts = time.time()
    response = requests.get("https://www.mygov.in/sites/default/files/covid/vaccine/vaccine_counts_today.json?timestamp={}".format(str(ts)))
    return response.json()
    
@app.route('/mygov/case-counts')
def case_counts():
    ts = time.time()
    response = requests.get("https://www.mygov.in/sites/default/files/covid/covid_state_counts_ver1.json?timestamp={{$timestamp}}".format(str(ts)))
    res = response.json()
    payload = {'confirmed': 0, 'active': 0, 'cured': 0, 'deaths': 0,
        'diff_confirmed': 0, 'diff_active': 0, 'diff_cured': 0, 'diff_deaths': 0, 'time': 0}
    if 'as_on' in res:
        payload['time'] = res['as_on']
    if 'Total Confirmed cases' in res:
        for i, case in res['Total Confirmed cases'].items():
            payload['confirmed'] += int(case)
    if 'Active' in res:
        for i, case in res['Active'].items():
            payload['active'] = payload['active'] + int(case)
    if 'Cured/Discharged/Migrated' in res:
        for i, case in res['Cured/Discharged/Migrated'].items():
            payload['cured'] += int(case)
    if 'Death' in res:
        for i, case in res['Death'].items():
            payload['deaths'] += int(case)
    if 'diff_confirmed_covid_cases' in res:
        for i, case in res['diff_confirmed_covid_cases'].items():
            payload['diff_confirmed'] += int(case)
    if 'diff_cured_discharged' in res:
        for i, case in res['diff_cured_discharged'].items():
            payload['diff_cured'] += int(case)
    if 'diff_death' in res:
        for i, case in res['diff_death'].items():
            payload['diff_deaths'] += int(case)
    if 'diff_active_covid_cases' in res:
        for i, case in res['diff_active_covid_cases'].items():
            payload['diff_active'] += int(case)
    return payload

if __name__ == '__main__':
    app.run()
