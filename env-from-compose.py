#!/bin/env python3

import argparse
from datetime import datetime
import re
import sys
import textwrap
import yaml

parser = argparse.ArgumentParser(
    description="Create environment file templates (.env.example) from docker compose files.",
    formatter_class=argparse.RawDescriptionHelpFormatter,
    epilog=textwrap.dedent("""
        Please report bugs to Tobias Tefke <tobias@tefke.name>
        The source code of this tool is available at <https://github.com/ttefke/env-from-compose>
        env-from-compose is made available under the terms of the GPLv2 license."""))
parser.add_argument("-i", "--input", action="append", help="name of the compose file(s) to be evaluated")
parser.add_argument("-o", "--output", help="name of environment file to be created or updated")
args = parser.parse_args()

if args.input == None or args.output == None: # No arguments provided
    parser.print_help()
else:
    new_environment_vars = list()
    # Read yaml file and get environment variables
    for yaml_file in args.input:
        # Load yaml
        try:
            compose_file = open(yaml_file, "r")
            yaml_rep = yaml.safe_load(compose_file)
            
            # Check if services are defined
            if yaml_rep == None or "services" not in yaml_rep:
                print("No container services defined in yaml file '" + yaml_file + "'")
                continue
            else:
                # Get environment variables from each service
                for service in yaml_rep["services"]:
                    current_service = yaml_rep["services"][service]
                    if "environment" not in current_service:
                        # Service does not receive any environment variables
                        continue
                    else:
                        # Service receives environment variables, add them to the list
                        environment = current_service["environment"]
                        for var in environment:
                            var_val = environment[var]
                            if var_val.startswith("$"):
                                if var not in new_environment_vars:
                                    new_environment_vars.append(var)
                            else:
                                print("The variable '" + var + "' of the service '" + service +
                                    "' is not relying on .env file values. Skipping.")
            compose_file.close()
        except FileNotFoundError:
            sys.exit("Could not open '" + yaml_file + "', aborting.")
        except yaml.scanner.ScannerError:
            sys.exit("File '" + yaml_file + "' does not contain valid YAML, aborting.")
    
    # Output 
    try:
        env_file = open(args.output, "a+")
        env_file.seek(0)
        
        # Get already defined environment variables
        env_re = re.compile("[A-Z_]*=")
        
        # Collect no longer needed environment variables in a list
        no_longer_needed_vars = list()
        
        # Look through already defined environment variables
        for line in env_file:
            # Check if variable is already defined
            line = line.strip()
            match = re.match(env_re, line)
            if match:
                # Get variable name
                var_name = match.group()
                var_name = var_name[0:len(var_name)-1]
                
                # Remove variable name from environment vars list,
                # as we don't want to have any double variables in the file
                if var_name in new_environment_vars:
                    new_environment_vars.remove(var_name)
                else:
                    # Collect no longer needed variables
                    if var_name not in no_longer_needed_vars:
                        no_longer_needed_vars.append(var_name)
        
        # Write new environment variables to list
        new_environment_vars.sort()
        env_file.write("\n# Appended by env-from-compose at " + datetime.now().strftime("%Y-%m-%d %H:%M:%S\n"))
        for var in new_environment_vars:
            env_file.write(var + "=\n")
        env_file.close()
        
        # Log no longer needed environment variables
        no_longer_needed_vars.sort()
        for var in no_longer_needed_vars:
            print("The variable '" + var + "' is no longer used by the specified compose files. It can be removed.")
        
    except FileNotFoundError:
        sys.exit("Could not write new environment variables to '" + args.output + "'.")
    print("The new environment variables (if any) were written to '" + args.output + "'.")
