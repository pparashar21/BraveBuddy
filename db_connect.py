# File: mongo_util.py
from pymongo import MongoClient
from pymongo.errors import ConnectionFailure
import bcrypt

# MongoDB URI with your username and password
uri = "mongodb+srv://BestBuddy:BestBuddy12@cluster0.yzi4n.mongodb.net/Brave?retryWrites=true&w=majority&appName=Cluster0"

# Function to hash a password
def hash_password(plain_password):
    # Generate a salt and hash the password
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(plain_password.encode('utf-8'), salt)
    return hashed_password.decode('utf-8')

# Function to verify a password
def verify_password(plain_password, hashed_password):
    # Check if the provided password matches the hashed password
    if bcrypt.checkpw(plain_password.encode('utf-8'), hashed_password.encode('utf-8')):
        return True  # Passwords match
    else:
        return False  # Passwords do not match



def addUser(first_name, language, gender, password):
    client = MongoClient(uri)
    # Test the connection
    client.admin.command('ping')
    print("Connected to MongoDB Atlas!")
    db = client["Brave"]
    # Specify a collection name
    collection = db["LEIA"]
    hashed_pass = hash_password(password)
    first_name = first_name.upper()
    language = language.upper()
    gender = gender.upper()
    print(hash_password)
    # Insert the user document
    sample_document = {
        "first_name": first_name,
        "language": language,
        "gender": gender,
        "password": hashed_pass
    }
    collection.insert_one(sample_document)
    print("Inserted a sample document.")

    # Retrieve and print a document from the collection
    document = collection.find_one()
    print("Document:", document)

def authenticate_user(first_name, password):
    client = MongoClient(uri)
    client.admin.command('ping')
    print("Connected to MongoDB Atlas!")
    db = client["Brave"]
    # Specify a collection name
    collection = db["LEIA"]
    print("Connected to LEIA")

    # Find the user document by first name
    user = collection.find_one({"first_name": first_name.upper()})
    
    if user is None:
        print("User not found.")
        return False, "User does not exist."  # User does not exist

    print(f"Information for user: {user}")

    # Validate the password
    is_valid = verify_password(password, user['password'])
    
    if is_valid:
        print("Password is valid.")
        return True, "Authentication successful."  # Authentication successful
    
    print("Invalid password.")
    return False, "Invalid password."  # Authentication failed
