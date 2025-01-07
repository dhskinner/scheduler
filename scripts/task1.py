# Brisbane Weather

import requests
from pymongo import MongoClient

# MongoDB Atlas connection URI
# Replace <username>, <password>, and <cluster-address> with your MongoDB Atlas credentials
# MONGO_URI = "mongodb+srv://<username>:<password>@<cluster-address>.mongodb.net/?retryWrites=true&w=majority"
MONGO_URI = "mongodb://100.69.147.87:27017/"

# Function to fetch weather data from the URL
def fetch_weather_data(url: str):
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise an exception for HTTP errors
        weather_data = response.json()
        print("Weather data fetched successfully.")
        return weather_data
    except requests.exceptions.RequestException as e:
        print(f"An error occurred while fetching weather data: {e}")
        return None

# Function to store data in MongoDB
def store_data_in_mongodb(data: dict, database_name: str, collection_name: str):
    try:
        # Connect to MongoDB Atlas
        client = MongoClient(MONGO_URI)
        
        # Access the database (creates it if it doesn't exist)
        db = client[database_name]
        
        # Access the collection (creates it if it doesn't exist)
        collection = db[collection_name]
        
        # Insert the document
        result = collection.insert_one(data)
        print(f"Weather data inserted with ID: {result.inserted_id}")
        
    except Exception as e:
        print(f"An error occurred while storing data in MongoDB: {e}")
    finally:
        # Close the connection
        client.close()

# Main function
if __name__ == "__main__":
    # Weather data URL
    weather_url = "https://reg.bom.gov.au/fwo/IDQ60901/IDQ60901.94576.json"
    
    # Fetch weather data
    weather_data = fetch_weather_data(weather_url)
    
    # Store weather data in MongoDB
    if weather_data:
        store_data_in_mongodb(weather_data, database_name="scheduler", collection_name="task1")
