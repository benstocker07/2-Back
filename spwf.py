filename = "participant number.txt"

with open(filename, "r") as f:
    first_line = f.readline()
    words = first_line.split()
    participant_number = None
    for word in words:
        if word.isdigit():
            participant_number = int(word)

folder_name = f'Participant {participant_number}'
