# Generate .env example/template files from docker compose files

This tool generates .env (example) files directly from one or multiple docker compose files.

## Description

Whenenver changing the contents of docker compose files, it might happen that you want to hand over a new environment variable to a container but forget to declare it in the .env (example) file.
On the other side, it can also happen that you no longer hand over certain environment variables to your containers but forget to remove them from the .env (example) file.

Keeping .env (example) files up to date can be a tedious task when working with larger compose files.
This tool helps you to prevent you from forgetting to add or remove entries to the .env (example) file.
You can hand over one or multiple docker compose files to this script.

This script checks if the environment variables handed over in a docker compose file are defined in a given environment file.
If a variable is missing, it is appended to the environment file.
You then only have to add the value.
Otherwise, if a variable is no longer needed, you get a notice that you can remove the definition.

This tool does not check, if you provide all necessary environment variables needed for running a specific service.
It only checks if all environment variables handed over in compose files are present in the .env (example) files.

Further limitation: only variables with names written in completely upper case will be taken over to the .env (example) file (underscores are allowed). This can be adjusted in the script if necessary.

## Installation
The tool can be installed the following way:
1.  Clone this repo
2. Install the requirements using pip (e. g. by running `pip install --user -r requirements.txt`)
3. Make the python script executable (e.g.  by running `chmod u+x env-from-compose.py`)
4. Ensure the script is in a directory which is in the `$PATH` (e.g. by running `cp env-from-compose.py $HOME/bin/env-from-compose`)
5. Test if you can run the script by entering `env-from-compose` in your shell. The help of the script should now be shown.

## Usage

You can hand over docker compose files by using the `-i` operator. This operator can be used multiple times. 
The output file, the .env (example) file can be specified by using the `-o` operator.  This operator can be used once. 

Any content already present in the .env (example) file will be left untouched.  Missing variable names will be appended at the end of the file.  You will receive a notification about no longer needed variable names in the shell.

### Examples

#### One docker compose file
`$ env-from-compose -i docker-compose.yaml -o .env.example`

#### Multiple docker compose files
`$ env-from-compose -i docker-compose-1.yaml -i docker-compose-2.yaml -o .env.example`

## License
See LICENSE.txt
