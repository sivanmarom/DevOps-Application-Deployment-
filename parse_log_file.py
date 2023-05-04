def parse_log_file(self):
    with open(self.log_file_path, "r") as f:
        last_line = f.readlines()[-1]
        entry = last_line.strip().split(" :")
        log_entry = {
            "timestamp": entry[0],
            "level": entry[1],
            "message": entry[2]
        }
    return log_entry