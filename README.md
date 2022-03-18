# SFL Scientific Exercise

This program serves as an ETL pipeline to extract, transform, and load some data.

### Extract
The extraction step is done using Python's Pandas library. The `DATA.csv` file as well as the `datacenters.csv` (explained
in more detail in the Transform step) are read in using Pandas' `read_csv()` function. They are read in as DataFrames.

### Transform
To transform the data, I decided I would use the IP addresses to find the closest AWS region server for this user and
add that to the database as well. This is done using the https://ipinfo.io/ API to get location data from the IP
addresses.

Once the latitude and longitude is obtained from the IP address, I determine which AWS data center is the closest. This
is done using latitude and longitude data for the AWS data centers contained in the `datacenters.csv` file. This data
was obtained from: https://github.com/turnkeylinux/aws-datacenters/. To compute the distances, I use the geopy library.

#### API Token
While the IpInfo API allows many requests for free and without an account, you may run into issues if an API token is
not supplied. In order to allow more requests per day, I made a free account and provided my API token in the `.env` file.
A free account can be made at https://ipinfo.io/signup. Alternatively, the program can be run with the `--ignore_token`
flag (see Usage for more details). According to the API docs, only 1,000 requests/day are allowed without an API token.
Through my testing, I have found that I can run the program multiple times without a token provided (totaling over 1,000
requests), and it still does not return an error. If you are having issues, try supplying an API token.

### Load
Once all the data is extracted and transformed, it can be loaded into the database. I use a PostgreSQL database for this.
The table schema is contained in `db/init.sql`. The data is committed to the database all at once in one bulk insert.
The database name, user, and password must be supplied in the `.env` file for this to work properly.

## Usage

To properly run the program, some information needs to be added to the `.env` file. This file is in the `.gitignore`,
so private data won't be committed. The database name, database user, and database password are all required for the
load step. An API key for ipinfo.io is also required for the transform step if the `--ignore_token` flag is not set.

To install the dependencies, run `pip install -r requirements.txt`.

To run the program with the token, run `python main.py`.

Otherwise, run `python main.py --ignore_token`.