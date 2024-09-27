import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

# Initialize the Firebase Admin SDK
cred = credentials.Certificate('firebase.json')  # Replace with your file path
firebase_admin.initialize_app(cred)

# Get a Firestore client
db = firestore.client()

# --- Working with Collections ---

# Check if a collection exists
def collection_exists(collection_name):
    try:
        db.collection(collection_name).get()
        return True
    except Exception:
        return False

# Create a new collection (if it doesn't exist)
def create_collection(collection_name):
    if not collection_exists(collection_name):
        db.collection(collection_name).document().set({})  # Create an empty document

# --- Adding Data to a Collection ---

def add_data(collection_name, data):
    doc_ref = db.collection(collection_name).document()
    doc_ref.set(data)
    print(f"Data added to document: {doc_ref.id}")

# Example usage
collection_name = 'laundry_items'
create_collection(collection_name)

data = {
    'item_name': 'T-shirt',
    'color': 'Blue',
    'status': 'Dirty'
}

add_data(collection_name, data)
