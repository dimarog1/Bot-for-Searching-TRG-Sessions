from geopy.geocoders import Nominatim


def get_location(country_code: str, city: str) -> bool:
    try:
        geolocator = Nominatim(user_agent="city_checker")
        location = geolocator.geocode(city.lower(), country_codes=country_code, exactly_one=True)
        print(location)
        return bool(location)
    except Exception:
        return False