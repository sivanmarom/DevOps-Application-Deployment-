with open("logfile.log", "r") as f:
    last_line = f.readlines()[-1]
    print(last_line)
    entry = last_line.strip().split(":")
    print(entry)
    print(len(entry))
    timestamp = entry[0] + ":" + entry[1]
    message = entry[4].strip().replace('"', '\\"')

print(f"{timestamp}, {message}")
