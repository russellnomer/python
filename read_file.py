try:
    with open("data.txt", "r") as file:
        for line in file:
            line = line.strip()
            if "username:" in line:
                username = line.split(":")[1]
                print("Username:", username)
            elif "password:" in line:
                password = line.split(":")[1]
                print("Password:", password)

except FileNotFoundError:
    print("Error: data.txt not found.")




#Old red_file.py
#try:
#    with open("data.txt", "r") as file:
#        for line in file:
#            print(line.strip()) #remove newline characters
#except FileNotFoundError:
#    print("Error: data.txt not found.")