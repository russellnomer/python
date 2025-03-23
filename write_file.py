data = ["user1:password1", "user2:password2", "user3:password3"]

with open("user_credentials.txt", "w") as file: # "w" write mode. overwrites file if exists
    for item in data:
        file.write(item + "\n") #adds a newline character to each line.

print("Data written to user_credentials.txt")