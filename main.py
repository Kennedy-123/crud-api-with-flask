from flask import request, jsonify
from config import app
from db.db import db, contacts_collection
from bson.objectid import ObjectId


# get Contacts
@app.route('/contacts', methods=["GET"])
def get_contacts():
    try:
        contacts = list(contacts_collection.find())
        for contact in contacts:
            contact["_id"] = str(contact["_id"])
        return jsonify(contacts)
    except Exception as e:
        return jsonify({f"message: {e}"}), 500


# get a single contactg
@app.route('/get_contact/<user_id>', methods=['GET'])
def get_contact(user_id):
    contact_id = ObjectId(user_id)
    try:
        result = contacts_collection.find_one({"_id": contact_id})
        if not result:
            return jsonify({"message": "Contact not found."}), 404

        # Convert ObjectId to string for JSON serialization
        result["_id"] = str(result["_id"])

        return jsonify(result), 200
    except Exception as e:
        return jsonify({"message": str(e)}), 400


# create a contact
@app.route("/create_contact", methods=['POST'])
def create_contact():
    first_name = request.json.get('firstName')
    last_name = request.json.get('lastName')
    email = request.json.get('email')
    try:
        if not first_name:
            return (
                jsonify({"message": "Enter firstname"}), 400
            )
        elif not last_name:
            return (
                jsonify({"message": "Enter lastname"}), 400
            )
        elif not email:
            return (
                jsonify({"message": "Enter email"}), 400
            )

        contact = request.json
        contacts_collection.insert_one(contact)
        return jsonify({"message": "Contact created"}), 201
    except Exception as e:
        return jsonify({"message": str(e)}), 400


# update contact
@app.route('/update_contact/<user_id>', methods=["PATCH"])
def update_contact(user_id):
    data = request.json
    contact_id = ObjectId(user_id)
    try:
        if not data:
            return jsonify({"error": "No data provided"}), 400

        result = contacts_collection.update_one({"_id": contact_id}, {'$set': data})

        # Check if the contact was found
        if result.matched_count == 0:
            return jsonify({"error": "Contact not found"}), 404

        return jsonify({"message": "Contact Updated"}), 200
    except Exception as e:
        return jsonify({f"message": {e}})


# delete a contact
@app.route('/delete_contact/<user_id>', methods=["DELETE"])
def delete_contact(user_id):
    contact_id = ObjectId(user_id)

    try:
        result = contacts_collection.delete_one({'_id': contact_id})

        if result.deleted_count == 0:
            return jsonify({"message": "Contact does not exist"}), 500

        return jsonify({"message": "Contact deleted"}), 200
    except Exception as e:
        return jsonify({f"message": {e}}), 500


if __name__ == '__main__':
    app.run(debug=True)

