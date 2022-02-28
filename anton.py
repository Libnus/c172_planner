import math

pi = math.pi

# LOAD NAVAIDS
input_navaids = open("Navaids.txt")
navaids = []
for line in input_navaids:
	aid = line.split(",")
	navaids.append(aid)

# LOAD WAYPOINTS
input_waypoints = open("Waypoints.txt")
waypoints = []
for line in input_waypoints:
	waypoint = line.split(",")
	waypoints.append(waypoint)

global last_location
global data

# def binary_search(arr, low, high, code):
# 	if high >= low:
# 		mid = (high+low)//2
# 		print(arr[mid][1])
# 		if arr[mid][1][0:4] == code:
# 			return mid
# 		elif arr[mid][1][0:4] > code:
# 			return binary_search(arr, low, mid-1, code)
# 		else:
# 			return binary_search(arr, mid+1, high, code)
# 	else:
# 		return -1

def get_location(airport_code):
	global last_location
	airport = []
	for navaid in navaids:
		if navaid[1][0:4] == airport_code or navaid[0] == airport_code:
			if(len(last_location) == 0 or (float(navaid[6]) >= last_location[0]-10 and float(navaid[6]) <= last_location[0]+10)):
				last_location = [float(navaid[6]), float(navaid[7])]
				return [float(navaid[6]), float(navaid[7])]

	if len(airport) == 0:
		for waypoint in waypoints:
			if waypoint[0] == airport_code:
				if(len(last_location) == 0 or (float(waypoint[1]) >= last_location[0]-10 and float(waypoint[2]) <= last_location[0]+10)):
					last_location = [float(waypoint[1]), float(waypoint[2])]
					return [float(waypoint[1]), float(waypoint[2])]
	print("not found")

def find_distance(dep, arr):

	R = 6371e3

	o1 =dep[0] * (pi/180)
	o2 = arr[0] * (pi/180)
	do = (arr[0]-dep[0]) * (pi/180)
	dh = (arr[1]-dep[1]) * (pi/180)

	a = math.sin(do/2) * math.sin(do/2) + \
		math.cos(o1) * math.cos(o2) * \
		math.sin(dh/2) * math.sin(dh/2)

	c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))

	total_distance = (R*c) / 1852
	return round(total_distance,1)

def calculate_time(distance, altitude):
	global data

	performance_cruise = {
		2000:  [116, 10.2],
		3000:  [117, 10.2],
		4000:  [118, 10.2],
		5000:  [119, 10.2],
		6000:  [120, 10.1],
		7000:  [121, 10.1],
		8000:  [122, 10.1],
		9000:  [122, 10.1],
		10000: [121, 9.6],
		11000: [119, 9.6],
		12000: [118, 8.8]
	}

#cruise
	performance_climb = {
		1000:  [73, 0, 0.4, 2],
		2000:  [73, 2, 0.8, 4],
		3000:  [73, 3, 1.3, 6],
		4000:  [73, 5, 1.7, 8],
		5000:  [73, 7, 2.2, 11],
		6000:  [72, 9, 2.7, 14],
		7000:  [72, 11, 3.1, 17],
		8000:  [72, 13, 3.6, 20],
		9000:  [72, 18, 4.2, 24],
		10000: [72, 21, 4.7, 28],
		11000: [72, 24, 5.3, 32],
		12000: [72, 27, 5.9, 37]
	}

	total_time = 0

	# calculate climb times from performance sheet
	climb_time = performance_climb.get(altitude)[1]
	print("Climb time:", climb_time, "min")
	print("Climb distance:", performance_climb.get(altitude)[3], "NM")
	#calculate total time
	# d = st
	distance_left = distance - performance_climb.get(altitude)[3]
	total_time = climb_time+((distance_left/performance_cruise.get(altitude)[0])*60)
	print("Total time: ", round(total_time), "min")

	# calculate total fuel
	time_in_hours = (total_time - climb_time) / 60 # convert to hours
	print("Fuel needed: ", round(time_in_hours*performance_cruise.get(altitude)[1] + performance_climb.get(altitude)[2], 1), "gal")
	print("Extra fuel: 30 minutes, 10 gal")

def main():
	global last_location
	welcome ="""

		
░█████╗░░░███╗░░███████╗██████╗░  ██████╗░██╗░░░░░░█████╗░███╗░░██╗███╗░░██╗███████╗██████╗░
██╔══██╗░████║░░╚════██║╚════██╗  ██╔══██╗██║░░░░░██╔══██╗████╗░██║████╗░██║██╔════╝██╔══██╗
██║░░╚═╝██╔██║░░░░░░██╔╝░░███╔═╝  ██████╔╝██║░░░░░███████║██╔██╗██║██╔██╗██║█████╗░░██████╔╝
██║░░██╗╚═╝██║░░░░░██╔╝░██╔══╝░░  ██╔═══╝░██║░░░░░██╔══██║██║╚████║██║╚████║██╔══╝░░██╔══██╗
╚█████╔╝███████╗░░██╔╝░░███████╗  ██║░░░░░███████╗██║░░██║██║░╚███║██║░╚███║███████╗██║░░██║
░╚════╝░╚══════╝░░╚═╝░░░╚══════╝  ╚═╝░░░░░╚══════╝╚═╝░░╚═╝╚═╝░░╚══╝╚═╝░░╚══╝╚══════╝╚═╝░░╚═╝
		"""

	

	print(welcome)
	print("Welcome to the ultimate flight C172 X-Plane planning tool!\n\n")

	departure = input("Please enter your departure(ICAO): ").upper() # TODO make sure its an actual altitude
	arrival = input("Please enter your arrival(ICAO: ").upper()
	flight_plan = input("Please enter your flight plan (NO SIDS OR ARRIVALS OR AIRPORTS SEPARATE WITH SPACES): ").split(' ')
	if(flight_plan[0] == ''): flight_plan.pop()
	altitude = round(int(input("\nPlease enter your planned altitude: ")),-3)
	
	flight_plan.insert(0, departure)
	flight_plan.append(arrival)
	distance = 0

	last_location = []
	#calculate each leg
	for i in range(len(flight_plan)-1):
		dep_location = get_location(flight_plan[i])
		arr_location = get_location(flight_plan[i+1])
		distance += find_distance(dep_location, arr_location)

	print("Distance:", distance, "NM")
	calculate_time(distance, altitude)
if __name__ == "__main__":
	main()

