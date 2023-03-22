import sys

import requests
import pyperclip
from bs4 import BeautifulSoup


class LicenseNotExistsException(Exception):
    pass


def manual_check(license_num):
    try:
        response = requests.get(f"https://www2.cslb.ca.gov/OnlineServices/CheckLicenseII/PersonnelList.aspx?LicNum={license_num}&LicName=VyslMjYrVytMQU5EU0NBUElORw==")
        # parse url and find href tags using BeautifulSoup
        soup = BeautifulSoup(response.text, 'html.parser')
        links = soup.find_all('a')
        # manual iteration to find and return personnel name
        personnel_name = links[24].text
        # raise exception if href_link returns "Check a License or HIS Registration"
        if "HIS" in personnel_name:
            raise LicenseNotExistsException
    except LicenseNotExistsException:
        print(f"[ERROR] License Number {license_num} does not exist.")
    else:
        # display name value
        print(personnel_name)
        # copy name to clipboard
        pyperclip.copy(personnel_name)


def bulk_check():
    while True:
        try:
            # create an empty 'licenses.txt' file
            open('licenses.txt', 'a').close()
            with open('licenses.txt', 'w') as f:
                # prompt user to input multiple license numbers
                print("Paste license numbers here (Double Press enter if done):")
                while True:
                    license_num = input()
                    # save user input to 'licenses.txt' if empty string is found
                    if license_num == "":
                        break
                    f.write(license_num + "\n")
            # read 'licenses.txt' and throw them to manual_check as license_num
            with open('licenses.txt', 'r') as f:
                for line in f:
                    license_num = line.strip()
                    manual_check(license_num)
        except IndexError:
            print(f"Invalid Input: '{license_num}'")
        yn = input("\nContinue checking? (Yes/No)\n> ")
        if 'n' in yn:
            break


print("  ___________   ___    _______           __          \n"
      " / ___/ __/ /  / _ )  / ___/ /  ___ ____/ /_____ ____\n"
      "/ /___\ \/ /__/ _  | / /__/ _ \/ -_) __/  '_/ -_) __/\n"
      "\___/___/____/____/  \___/_//_/\__/\__/_/\_\\__/_/   \n"
      "\tCSLB License Checker v2.0 | MLuayon\n")

option = input("\t\t[1] Manual Checker\n\t\t[2] Bulk Checker\n\t\t[3] Exit\n")
if option == '1':
    while True:
        try:
            manual_check(int(input("Enter License #: ")))
        except ValueError or IndexError:
            print("[ERROR] Invalid input.")
elif option == '2':
    bulk_check()
elif option == '3':
    sys.exit()
