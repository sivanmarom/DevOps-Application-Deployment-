with open("logfile.log", "r") as f:
    last_line = f.readlines()[-1]
    entry = last_line.strip().split(" :")
    timestamp = entry[0]
    message = entry[4]

print(f"{timestamp},{message}")