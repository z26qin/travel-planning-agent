import requests
from datetime import datetime, timedelta
import polyline

class TravelAPI:
    def __init__(self):
        # API keys would typically be stored securely, not hard-coded
        self.flight_api_key = "your_flight_api_key"
        self.hotel_api_key = "your_hotel_api_key"
        self.attraction_api_key = "your_attraction_api_key"
        
    def search_flights(self, origin, destination, dates):
        # Format dates properly for API
        formatted_dates = self._format_dates(dates)
        
        # In a real implementation, you would call an actual flight API
        # Examples: Skyscanner, Amadeus, Kiwi.com APIs
        
        # Mock data for demonstration
        return [
            {
                "airline": "Sample Airlines",
                "flight_number": "SA123",
                "departure": f"{origin} - {formatted_dates.get('departure', 'N/A')}",
                "arrival": f"{destination} - {formatted_dates.get('arrival', 'N/A')}",
                "price": "500.00 USD"
            },
            {
                "airline": "Another Airline",
                "flight_number": "AA456",
                "departure": f"{origin} - {formatted_dates.get('departure', 'N/A')}",
                "arrival": f"{destination} - {formatted_dates.get('arrival', 'N/A')}",
                "price": "450.00 USD"
            }
        ]
    
    def search_hotels(self, location, check_in, check_out, guests=1):
        # In a real implementation, you would call a hotel API
        # Examples: Booking.com, Hotels.com, Expedia APIs
        
        # Mock data for demonstration
        return [
            {
                "name": "Grand Hotel",
                "location": location,
                "check_in": check_in,
                "check_out": check_out,
                "price_per_night": "150.00 USD",
                "rating": 4.5
            },
            {
                "name": "Cozy Inn",
                "location": location,
                "check_in": check_in,
                "check_out": check_out,
                "price_per_night": "95.00 USD",
                "rating": 4.2
            }
        ]
    
    def search_attractions(self, location):
        # In a real implementation, you would call an attractions API
        # Examples: Google Places, TripAdvisor, Yelp APIs
        
        # Generate mock data based on location
        attractions = []
        
        # Different attractions for different cities
        if "paris" in location.lower():
            attractions = [
                {
                    "name": "Eiffel Tower",
                    "category": "historical",
                    "rating": 4.7,
                    "description": "Iconic iron tower with panoramic city views."
                },
                {
                    "name": "Louvre Museum",
                    "category": "culture",
                    "rating": 4.8,
                    "description": "World's largest art museum and historic monument."
                },
                {
                    "name": "Luxembourg Gardens",
                    "category": "outdoors",
                    "rating": 4.6,
                    "description": "Beautiful garden with fountains and statues."
                }
            ]
        elif "new york" in location.lower():
            attractions = [
                {
                    "name": "Empire State Building",
                    "category": "historical",
                    "rating": 4.7,
                    "description": "Iconic 102-story skyscraper with observation decks."
                },
                {
                    "name": "Central Park",
                    "category": "outdoors",
                    "rating": 4.8,
                    "description": "Urban park spanning 843 acres in the heart of Manhattan."
                },
                {
                    "name": "Metropolitan Museum of Art",
                    "category": "culture",
                    "rating": 4.9,
                    "description": "One of the world's largest and finest art museums."
                }
            ]
        else:
            attractions = [
                {
                    "name": "Famous Museum",
                    "category": "culture",
                    "rating": 4.7,
                    "description": "A world-renowned museum featuring art and artifacts."
                },
                {
                    "name": "City Park",
                    "category": "outdoors",
                    "rating": 4.5,
                    "description": "Beautiful urban park with walking trails."
                },
                {
                    "name": "Historic District",
                    "category": "historical",
                    "rating": 4.6,
                    "description": "Charming area with historic buildings and shops."
                }
            ]
        
        return attractions
    
    def _format_dates(self, date_texts):
        # Convert natural language date mentions to structured format
        # This is a simplified version; real implementation would be more robust
        
        now = datetime.now()
        dates = {}
        
        if not date_texts:
            # Default to a trip starting in a week
            departure = now + timedelta(days=7)
            return {
                "departure": departure.strftime("%Y-%m-%d"),
                "arrival": (departure + timedelta(days=7)).strftime("%Y-%m-%d")
            }
            
        # Very simple parsing - would use a more sophisticated approach in production
        for date_text in date_texts:
            date_lower = date_text.lower()
            if "tomorrow" in date_lower:
                departure = now + timedelta(days=1)
                dates["departure"] = departure.strftime("%Y-%m-%d")
                dates["arrival"] = (departure + timedelta(days=7)).strftime("%Y-%m-%d")
            elif "next week" in date_lower:
                departure = now + timedelta(days=7)
                dates["departure"] = departure.strftime("%Y-%m-%d")
                dates["arrival"] = (departure + timedelta(days=7)).strftime("%Y-%m-%d")
            elif "next month" in date_lower:
                departure = now + timedelta(days=30)
                dates["departure"] = departure.strftime("%Y-%m-%d")
                dates["arrival"] = (departure + timedelta(days=7)).strftime("%Y-%m-%d")
                
        return dates

class ExpediaService:
    def __init__(self, api_key):
        self.api_key = api_key
        self.base_url = "https://hotels4.p.rapidapi.com/"
        self.headers = {
            "X-RapidAPI-Key": self.api_key,
            "X-RapidAPI-Host": "hotels4.p.rapidapi.com"
        }
    
    def search_hotels(self, location, check_in, check_out, guests=1):
        # Get location ID
        location_id = self._get_location_id(location)
        
        url = f"{self.base_url}properties/list"
        
        payload = {
            "destination": {"regionId": location_id},
            "checkInDate": {
                "day": check_in.day,
                "month": check_in.month,
                "year": check_in.year
            },
            "checkOutDate": {
                "day": check_out.day,
                "month": check_out.month,
                "year": check_out.year
            },
            "rooms": [{"adults": guests}],
            "resultsStartingIndex": 0,
            "resultsSize": 20,
            "sort": "PRICE_LOW_TO_HIGH"
        }
        
        response = requests.post(url, json=payload, headers=self.headers)
        
        if response.status_code == 200:
            return self._parse_hotels(response.json())
        else:
            raise Exception(f"Expedia API error: {response.status_code}")
    
    def _get_location_id(self, location):
        url = f"{self.base_url}locations/v2/search"
        querystring = {"query": location, "locale": "en_US"}
        
        response = requests.get(url, headers=self.headers, params=querystring)
        
        if response.status_code == 200:
            data = response.json()
            suggestions = data.get("suggestions", [])
            for group in suggestions:
                if group.get("group") == "CITY_GROUP":
                    entities = group.get("entities", [])
                    if entities:
                        return entities[0].get("destinationId")
        
        raise Exception(f"Location search error: {response.status_code}")
    
    def _parse_hotels(self, data):
        hotels = []
        
        for hotel in data.get("data", {}).get("body", {}).get("searchResults", {}).get("results", []):
            hotels.append({
                "name": hotel.get("name"),
                "address": hotel.get("address", {}).get("streetAddress", ""),
                "rating": hotel.get("starRating", 0),
                "price": hotel.get("ratePlan", {}).get("price", {}).get("current", ""),
                "image": hotel.get("optimizedThumbUrls", {}).get("srpDesktop", "")
            })
            
        return hotels

class GooglePlacesService:
    def __init__(self, api_key):
        self.api_key = api_key
        self.base_url = "https://maps.googleapis.com/maps/api/place/"
    
    def search_attractions(self, location, radius=5000, type="tourist_attraction"):
        # First, get location coordinates
        coordinates = self._geocode_location(location)
        if not coordinates:
            raise Exception(f"Could not geocode location: {location}")
        
        # Search for attractions
        url = f"{self.base_url}nearbysearch/json"
        
        params = {
            "location": f"{coordinates['lat']},{coordinates['lng']}",
            "radius": radius,
            "type": type,
            "key": self.api_key
        }
        
        response = requests.get(url, params=params)
        
        if response.status_code == 200:
            data = response.json()
            if data.get("status") == "OK":
                return self._parse_attractions(data)
            else:
                raise Exception(f"Google Places API error: {data.get('status')}")
        else:
            raise Exception(f"Google Places API error: {response.status_code}")
    
    def _geocode_location(self, location):
        url = "https://maps.googleapis.com/maps/api/geocode/json"
        
        params = {
            "address": location,
            "key": self.api_key
        }
        
        response = requests.get(url, params=params)
        
        if response.status_code == 200:
            data = response.json()
            if data.get("status") == "OK" and data.get("results"):
                return data["results"][0]["geometry"]["location"]
        
        return None
    
    def _parse_attractions(self, data):
        attractions = []
        
        for place in data.get("results", []):
            # Get more details for top attractions
            if place.get("rating", 0) >= 4.0:
                details = self._get_place_details(place.get("place_id"))
            else:
                details = {}
                
            attractions.append({
                "name": place.get("name"),
                "address": place.get("vicinity"),
                "rating": place.get("rating", 0),
                "total_ratings": place.get("user_ratings_total", 0),
                "location": place.get("geometry", {}).get("location", {}),
                "photo": self._get_photo_url(place.get("photos", [{}])[0].get("photo_reference")) if place.get("photos") else "",
                "types": place.get("types", []),
                "website": details.get("website", ""),
                "phone": details.get("formatted_phone_number", ""),
                "opening_hours": details.get("opening_hours", {}).get("weekday_text", [])
            })
            
        return attractions
    
    def _get_place_details(self, place_id):
        url = f"{self.base_url}details/json"
        
        params = {
            "place_id": place_id,
            "fields": "name,rating,formatted_phone_number,website,opening_hours,review",
            "key": self.api_key
        }
        
        response = requests.get(url, params=params)
        
        if response.status_code == 200:
            data = response.json()
            if data.get("status") == "OK":
                return data.get("result", {})
        
        return {}
    
    def _get_photo_url(self, photo_reference, max_width=400):
        if not photo_reference:
            return ""
            
        return f"{self.base_url}photo?maxwidth={max_width}&photoreference={photo_reference}&key={self.api_key}"

class GoogleMapsService:
    def __init__(self, api_key):
        self.api_key = api_key
        self.base_url = "https://maps.googleapis.com/maps/api/"
    
    def get_directions(self, origin, destination, mode="walking", waypoints=None):
        url = f"{self.base_url}directions/json"
        
        params = {
            "origin": origin,
            "destination": destination,
            "mode": mode,
            "key": self.api_key
        }
        
        if waypoints:
            params["waypoints"] = "|".join(waypoints)
        
        response = requests.get(url, params=params)
        
        if response.status_code == 200:
            data = response.json()
            if data.get("status") == "OK":
                return self._parse_directions(data)
            else:
                raise Exception(f"Directions API error: {data.get('status')}")
        else:
            raise Exception(f"Google Maps API error: {response.status_code}")
    
    def _parse_directions(self, data):
        route_data = {
            "distance": data["routes"][0]["legs"][0]["distance"]["text"],
            "duration": data["routes"][0]["legs"][0]["duration"]["text"],
            "start_address": data["routes"][0]["legs"][0]["start_address"],
            "end_address": data["routes"][0]["legs"][0]["end_address"],
            "steps": [],
            "polyline": data["routes"][0]["overview_polyline"]["points"],
            "decoded_polyline": polyline.decode(data["routes"][0]["overview_polyline"]["points"])
        }
        
        for step in data["routes"][0]["legs"][0]["steps"]:
            route_data["steps"].append({
                "instruction": step["html_instructions"],
                "distance": step["distance"]["text"],
                "duration": step["duration"]["text"]
            })
        
        return route_data
    
    def get_static_map(self, center=None, zoom=13, size="600x300", markers=None, path=None):
        url = f"{self.base_url}staticmap"
        
        params = {
            "key": self.api_key,
            "size": size
        }
        
        if center:
            params["center"] = center
            params["zoom"] = zoom
        
        if markers:
            for marker in markers:
                params[f"markers=color:red|{marker}"] = ""
        
        if path:
            params["path"] = f"weight:3|color:blue|enc:{path}"
        
        return url + "?" + "&".join([f"{k}={v}" for k, v in params.items() if v])

class WeatherService:
    def __init__(self, api_key):
        self.api_key = api_key
        self.base_url = "https://api.weather.com/v3/"
    
    def get_forecast(self, location, days=5):
        # First get location coordinates
        coordinates = self._get_location_coordinates(location)
        
        url = f"{self.base_url}wx/forecast/daily/{days}day"
        
        params = {
            "geocode": f"{coordinates['lat']},{coordinates['lng']}",
            "format": "json",
            "units": "e",  # e for imperial, m for metric
            "language": "en-US",
            "apiKey": self.api_key
        }
        
        response = requests.get(url, params=params)
        
        if response.status_code == 200:
            return self._parse_forecast(response.json())
        else:
            raise Exception(f"Weather API error: {response.status_code}")
    
    def _get_location_coordinates(self, location):
        url = f"{self.base_url}location/search"
        
        params = {
            "query": location,
            "locationType": "city",
            "language": "en-US",
            "format": "json",
            "apiKey": self.api_key
        }
        
        response = requests.get(url, params=params)
        
        if response.status_code == 200:
            data = response.json()
            return {
                "lat": data["location"]["latitude"][0],
                "lng": data["location"]["longitude"][0]
            }
        else:
            raise Exception(f"Location search error: {response.status_code}")
    
    def _parse_forecast(self, data):
        forecast = []
        
        for i in range(len(data["calendarDayTemperatureMax"])):
            day_data = {
                "date": (datetime.now() + timedelta(days=i)).strftime("%Y-%m-%d"),
                "temp_max": data["calendarDayTemperatureMax"][i],
                "temp_min": data["calendarDayTemperatureMin"][i],
                "narrative": data["narrative"][i],
                "precipitation_chance": data["daypart"][0]["precipChance"][i*2],
                "wind_speed": data["daypart"][0]["windSpeed"][i*2],
                "humidity": data["daypart"][0]["relativeHumidity"][i*2],
                "weather_type": data["daypart"][0]["wxPhraseLong"][i*2],
                "icon_code": data["daypart"][0]["iconCode"][i*2]
            }
            forecast.append(day_data)
            
        return forecast

class APIManager:
    def __init__(self, api_keys):
        self.api_keys = api_keys
        self.services = {}
        
    def get_flight_data(self, origin, destination, departure_date, return_date=None):
        """Try multiple flight APIs in sequence if primary fails"""
        try:
            # Try Skyscanner first
            if not self.services.get("skyscanner"):
                from .flight_service import SkyscannerService
                self.services["skyscanner"] = SkyscannerService(self.api_keys.get("skyscanner"))
                
            return self.services["skyscanner"].search_flights(origin, destination, departure_date, return_date)
        except Exception as e:
            print(f"Skyscanner API error: {e}")
            
            # Fallback options can be implemented here
            return {"error": "Unable to fetch flight data", "details": str(e)}
    
    def get_hotel_data(self, location, check_in, check_out, guests=1):
        """Try multiple hotel APIs in sequence"""
        hotels = []
        
        # Try Booking.com
        try:
            if not self.services.get("booking"):
                from .hotel_service import BookingService
                self.services["booking"] = BookingService(self.api_keys.get("booking"))
                
            hotels = self.services["booking"].search_hotels(location, check_in, check_out, guests)
        except Exception as e:
            print(f"Booking.com API error: {e}")
            
            # Try Expedia as fallback
            try:
                if not self.services.get("expedia"):
                    from .hotel_service import ExpediaService
                    self.services["expedia"] = ExpediaService(self.api_keys.get("expedia"))
                    
                hotels = self.services["expedia"].search_hotels(location, check_in, check_out, guests)
            except Exception as e2:
                print(f"Expedia API error: {e2}")
                return {"error": "Unable to fetch hotel data"}
        
        return hotels
