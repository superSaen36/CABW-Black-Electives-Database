from flask import Flask, render_template, request, jsonify, redirect
import logging
import sqlite3
import os

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

app = Flask(__name__)

# Database path configuration for Firebase Functions
def get_db_path():
    if os.environ.get('FUNCTIONS_EMULATOR'):
        # Local development
        return os.path.join(os.path.dirname(os.path.abspath(__file__)), "elected_officials.db")
    else:
        # Firebase Functions environment
        return "/tmp/elected_officials.db"

def init_db():
    """Initialize database for Firebase Functions"""
    db_path = get_db_path()
    
    # For Firebase Functions, copy the database to /tmp if it doesn't exist
    if not os.path.exists(db_path) and not os.environ.get('FUNCTIONS_EMULATOR'):
        # Copy database from the functions directory
        source_db = os.path.join(os.path.dirname(os.path.abspath(__file__)), "elected_officials.db")
        if os.path.exists(source_db):
            import shutil
            shutil.copy2(source_db, db_path)
        else:
            logger.warning("Database file not found, creating empty database")
            # Create empty database if source doesn't exist
            conn = sqlite3.connect(db_path)
            conn.close()
    
    return db_path

def get_dropdown_data():
    # Initialize database and connect
    init_db()
    conn = sqlite3.connect(get_db_path())
    cursor = conn.cursor()

    # Query distinct values for each field
    cursor.execute("SELECT DISTINCT Name FROM elected_officials")
    names = [row for row in cursor.fetchall()]

    cursor.execute("SELECT DISTINCT County FROM elected_officials")
    counties = [row for row in cursor.fetchall()]

    cursor.execute("SELECT DISTINCT City FROM elected_officials")
    cities = [row for row in cursor.fetchall()]

    cursor.execute("SELECT DISTINCT Office FROM elected_officials")
    offices = [row for row in cursor.fetchall()]

    cursor.execute("SELECT DISTINCT District FROM elected_officials")
    districts = [row for row in cursor.fetchall()]

    cursor.execute("SELECT DISTINCT Zip_Codes FROM elected_officials")
    zip_codes = [row for row in cursor.fetchall()]

    cursor.execute("SELECT DISTINCT Term_Length FROM elected_officials")
    term_lengths = [row for row in cursor.fetchall()]

    cursor.execute("SELECT DISTINCT Term_Expires FROM elected_officials")
    term_expires = [row for row in cursor.fetchall()]

    cursor.execute("SELECT DISTINCT Term_Limits FROM elected_officials")
    term_limits = [row for row in cursor.fetchall()]

    cursor.execute("SELECT DISTINCT Previous_Elected_Office FROM elected_officials")
    previous_offices = [row for row in cursor.fetchall()]

    cursor.execute("SELECT DISTINCT CABWC_PAC_Endorsed FROM elected_officials")
    cabwc_pac_endorsed = [row for row in cursor.fetchall()]

    cursor.execute("SELECT DISTINCT Political_Party FROM elected_officials")
    political_parties = [row for row in cursor.fetchall()]

    cursor.execute("SELECT DISTINCT Contact FROM elected_officials")
    contacts = [row for row in cursor.fetchall()]

    # Close the connection
    conn.close()

    # Return the data as a dictionary
    return {
        "names": names,
        "counties": counties,
        "cities": cities,
        "offices": offices,
        "districts": districts,
        "zip_codes": zip_codes,
        "term_lengths": term_lengths,
        "term_expires": term_expires,
        "term_limits": term_limits,
        "previous_offices": previous_offices,
        "cabwc_pac_endorsed": cabwc_pac_endorsed,
        "political_parties": political_parties,
        "contacts": contacts
    }

def get_officials_sample(limit=6):
    init_db()
    conn = sqlite3.connect(get_db_path())
    cursor = conn.cursor()
    cursor.execute("SELECT id, Name, County, City, Office, District, Zip_Codes, Term_Length, Term_Expires, Term_Limits, Previous_Elected_Office, CABWC_PAC_Endorsed, Political_Party, Contact FROM elected_officials LIMIT ?", (limit,))
    rows = cursor.fetchall()
    conn.close()
    print(f"rows {rows}")
    return rows

@app.route("/", methods=["POST","GET"])
def search():
    """
        search: name, county, city

        data:
            {
                name:john smith,
                county: alameda,
                city: san francisco,
            }

    """
    try:
        if request.method == "POST":
            data = request.get_json()
            print(f"data {data}")
            # query_data = generate_sql_query(data)
            # logger.info("[+] Query Successful")
            # return jsonify({"success":query_data}), 200
        
        if request.method == "GET":
            dropdown_data = get_dropdown_data()
            officials = get_officials_sample(limit=15)
            return render_template("index.html", dropdown_data=dropdown_data, officials=officials)
    except Exception as e:
        logger.error(f"[!] Failed to query data {e}")
        return jsonify({"result":"Failed to query data"}), 500
    
@app.route("/results", methods=["POST"])
def results():
    # Get the selected filters from the form
    filters = request.form.to_dict()

    # Build the SQL query dynamically based on the selected filters
    query = "SELECT * FROM elected_officials WHERE 1=1"
    params = {}
    for key, value in filters.items():
        if value:  # Only include filters with a value
            query += f" AND {key} = :{key}"
            params[key] = value

    # Initialize database and connect to execute the query
    init_db()
    conn = sqlite3.connect(get_db_path())
    cursor = conn.cursor()
    cursor.execute(query, params)
    results = cursor.fetchall()
    conn.close()

    # Pass the results to the template
    return render_template("results.html", results=results, filters=filters)

@app.route("/wiki/<int:id>")
def wiki_page(id):
    # Initialize database and connect
    init_db()
    conn = sqlite3.connect(get_db_path())
    cursor = conn.cursor()

    # Query the elected official by ID
    cursor.execute("SELECT * FROM elected_officials WHERE id = ?", (id,))
    row = cursor.fetchone()
    conn.close()

    # Map the row to a dictionary
    if row:
        elected_official = {
            "Name": row[1],
            "County": row[2],
            "City": row[3],
            "Office": row[4],
            "District": row[5],
            "Zip_Codes": row[6],
            "Term_Length": row[7],
            "Term_Expires": row[8],
            "Term_Limits": row[9],
            "Previous_Elected_Office": row[10],
            "CABWC_PAC_Endorsed": row[11],
            "Political_Party": row[12],
            "Contact": row[13],
        }
        return render_template("wiki_page.html", elected_official=elected_official)
    else:
        return "Elected official not found", 404
    
# Example Python code to generate the SQL query
def generate_sql_query(data):
    table_name = "elected_officials"
    keys = ", ".join(data.keys())  # Columns to select
    conditions = " AND ".join([f"{key}='{value}'" for key, value in data.items()])  # WHERE clause
    query = f"SELECT {keys} FROM {table_name} WHERE {conditions};"
    return query

@app.route("/login", methods=["GET"])
def login():
    return render_template("login.html")

@app.route("/profile/<int:id>")
def profile(id):
    # Initialize database and connect
    init_db()
    conn = sqlite3.connect(get_db_path())
    cursor = conn.cursor()

    # Query the elected official by ID
    cursor.execute("SELECT * FROM elected_officials WHERE id = ?", (id,))
    row = cursor.fetchone()
    conn.close()

    # Map the row to a dictionary
    if row:
        elected_official = {
            "id": row[0],
            "Name": row[1],
            "County": row[2],
            "City": row[3],
            "Office": row[4],
            "District": row[5],
            "Zip_Codes": row[6],
            "Term_Length": row[7],
            "Term_Expires": row[8],
            "Term_Limits": row[9],
            "Previous_Elected_Office": row[10],
            "CABWC_PAC_Endorsed": row[11],
            "Political_Party": row[12],
            "Contact": row[13],
        }
        return render_template("profile.html", elected_official=elected_official)
    else:
        return "Elected official not found", 404

@app.route("/update_official/<int:official_id>", methods=["GET", "POST"])
def update_official(official_id):
    # Initialize database and connect
    init_db()
    conn = sqlite3.connect(get_db_path())
    cursor = conn.cursor()

    if request.method == "GET":
        # Query the elected official by ID for the form
        cursor.execute("SELECT * FROM elected_officials WHERE id = ?", (official_id,))
        row = cursor.fetchone()
        conn.close()

        if row:
            elected_official = {
                "id": row[0],
                "Name": row[1],
                "County": row[2],
                "City": row[3],
                "Office": row[4],
                "District": row[5],
                "Zip_Codes": row[6],
                "Term_Length": row[7],
                "Term_Expires": row[8],
                "Term_Limits": row[9],
                "Previous_Elected_Office": row[10],
                "CABWC_PAC_Endorsed": row[11],
                "Political_Party": row[12],
                "Contact": row[13],
                "State": row[14] if len(row) > 14 else "CA",
                "Phone": row[15] if len(row) > 15 else "",
                "Email": row[16] if len(row) > 16 else "",
                "Website": row[17] if len(row) > 17 else "",
                "Notes": row[18] if len(row) > 18 else "",
            }
            return render_template("update-info.html", elected_official=elected_official)
        else:
            return "Elected official not found", 404

    elif request.method == "POST":
        try:
            # Get form data
            form_data = request.form.to_dict()
            
            # Prepare the update query
            update_fields = []
            params = []
            
            # Map form fields to database columns
            field_mapping = {
                'name': 'Name',
                'office': 'Office',
                'district': 'District',
                'city': 'City',
                'county': 'County',
                'state': 'State',
                'term_length': 'Term_Length',
                'term_expires': 'Term_Expires',
                'term_limits': 'Term_Limits',
                'party': 'Political_Party',
                'phone': 'Phone',
                'email': 'Email',
                'website': 'Website',
                'previous_office': 'Previous_Elected_Office',
                'contact': 'Contact',
                'notes': 'Notes'
            }
            
            for form_field, db_field in field_mapping.items():
                if form_field in form_data and form_data[form_field]:
                    update_fields.append(f"{db_field} = ?")
                    params.append(form_data[form_field])
            
            if update_fields:
                # Add the official_id to params
                params.append(official_id)
                
                # Build and execute the update query
                query = f"UPDATE elected_officials SET {', '.join(update_fields)} WHERE id = ?"
                cursor.execute(query, params)
                conn.commit()
                
                logger.info(f"Successfully updated elected official with ID {official_id}")
                
                # Redirect to the profile page
                return redirect(f"/profile/{official_id}")
            else:
                logger.warning("No fields to update")
                return redirect(f"/update_official/{official_id}")
                
        except Exception as e:
            logger.error(f"Error updating elected official: {e}")
            conn.rollback()
            return "Error updating elected official", 500
        finally:
            conn.close()


if __name__ == "__main__":
    app.run(debug=True)