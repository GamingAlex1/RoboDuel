"""
Hello, you may feel free to edit and view whatever you would like here. If you encounter any errors
you can redownload the updater.py from the GitHub yourself(hopefully it works), happy coding :)

FYI: My code may be hideous to many, do not say I did not warn you, lol.
"""


import requests    # To get the data from the GitHub repository.
import shutil    # Moving directories, removing folders, files, etc.
import zipfile    # To unzip and zip the download of the GitHub.
import base64    # Used to decode the utf-8 strings.
import os    # Anying to do with the folder and file deletion, also used to move items.
import time    # Just used to track how long it took to execute the update.


def check_for_updates():
    """
    
░██████╗░██████╗░░█████╗░██████╗░  ██╗░░░██╗███████╗██████╗░░██████╗██╗░█████╗░███╗░░██╗
██╔════╝░██╔══██╗██╔══██╗██╔══██╗  ██║░░░██║██╔════╝██╔══██╗██╔════╝██║██╔══██╗████╗░██║
██║░░██╗░██████╔╝███████║██████╦╝  ╚██╗░██╔╝█████╗░░██████╔╝╚█████╗░██║██║░░██║██╔██╗██║
██║░░╚██╗██╔══██╗██╔══██║██╔══██╗  ░╚████╔╝░██╔══╝░░██╔══██╗░╚═══██╗██║██║░░██║██║╚████║
╚██████╔╝██║░░██║██║░░██║██████╦╝  ░░╚██╔╝░░███████╗██║░░██║██████╔╝██║╚█████╔╝██║░╚███║
░╚═════╝░╚═╝░░╚═╝╚═╝░░╚═╝╚═════╝░  ░░░╚═╝░░░╚══════╝╚═╝░░╚═╝╚═════╝░╚═╝░╚════╝░╚═╝░░╚══╝
    """
    # Making a request on the GitHub version.txt inside of the RoboDuel repository to make
    # sure that we are on the latest/outdated version of the GitHub repository.
    url = "https://api.github.com/repos/GamingAlex1/RoboDuel/contents/version.txt"
    headers = {"Accept": "application/vnd.github+json"}
    r = requests.get(url, headers=headers)

    # Reading the version from the local system to compare with the GitHub version later on.
    # Declaring a variable named "stored_version" as the version information.
    with open("version.txt", "r") as f:
        stored_version = f.read()

    # Getting/Trying to get the current version for the version.txt on the GitHub from the
    # call that we made before.
    try:
        current_version = r.json()["content"]
    # If we run into the GitHub API rate limit then we will stop and the user will have to
    # download it themselves :(
    except KeyError:
        print("Github API rate limit reached. Please try again later(1 hour or less from now).")
        return

    # The GitHub r.json call has utf-8 formatting so we want to decode that and make it
    # into readable and understandable version.
    current_version = current_version.strip()
    decoded_version = base64.b64decode(current_version).decode("utf-8")
    current_version = decoded_version

    # Make an x and y value for the number. The reason for this is because of the fact
    # later on it can't be declared as an interger from testing, at least I could not
    # find a way to do it.
    current_x, current_y = map(int, decoded_version.strip().split("."))
    stored_x, stored_y = map(int, stored_version.strip().split("."))


    """
██╗░░░██╗███████╗██████╗░░██████╗██╗░█████╗░███╗░░██╗  ░█████╗░██╗░░██╗███████╗░█████╗░██╗░░██╗
██║░░░██║██╔════╝██╔══██╗██╔════╝██║██╔══██╗████╗░██║  ██╔══██╗██║░░██║██╔════╝██╔══██╗██║░██╔╝
╚██╗░██╔╝█████╗░░██████╔╝╚█████╗░██║██║░░██║██╔██╗██║  ██║░░╚═╝███████║█████╗░░██║░░╚═╝█████═╝░
░╚████╔╝░██╔══╝░░██╔══██╗░╚═══██╗██║██║░░██║██║╚████║  ██║░░██╗██╔══██║██╔══╝░░██║░░██╗██╔═██╗░
░░╚██╔╝░░███████╗██║░░██║██████╔╝██║╚█████╔╝██║░╚███║  ╚█████╔╝██║░░██║███████╗╚█████╔╝██║░╚██╗
░░░╚═╝░░░╚══════╝╚═╝░░╚═╝╚═════╝░╚═╝░╚════╝░╚═╝░░╚══╝  ░╚════╝░╚═╝░░╚═╝╚══════╝░╚════╝░╚═╝░░╚═╝
    """

    # As the title suggests, this is a version checker, using current_version and stored_version
    # from the code above.
    
    # This is seeing if we have updates.
    # Example GitHub:1.1 > User:1.0
    if current_x > stored_x or (current_x == stored_x and current_y > stored_y):
        print(f"\nGitHub version: {current_version}Ur Current version: {stored_version}", end="\n\n")
        print("Updates are available.")
        print("Would you like to install them?")

        #Different function for more readability I guess.
        reply(current_version)

    # This is mostly an error that happens, likely this will never happen unless myself the developer has put the version down.
    # Example GitHub:1.0 < User:1.1
    elif current_x < stored_x or (current_x == stored_x and current_y < stored_y):
        print("Looks like you are using a newer version than the one on GitHub. Please report this to the developer.")
        exit()

    # Checking it he user is on the current version, if they are, they may obviously override it and just redownload.
    # Example GitHub:1.0 == User:1.0
    elif current_x == stored_x and current_y == stored_y:
        print("You are on the latest version.")
        print("Do you want to overide this?")
        reply(current_version)

    # If for some reason that there is an error while doing any of these if statments, no clue.
    else:
        print("ERROR: VERSION CHECK")
        quit()


def reply(current_version): # Different function for more readability.
    """
    
██╗░░░██╗███████╗░██████╗  ░█████╗░██████╗░  ███╗░░██╗░█████╗░
╚██╗░██╔╝██╔════╝██╔════╝  ██╔══██╗██╔══██╗  ████╗░██║██╔══██╗
░╚████╔╝░█████╗░░╚█████╗░  ██║░░██║██████╔╝  ██╔██╗██║██║░░██║
░░╚██╔╝░░██╔══╝░░░╚═══██╗  ██║░░██║██╔══██╗  ██║╚████║██║░░██║
░░░██║░░░███████╗██████╔╝  ╚█████╔╝██║░░██║  ██║░╚███║╚█████╔╝
░░░╚═╝░░░╚══════╝╚═════╝░  ░╚════╝░╚═╝░░╚═╝  ╚═╝░░╚══╝░╚════╝░
    """
    # Creating an input to the console, to ask the question "yes or no" to apply the update/download.
    yesNo = input("(y/n): ")

    # Create a list of valid responses for user input.
    valid_responses = ["y", "n", "yes", "no", "ok", "ye", "nah", "na", "negative", "positive", "sure", "yea", "yeah", "nope", "cancel", "reject", "never", "okay", "alright", "accept", "yup", "grant", "alrighty", "indeed", "permit", "agree", "agreed"]

    # While the user input is not in the list of valid responses, continue prompting for a valid response
    while yesNo.lower() not in valid_responses:
        print("Please enter a valid response.")
        yesNo = input("(y/n): ")

    # If the user input is yes, call the update_files function with the current version
    if yesNo.lower() in ["y", "yes", "ye", "ok", "positive", "sure", "yea", "yeah", "okay", "alright", "accept", "yup", "grant", "alrighty", "indeed", "permit", "agreed", "agree"]:
        update_files(current_version)
    # Otherwise, print a message indicating that the update process has been cancelled
    else:
        print("Ok, no problem.")



def update_files(current_version):
    """
    
██╗███╗░░██╗░██████╗████████╗░█████╗░██╗░░░░░██╗░░░░░  ██╗░░░██╗██████╗░██████╗░░█████╗░████████╗███████╗
██║████╗░██║██╔════╝╚══██╔══╝██╔══██╗██║░░░░░██║░░░░░  ██║░░░██║██╔══██╗██╔══██╗██╔══██╗╚══██╔══╝██╔════╝
██║██╔██╗██║╚█████╗░░░░██║░░░███████║██║░░░░░██║░░░░░  ██║░░░██║██████╔╝██║░░██║███████║░░░██║░░░█████╗░░
██║██║╚████║░╚═══██╗░░░██║░░░██╔══██║██║░░░░░██║░░░░░  ██║░░░██║██╔═══╝░██║░░██║██╔══██║░░░██║░░░██╔══╝░░
██║██║░╚███║██████╔╝░░░██║░░░██║░░██║███████╗███████╗  ╚██████╔╝██║░░░░░██████╔╝██║░░██║░░░██║░░░███████╗
╚═╝╚═╝░░╚══╝╚═════╝░░░░╚═╝░░░╚═╝░░╚═╝╚══════╝╚══════╝  ░╚═════╝░╚═╝░░░░░╚═════╝░╚═╝░░╚═╝░░░╚═╝░░░╚══════╝
    """
    # Start a timer to track the duration of the update process.
    startTime = time.time()

    # Open the version.txt file and rewrite it with the updated version number.
    with open("version.txt", "w") as f:
        f.write("")
        f.write(str(current_version))

    # Check if the update.zip file already exists and delete it to prevent errors.
    if os.path.exists("update.zip"):
        os.remove("update.zip")

    # Download the latest version of the program from the GitHub repository.
    download_url = "https://github.com/GamingAlex1/RoboDuel/archive/main.zip"
    r = requests.get(download_url, stream=True)

    # Save the downloaded file as update.zip
    with open("update.zip", "wb") as f:
        shutil.copyfileobj(r.raw, f)

    # Check if the "scripts" folder already exists, and delete it if it does.
    if os.path.exists("scripts"):
        shutil.rmtree("scripts")

    # Create a new "scripts" folder
    os.makedirs("scripts")

    # Extract the contents of update.zip to a temporary location called "temp"
    with zipfile.ZipFile("update.zip", "r") as z:
        z.extractall("temp")

    # Iterate through the items in the "temp/RoboDuel-main" folder
    for item in os.listdir("temp/RoboDuel-main"):
        
        # Set the source file path as the item in "temp/RoboDuel-main"
        src = os.path.join("temp/RoboDuel-main", item)
        
        # Set the destination file path as the item in the "scripts" folder
        dst = os.path.join("scripts", item)
        
        # Move the item from the source location to the destination location
        shutil.move(src, dst)

    # Remove the temporary "temp" folder and the unneeded files, such as README.md and updater.py
    shutil.rmtree("temp")
    os.remove("scripts/README.md")
    os.remove("scripts/updater.py")
    os.remove("scripts/version.txt")
    os.remove("update.zip")

    # Print a message to indicate that the update process was successful, along with the duration of the process in milliseconds and seconds.
    print("Downloaded was successfully in " + str(round((time.time() - startTime) * 1000)) + "ms(" + str(round(time.time() - startTime, 2)) + "s).")

def configUpdate():
    """
    
░█████╗░░█████╗░███╗░░██╗███████╗██╗░██████╗░  ██╗░░░██╗██████╗░██████╗░░█████╗░████████╗███████╗██████╗░
██╔══██╗██╔══██╗████╗░██║██╔════╝██║██╔════╝░  ██║░░░██║██╔══██╗██╔══██╗██╔══██╗╚══██╔══╝██╔════╝██╔══██╗
██║░░╚═╝██║░░██║██╔██╗██║█████╗░░██║██║░░██╗░  ██║░░░██║██████╔╝██║░░██║███████║░░░██║░░░█████╗░░██████╔╝
██║░░██╗██║░░██║██║╚████║██╔══╝░░██║██║░░╚██╗  ██║░░░██║██╔═══╝░██║░░██║██╔══██║░░░██║░░░██╔══╝░░██╔══██╗
╚█████╔╝╚█████╔╝██║░╚███║██║░░░░░██║╚██████╔╝  ╚██████╔╝██║░░░░░██████╔╝██║░░██║░░░██║░░░███████╗██║░░██║
░╚════╝░░╚════╝░╚═╝░░╚══╝╚═╝░░░░░╚═╝░╚═════╝░  ░╚═════╝░╚═╝░░░░░╚═════╝░╚═╝░░╚═╝░░░╚═╝░░░╚══════╝╚═╝░░╚═╝    
    """
    # This is in progress(if v1.0 is released with this, then no its not).
    print("Config Update")


def check_for_updates_api():
    # Make a request to the GitHub API to get the contents of the version.txt file
    # and saves the response in a variable named 'response'. If the status code is not 200, returns 'github_error'.
    url = "https://api.github.com/repos/GamingAlex1/RoboDuel/contents/version.txt"
    headers = {"Accept": "application/vnd.github+json"}
    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        return "github_error"

    # Get the current version from the file contents. If the key 'content' is not found in the json response, returns 'github_error'
    try:
        current_version = response.json()["content"]
    except KeyError:
        return "github_error"

    # Decode the current version using base64 decoding and then using utf-8 encoding and saves the version numbers in current_x and current_y
    decoded_version = base64.b64decode(current_version).decode("utf-8")
    current_x, current_y = map(int, decoded_version.strip().split("."))

    # Read the stored version from the file and saves the version numbers in stored_x and stored_y
    with open("version.txt", "r") as f:
        stored_version = f.read()
    stored_x, stored_y = map(int, stored_version.strip().split("."))

    # Compare the current and stored versions, returns False if current version is newer, False if stored version is newer and true if they are same.
    if current_x > stored_x or (current_x == stored_x and current_y > stored_y):
        return False
    elif current_x < stored_x or (current_x == stored_x and current_y < stored_y):
        return False
    elif current_x == stored_x and current_y == stored_y:
        return True



if __name__ == "__main__":
    check_for_updates()
