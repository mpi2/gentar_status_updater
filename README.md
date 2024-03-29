# gentar_status_updater
An application to migrate the state of a phenotyping plan in GenTaR 

This project was written using python 3.9.4
and has been tested on OSX

## 1. Check your python installation:

```
python --version
```

## 2. Create a virtual environment for the project (requires Python 3.4+)

```
cd <name_of_cloned_github_repository>
python -m venv venv
```

## 3. To begin using the virtual environment, it needs to be activated:

```
source venv/bin/activate
```

## 4. Install the packages required for the project

```
pip install -r requirements.txt
```
---
## 5. Prepare to run the program.

### A) Edit the colonies.txt file.

Add each colony to be updated on a separate line and save the file.
e.g.
```
JR34077
JR34293
```
### B) Export environment variable with your user credential.
```
export GENTAR_USER=<username>
export GENTAR_PASSWORD=<gentar_password>
```
### C) Specify the service to update.
```
export GENTAR_ENV=SANDBOX
```
Note: You can use the <a href="https://www.gentar.org/production-tracker-sandbox/#/">SANDBOX</a> to test the update.
Use "export GENTAR_ENV=PRODUCTION" to update the main service.

### D) Optionally specify the type of phenotyping stage to update.
By default only 'early adult and embryo' phenotyping stages are modified.
Alternatively, you can select from one of these options:
```
export PHENOTYPING_STAGE=LATE_ADULT
export PHENOTYPING_STAGE=BOTH
export PHENOTYPING_STAGE=EARLY_ADULT_AND_EMBRYO
```

## 6. Invoke the program
```
python phenotyping_stage_status_transition_by_colony.py
```
This will produce the following sort of output
```
processing JR34077
JR34077 sucessfully updated
```
If the colony cannot be updated (e.g. because of the phenotyping stage or current status) you will only see the line stating that the colony is being processed. However, an error will be thrown if a colony name cannot be found and processing will stop. In this case, edit the colonies file to correct the name or remove the line and then restart the program.

---
## 7. Once you have finished working in the virtual environment clean up

```
deactivate
```

This puts you back to the system’s default Python interpreter
with all its installed libraries.


