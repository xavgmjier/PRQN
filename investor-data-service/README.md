# Investor Data Service

## Install requirements

From the root folder:

``` bash
virtualenv -p python3 .venv
source .venv/bin/activate
pip3 install -r requirements.txt
```

### Build the Database

The database must be built before the webserver can be started

```InvestorCommitments.db``` will appear in the root directory after running the following command

From the root directory run:

``` bash
python3 main.py
```

### Start the Web Server

From the ```src``` directory run:

```bash
uvicorn main:app --reload
```

### Local Debug

After the web server has started, run the healthcheck by navigating to:

``` bash
http://127.0.0.1:8000  OR  http://localhost:8000
```

Read the API docs by navigating to:

``` bash
http://127.0.0.1:8000/docs
```

Make a call to the ```/investors/``` endpoint