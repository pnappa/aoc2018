import datetime 

def extract_time(line):
    return line[line.find(":")-2:line.find("]")]
    
#input2 is simply $ sort input > input2

# guard num -> [(from, to), ...]
sleep_times = {}
guard_starts = []
with open('input2', 'r') as ifile:
    for line in ifile:
        lineTime = datetime.datetime.strptime(line[1:line.find("]")], "%Y-%m-%d %H:%M")
        print(lineTime)
        if "#" in line:
            guard_id = line[line.find("#")+1:line.find("begins")]
            if guard_id not in sleep_times:
                sleep_times[guard_id] = []

            guard_starts.append(guard_id)
        elif "falls" in line:
            sleep_times[guard_starts[-1]].append([lineTime])
        elif "wakes" in line:
            sleep_times[guard_starts[-1]][-1].append(lineTime)

print(sleep_times)

sleep_durations = {}
for guard_id, ranges in sleep_times.items():
    sleep_durations[guard_id] = datetime.timedelta()
    for slrange in ranges:
        duration = slrange[1]-slrange[0]
        sleep_durations[guard_id] += duration
        
print(sleep_durations)
sleepiest_guard = max(sleep_durations.items(), key=lambda x: x[1])[0]

sleepiest_times = [[0]*60 for _ in range(24)]

for rangeTime in sleep_times[sleepiest_guard]:
    start_time = rangeTime[0]
    num_mins = int((rangeTime[1]-rangeTime[0]).total_seconds() // 60)
    for i in range(num_mins):
        cHour = start_time.hour
        cMin = start_time.minute + i
        if cMin >= 60:
            cHour += cMin // 60
            cMin = cMin%60
            
        sleepiest_times[cHour][cMin] += 1

print(sleepiest_guard, sleepiest_times)


    

