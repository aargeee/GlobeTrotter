import requests
import time

# List of 20 tourist destinations
tourist_destinations = [
    "Rome", "Sydney", "Cape Town", "Vienna", "Athens",
    "Lisbon", "Madrid", "Seoul", "Beijing", "Shanghai",
    "Singapore", "Kuala Lumpur", "Bali", "Phuket", "Hanoi",
    "Ho Chi Minh City", "Jerusalem", "Tel Aviv", "Cairo", "Marrakech",
    "Casablanca", "Reykjavik", "Oslo", "Stockholm", "Helsinki",
    "Copenhagen", "Zurich", "Geneva", "Munich", "Florence",
    "Milan", "Naples", "Edinburgh", "Glasgow", "Dublin",
    "Belfast", "Brussels", "Budapest", "Warsaw", "Krakow",
    "Prague", "Santorini", "Mykonos", "Dubrovnik", "Split",
    "Zagreb", "Sofia", "Bucharest", "Belgrade", "Ljubljana",
    "Tallinn", "Riga", "Vilnius", "Baku", "Tbilisi",
    "Yerevan", "Doha", "Abu Dhabi", "Manama", "Muscat",
    "Kathmandu", "Colombo", "Male", "Maldives", "Seychelles",
    "Mauritius", "Cape Verde", "Zanzibar", "Nairobi", "Addis Ababa",
    "Cusco", "Lima", "Santiago", "Buenos Aires", "Montevideo",
    "Quito", "Bogota", "Cartagena", "Panama City", "San Jose",
    "Havana", "Kingston", "Nassau", "Reykjavik", "Anchorage",
    "Vancouver", "Montreal", "Quebec City", "Calgary", "Banff",
    "Auckland", "Wellington", "Christchurch", "Queenstown", "Fiji",
    "Tahiti", "Bora Bora", "Honolulu", "Maui", "Las Vegas",
    "Chicago", "Boston", "Washington D.C.", "Miami", "New Orleans"
]

# API endpoint and headers
url = 'https://aargeee2.pythonanywhere.com/api/destination/generate/'
headers = {
    'Content-Type': 'application/json',
    'Authorization': 'Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzQwOTIzMTYzLCJpYXQiOjE3NDA5MTk1NjMsImp0aSI6IjlhOGVhNDQ2OWZmZTQxYjViOTRkYTIzM2Q5MmUyNTg1IiwidXNlcl9pZCI6MX0.l_2INQc6hFIXFiYk1NF2WUK3qpboXBo4giHYlbUROsE'
}

# Function to send the request
def send_request(city):
    data = {
        "city": city
    }
    response = requests.post(url, headers=headers, json=data)
    if response.status_code == 201:
        print(f"Success: {city}")
    else:
        print(f"Failure: {city} - {response.status_code} - {response.text}")

# Limit to 12 requests per minute
for i, destination in enumerate(tourist_destinations):
    send_request(destination)
    print(".", end="")
    time.sleep(5)  # Wait for 10 seconds after every 12 requests
    print(".")

# Handle remaining requests (if any)
remaining_requests = len(tourist_destinations) % 12
if remaining_requests > 0:
    for destination in tourist_destinations[-remaining_requests:]:
        send_request(destination)