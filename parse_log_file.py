with open("logfile.log", "r") as f:
    last_line = f.readlines()[-1]
    entry = last_line.strip().split(" :")
    log_entry = {
        "timestamp": entry[0],
        "level": entry[1],
        "message": entry[2]
    }

print(log_entry)