# Project Title

## Setting Up a Virtual Python Environment

1. Install the `virtualenv` package if it's not already installed. You can do this by running the following command in your terminal: 
 
```bash
pip install virtualenv
```
 
2. Navigate to your project directory and create a new virtual environment. Replace env with the name you want to give to your virtual environment: 
 
```bash
cd /path/to/your/project
virtualenv env
```
 
3. Activate the virtual environment: 
* On macOS and Linux: 
```bash
source env/bin/activate
```
* On Windows: 
```
.\env\Scripts\activate
```

4. Now you can install the project dependencies in the virtual environment: 
```bash
pip install -r requirements.txt
```

5. Make sure to have GOOGLE_MAPS_API_KEY= in a .env file
 
### Running the Scripts
The scripts in this project need to be run in a certain sequence. Here's the order: 

```
python extract_urls.py 
python extract_details.py
python calculate_airport_distance.py
python filter_schools.py
```

First artifact is a flat list of urls school_urls.xlsx
Second artifact is school details schools.xlsx
Third artifact script just adds distances to the existing schools.xlsx
Fourth script produces filtered_schools.xlsx

### License
This project is open-source and is licensed under the MIT License.