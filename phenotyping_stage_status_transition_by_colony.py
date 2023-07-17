import csv

import requests
import os
import sys


class Updater:

    def __init__(self):

        env = os.getenv('GENTAR_ENV', False)
        self.service = None

        if env == 'PRODUCTION':
            self.service = "https://www.gentar.org/tracker-api/"
        elif env == 'SANDBOX':
            self.service = "https://www.gentar.org/production-tracker-sandbox-api/"
        else:
            self.service = "http://127.0.0.1:8080/"

        self.api = "api/"
        self.token = None
        self.obtain_token()
        self.colonies = set()

    def read_colonies(self, file):
        filepath = os.path.join((os.path.dirname(os.path.abspath(__file__))), file)
        if os.path.isfile(filepath):
            with open(filepath, 'rt') as colonyfile:
                colony_reader = csv.reader(colonyfile, delimiter="\t")
                for row in colony_reader:
                    if row and row != "" and row[0] and row[0] != "":
                        self.colonies.add(row[0])

    def process_colonies(self):
        for colony in self.colonies:
            print("processing {}".format(colony))
            plan_data = self.fetch_gentar_plan(colony)
            plan = plan_data['_embedded']['plans'][0]
            stages = plan["phenotypingAttemptResponse"]["_links"]["phenotypingStages"]
            if len(stages) > 0:
                self.process_stages(stages, colony)
            else:
                print("No phenotyping stages for {}".format(colony))

    def process_stages(self, stages, colony):
        for stage_link in stages:
            stage_url = stage_link['href']
            stage_data = self.fetch_one_entry(stage_url)

            stage = stage_data['phenotypingTypeName']
            status = stage_data["statusName"]
            if stage == 'early adult and embryo' and status == 'Phenotyping Started':
                self.update_status(stage_data, colony, stage_url)

    def update_status(self, stage_data, colony, stage_url):
        stage_data["statusTransition"]["actionToExecute"] = "updateToPhenotypingAllDataSent"
        json, status = self.revise_service(stage_url, stage_data)
        if status == 200:
            print("{} sucessfully updated".format(colony))

    def obtain_token(self):
        user = os.getenv('GENTAR_USER')
        password = os.getenv('GENTAR_PASSWORD')
        if user is None or password is None:
            sys.exit("please export your GENTAR_USER and GENTAR_PASSWORD to the environment before running the script.")

        url = self.service + "auth/signin"
        headers = {'Content-Type': 'application/json', 'cache-control': 'no-cache'}
        credentials = {'userName': user, 'password': password}

        r = requests.post(url, headers=headers, json=credentials)

        if r.status_code == 200:
            self.token = r.json()['accessToken']
        else:
            r.raise_for_status()

    def update_token(self):
        try:
            self.obtain_token()
        except requests.exceptions.HTTPError:
            # Update the token to ensure it is valid
            # Tokens are valid for 3 hours so no need to process an error.
            pass

    def fetch_one_entry(self, url):
        headers = {'Content-Type': 'application/json',
                   'cache-control': 'no-cache',
                   'Authorization': 'Bearer ' + self.token}

        r = requests.get(url, headers=headers)
        r.raise_for_status()

        return r.json()

    def revise_service(self, url, data):
        headers = {'Content-Type': 'application/json',
                   'cache-control': 'no-cache',
                   'Authorization': 'Bearer ' + self.token}

        r = requests.put(url, headers=headers, json=data)
        r.raise_for_status()
        return r.json, r.status_code

    def fetch_gentar_plan(self, colony_name):
        url = self.service + self.api + "plans?phenotypingExternalRef=" + colony_name
        return self.fetch_one_entry(url)


if __name__ == '__main__':
    updater = Updater()
    updater.read_colonies("colonies.txt")
    updater.process_colonies()
