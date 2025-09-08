#!/bin/bash
set -e

# Function to print messages in color
print_message() {
  local COLOR=$1
  local MESSAGE=$2
  case $COLOR in
  "green")
    echo -e "\e[32m$MESSAGE\e[0m"
    ;;
  "yellow")
    echo -e "\e[33m$MESSAGE\e[0m"
    ;;
  "red")
    echo -e "\e[31m$MESSAGE\e[0m"
    ;;
  *)
    echo "$MESSAGE"
    ;;
  esac
}

print_message "green" "Starting Initialization (init_script.sh)!"
# python manage.py execute_something
# print_message "yellow" "Populating Database..."
# python manage.py runscript load_data
print_message "green" "Initialization completed successfully!"
