from flask import Flask, render_template, request, jsonify, redirect, session, flash
import logging
import os
from functools import wraps
from fire_store_client import (
    db, get_electeds_data, verify_id_token, is_admin,
    get_all_articles, get_approved_articles, add_article,
    approve_article, disapprove_article,
    add_pending_update, get_all_pending_updates, get_unapproved_pending_updates,
    approve_pending_update, disapprove_pending_update
)
from rss_feed_reader import get_feed_data
from firebase_auth_client import send_password_reset_email, send_email_login

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', 'your-secret-key-here')

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user' not in session:
            return redirect('/login')
        return f(*args, **kwargs)
    return decorated_function

def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user' not in session:
            return redirect('/login')
        if not session['user'].get('is_admin', False):
            return jsonify({"error": "Admin access required"}), 403
        return f(*args, **kwargs)
    return decorated_function

def get_dropdown_data():
    """Get dropdown data from Firestore"""
    try:
        # Get all documents from the electeds-db collection
        docs = db.collection("electeds-db").get()
        
        # Extract unique values for each field
        names = set()
        counties = set()
        cities = set()
        offices = set()
        districts = set()
        zip_codes = set()
        term_lengths = set()
        term_expires = set()
        term_limits = set()
        previous_offices = set()
        cabwc_pac_endorsed = set()
        political_parties = set()
        
        for doc in docs:
            data = doc.to_dict()
            if data.get('Name'):
                names.add(data['Name'])
            if data.get('County'):
                counties.add(data['County'])
            if data.get('City'):
                cities.add(data['City'])
            if data.get('Office'):
                offices.add(data['Office'])
            if data.get('District'):
                districts.add(data['District'])
            if data.get('Zip Codes'):
                zip_codes.add(data['Zip Codes'])
            if data.get('Term Length'):
                term_lengths.add(data['Term Length'])
            if data.get('Term Expires'):
                term_expires.add(data['Term Expires'])
            if data.get('Term Limits'):
                term_limits.add(data['Term Limits'])
            if data.get('Previous_Elected_Office'):
                previous_offices.add(data['Previous_Elected_Office'])
            if data.get('CABWC_PAC_Endorsed'):
                cabwc_pac_endorsed.add(data['CABWC_PAC_Endorsed'])
            if data.get('Political_Party'):
                political_parties.add(data['Political_Party'])
        
        # Convert sets to lists for template rendering
        return {
            "names": sorted(list(names)),
            "counties": sorted(list(counties)),
            "cities": sorted(list(cities)),
            "offices": sorted(list(offices)),
            "districts": sorted(list(districts)),
            "zip_codes": sorted(list(zip_codes)),
            "term_lengths": sorted(list(term_lengths)),
            "term_expires": sorted(list(term_expires)),
            "term_limits": sorted(list(term_limits)),
            "previous_offices": sorted(list(previous_offices)),
            "cabwc_pac_endorsed": sorted(list(cabwc_pac_endorsed)),
            "political_parties": sorted(list(political_parties))
        }
    except Exception as e:
        logger.error(f"Error getting dropdown data: {e}")
        return {}

def get_county_coordinates():
    """Get California county coordinates"""
    return {
        'Alameda': {'lat': 37.6017, 'lng': -121.7195},
        'Contra Costa': {'lat': 37.9161, 'lng': -121.9496},
        'Fresno': {'lat': 36.7378, 'lng': -119.7871},
        'Los Angeles': {'lat': 34.0522, 'lng': -118.2437},
        'Marin': {'lat': 38.0834, 'lng': -122.7633},
        'Monterey': {'lat': 36.2677, 'lng': -121.6056},
        'Orange': {'lat': 33.7175, 'lng': -117.8311},
        'Riverside': {'lat': 33.7208, 'lng': -116.2023},
        'Sacramento': {'lat': 38.4747, 'lng': -121.3542},
        'San Bernardino': {'lat': 34.9592, 'lng': -116.4194},
        'San Diego': {'lat': 32.8312, 'lng': -117.1225},
        'San Francisco': {'lat': 37.7749, 'lng': -122.4194},
        'San Joaquin': {'lat': 37.9357, 'lng': -121.2907},
        'San Jose': {'lat': 37.3382, 'lng': -121.8863},
        'San Mateo': {'lat': 37.5630, 'lng': -122.3255},
        'Solano': {'lat': 38.4404, 'lng': -121.8735},
        'Sonoma': {'lat': 38.5816, 'lng': -122.8047},
        'Tulare': {'lat': 36.2077, 'lng': -118.8897},
        'Ventura': {'lat': 34.2804, 'lng': -119.2945}
    }

def add_coordinates_to_official(data):
    """Add coordinates to official data based on county"""
    county_coords = get_county_coordinates()
    county = data.get('County', '').strip()
    if county in county_coords:
        data['coordinates'] = county_coords[county]
    elif county == 'Alameda ':  # Handle trailing space
        data['coordinates'] = county_coords['Alameda']
    elif county == 'Los Angeles ':  # Handle trailing space
        data['coordinates'] = county_coords['Los Angeles']
    else:
        data['coordinates'] = {'lat': 34.0522, 'lng': -118.2437}  # Default to LA
    return data

def get_officials_sample(limit=15):
    """Get sample officials from Firestore sorted by name"""
    try:
        docs = db.collection("electeds-db").order_by("Name").limit(limit).get()
        officials = []
        
        for doc in docs:
            data = doc.to_dict()
            data['id'] = doc.id  # Add document ID
            data = add_coordinates_to_official(data)
            officials.append(data)
        return officials
    except Exception as e:
        logger.error(f"Error getting officials sample: {e}")
        return []

def get_all_officials():
    """Get all officials from Firestore sorted by name"""
    try:
        docs = db.collection("electeds-db").order_by("Name").get()
        officials = []
        
        for doc in docs:
            data = doc.to_dict()
            data['id'] = doc.id  # Add document ID
            data = add_coordinates_to_official(data)
            officials.append(data)
        return officials
    except Exception as e:
        logger.error(f"Error getting all officials: {e}")
        return []

def search_all_officials(search_query):
    """Search all officials in the database"""
    try:
        # Get all documents from the collection
        docs = db.collection("electeds-db").get()
        matching_officials = []
        
        for doc in docs:
            data = doc.to_dict()
            data['id'] = doc.id  # Add document ID
            
            # Search in multiple fields (case insensitive)
            searchable_fields = [
                data.get('Name', ''),
                data.get('City', ''),
                data.get('Office', ''),
                data.get('County', ''),
                data.get('District', ''),
                data.get('Political_Party', ''),
                data.get('Zip Codes', ''),
                data.get('Term Length', ''),
                data.get('Term Expires', ''),
                data.get('Term Limits', ''),
                data.get('Previous Elected Office', ''),
                data.get('CABWC PAC Endorsed', '')
            ]
            
            # Check if search query matches any field
            if any(search_query in field.lower() for field in searchable_fields if field):
                data = add_coordinates_to_official(data)
                matching_officials.append(data)
        
        # Sort results by name
        matching_officials.sort(key=lambda x: x.get('Name', ''))
        return matching_officials
        
    except Exception as e:
        logger.error(f"Error searching officials: {e}")
        return []

@app.route("/")
def home():
    """Home page with navigation cards"""
    # Check if user is admin
    user_is_admin = False
    if 'user' in session:
        user_is_admin = session['user'].get('is_admin', False)

    return render_template("home.html", is_admin=user_is_admin)

@app.route("/location", methods=["POST","GET"])
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
        if request.method == "GET":
            try:
                dropdown_data = get_dropdown_data()
                search_query = request.args.get('search', '').strip().lower()

                if search_query:
                    # Search the entire database
                    officials = search_all_officials(search_query)
                else:
                    # Show all officials
                    officials = get_all_officials()

                return render_template("index.html", dropdown_data=dropdown_data, officials=officials)
            except Exception as get_error:
                logger.error(f"Error in GET request: {get_error}")
                return f"Database error: {get_error}", 500
    except Exception as e:
        logger.error(f"[!] Failed to query data {e}")
        return jsonify({"result":"Failed to query data"}), 500
    
@app.route("/results", methods=["POST"])
def results():
    # Get the selected filters from the form
    filters = request.form.to_dict()
    print(f"filters {filters}")
    try:
        # Build Firestore query based on filters
        query = db.collection("electeds-db")
        
        # Apply filters
        for key, value in filters.items():
            if value:  # Only include filters with a value
                query = query.where(key, "==", value)
        
        # Execute query
        docs = query.get()
        results = []
        for doc in docs:
            data = doc.to_dict()
            data['id'] = doc.id  # Add document ID
            results.append(data)
        
        # Pass the results to the template
        return render_template("results.html", results=results, filters=filters)
    except Exception as e:
        logger.error(f"Error querying results: {e}")
        return "Error querying results", 500

@app.route("/wiki/<id>")
def wiki_page(id):
    try:
        # Query the elected official by document ID
        doc = db.collection("electeds-db").document(id).get()
        
        if doc.exists:
            elected_official = doc.to_dict()
            elected_official['id'] = doc.id  # Add document ID
            return render_template("wiki_page.html", elected_official=elected_official)
        else:
            return "Elected official not found", 404
    except Exception as e:
        logger.error(f"Error getting wiki page: {e}")
        return "Error retrieving elected official", 500

@app.route("/profile/<id>")
def profile(id):
    try:
        # Query the elected official by document ID
        doc = db.collection("electeds-db").document(id).get()
        
        if doc.exists:
            elected_official = doc.to_dict()
            elected_official['id'] = doc.id  # Add document ID
            return render_template("profile.html", elected_official=elected_official)
        else:
            return "Elected official not found", 404
    except Exception as e:
        logger.error(f"Error getting profile: {e}")
        return "Error retrieving elected official", 500

@app.route("/update_official/<id>", methods=["GET", "POST"])
@login_required
def update_official(id):
    try:
        if request.method == "GET":
            # Query the elected official by document ID for the form
            doc = db.collection("electeds-db").document(id).get()
            
            if doc.exists:
                elected_official = doc.to_dict()
                elected_official['id'] = doc.id  # Add document ID
                return render_template("update-info.html", elected_official=elected_official)
            else:
                return "Elected official not found", 404

        elif request.method == "POST":
            # Get form data
            form_data = request.form.to_dict()

            # Map form fields to Firestore fields
            field_mapping = {
                'name': 'Name',
                'office': 'Office',
                'district': 'District',
                'city': 'City',
                'county': 'County',
                'state': 'State',
                'term_length': 'Term Length',
                'term_expires': 'Term Expires',
                'term_limits': 'Term Limits',
                'party': 'Political_Party',
                'phone': 'Phone',
                'email': 'Email',
                'website': 'Website',
                'previous_office': 'Previous_Elected_Office',
                'contact': 'Contact',
                'notes': 'Notes'
            }

            # Prepare update data
            update_data = {}
            for form_field, firestore_field in field_mapping.items():
                if form_field in form_data and form_data[form_field]:
                    update_data[firestore_field] = form_data[form_field]

            if update_data:
                # Get current official data for the name
                doc = db.collection("electeds-db").document(id).get()
                official_name = doc.to_dict().get('Name', 'Unknown') if doc.exists else 'Unknown'

                # Get user info from session
                user_name = session['user'].get('name', 'Unknown User')
                user_email = session['user'].get('email', 'unknown@example.com')

                # Create a pending update instead of directly updating
                add_pending_update(
                    official_id=id,
                    official_name=official_name,
                    update_data=update_data,
                    submitted_by=user_name,
                    submitted_by_email=user_email
                )

                logger.info(f"Created pending update for elected official with ID {id}")
                flash("Your update has been submitted for admin approval.", "success")

                # Redirect to the profile page
                return redirect(f"/profile/{id}")
            else:
                logger.warning("No fields to update")
                return redirect(f"/update_official/{id}")
                
    except Exception as e:
        logger.error(f"Error updating elected official: {e}")
        return "Error updating elected official", 500

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template("login.html")

    if request.method == "POST":
        try:
            data = request.get_json()
            id_token = data.get('idToken')

            if not id_token:
                return jsonify({"error": "No token provided"}), 400

            decoded_token = verify_id_token(id_token)
            if decoded_token:
                user_email = decoded_token.get('email')
                user_is_admin = is_admin(user_email)

                session['user'] = {
                    'uid': decoded_token['uid'],
                    'email': user_email,
                    'name': decoded_token.get('name'),
                    'is_admin': user_is_admin
                }

                logger.info(f"User {user_email} logged in. Admin: {user_is_admin}")
                return jsonify({"success": True, "is_admin": user_is_admin}), 200
            else:
                return jsonify({"error": "Invalid token"}), 401

        except Exception as e:
            logger.error(f"Login error: {e}")
            return jsonify({"error": "Login failed"}), 500

@app.route("/logout", methods=["POST"])
def logout():
    session.pop('user', None)
    return jsonify({"success": True}), 200

@app.route("/forgot-password", methods=["POST"])
def forgot_password():
    """Send password reset email"""
    try:
        data = request.get_json()
        email = data.get('email')

        if not email:
            return jsonify({"error": "Email is required"}), 400

        link = send_password_reset_email(email)
        if link:
            logger.info(f"Password reset email sent to {email}")
            return jsonify({
                "success": True,
                "message": "Password reset link sent to your email"
            }), 200
        else:
            return jsonify({"error": "Failed to send password reset email"}), 500

    except Exception as e:
        logger.error(f"Forgot password error: {e}")
        return jsonify({"error": "Failed to process request"}), 500

@app.route("/request-login-link", methods=["POST"])
def request_login_link():
    """Send passwordless login link"""
    try:
        data = request.get_json()
        email = data.get('email')

        if not email:
            return jsonify({"error": "Email is required"}), 400

        link = send_email_login(email)
        if link:
            logger.info(f"Login link sent to {email}")
            return jsonify({
                "success": True,
                "message": "Sign-in link sent to your email"
            }), 200
        else:
            return jsonify({"error": "Failed to send login link"}), 500

    except Exception as e:
        logger.error(f"Request login link error: {e}")
        return jsonify({"error": "Failed to process request"}), 500

@app.route("/signup", methods=["GET", "POST"])
def signup():
    """Handle user signup - display form and process registration"""
    if request.method == "GET":
        return render_template("signup.html")

    if request.method == "POST":
        try:
            data = request.get_json()
            email = data.get('email')
            first_name = data.get('firstName')
            last_name = data.get('lastName')
            city = data.get('city')
            county = data.get('county')
            zip_code = data.get('zipCode')

            if not email:
                return jsonify({"error": "Email is required"}), 400

            # Create Firebase user account
            try:
                user = auth.create_user(
                    email=email,
                    email_verified=False
                )

                # Store user data in Firestore
                user_data = {
                    'email': email,
                    'firstName': first_name or '',
                    'lastName': last_name or '',
                    'city': city or '',
                    'county': county or '',
                    'zipCode': zip_code or '',
                    'created_at': firestore.SERVER_TIMESTAMP,
                    'is_admin': False,
                    'is_elected': False
                }

                # Add user to users collection
                db.collection('users').document(user.uid).set(user_data)

                # Send verification email
                link = send_password_reset_email(email)

                logger.info(f"New user signed up: {email}")
                return jsonify({
                    "success": True,
                    "message": "Account created successfully. Please check your email to set your password."
                }), 200

            except auth.EmailAlreadyExistsError:
                return jsonify({"error": "An account with this email already exists"}), 400
            except Exception as e:
                logger.error(f"Firebase user creation error: {e}")
                return jsonify({"error": "Failed to create account"}), 500

        except Exception as e:
            logger.error(f"Signup error: {e}")
            return jsonify({"error": "Failed to process signup"}), 500

def sync_rss_to_articles():
    """Sync RSS feed data to articles collection"""
    try:
        # Get RSS feed data
        rss_entries = get_feed_data()

        # Get existing articles to avoid duplicates
        existing_articles = get_all_articles()
        existing_links = {article['link'] for article in existing_articles}

        # Add new articles
        new_count = 0
        for entry in rss_entries:
            if entry['link'] not in existing_links:
                add_article(
                    title=entry['title'],
                    link=entry['link'],
                    published=entry['published'],
                    source=entry.get('source', 'RSS Feed'),
                    approved=False,  # New articles need admin approval
                    image_url=entry.get('image_url')
                )
                new_count += 1

        logger.info(f"Synced {new_count} new articles from RSS feeds")
        return new_count
    except Exception as e:
        logger.error(f"Error syncing RSS feeds: {e}")
        return 0

@app.route("/news")
def news():
    """News page displaying articles - admins see all, users see approved only"""
    try:
        # Sync RSS feeds to articles collection (commented out for faster loading)
        # sync_rss_to_articles()

        # Check if user is admin
        user_is_admin = False
        if 'user' in session:
            user_is_admin = session['user'].get('is_admin', False)

        # Get articles based on admin status
        if user_is_admin:
            all_articles = get_all_articles()
            logger.info(f"Admin view: Retrieved {len(all_articles)} total articles")
        else:
            all_articles = get_approved_articles()
            logger.info(f"Public view: Retrieved {len(all_articles)} approved articles")

        # Separate featured article (first one) from recent articles (next two)
        featured_article = all_articles[0] if all_articles else None
        news_entries = all_articles[1:3] if len(all_articles) > 1 else []  # Get next 2 articles only

        # Debug logging
        logger.info(f"Featured article: {featured_article.get('title') if featured_article else 'None'}")
        logger.info(f"Recent articles count: {len(news_entries)}")

        # Get all politician names for filtering
        all_officials_docs = get_electeds_data()
        all_officials = [doc.to_dict() for doc in all_officials_docs]
        politician_names = sorted(set(official.get('Name', '') for official in all_officials if official.get('Name')))

        return render_template("news.html", news_entries=news_entries, featured_article=featured_article, is_admin=user_is_admin, politician_names=politician_names)
    except Exception as e:
        logger.error(f"Error fetching news: {e}")
        import traceback
        traceback.print_exc()
        return render_template("news.html", news_entries=[], featured_article=None, is_admin=False, politician_names=[])

@app.route("/article/approve/<article_id>", methods=["POST"])
@admin_required
def approve_article_route(article_id):
    """Approve an article (admin only)"""
    try:
        success = approve_article(article_id)
        if success:
            logger.info(f"Article {article_id} approved by {session['user']['email']}")
            return jsonify({"success": True, "message": "Article approved"}), 200
        else:
            return jsonify({"success": False, "message": "Failed to approve article"}), 500
    except Exception as e:
        logger.error(f"Error approving article: {e}")
        return jsonify({"success": False, "message": str(e)}), 500

@app.route("/article/disapprove/<article_id>", methods=["POST"])
@admin_required
def disapprove_article_route(article_id):
    """Disapprove an article (admin only)"""
    try:
        success = disapprove_article(article_id)
        if success:
            logger.info(f"Article {article_id} disapproved by {session['user']['email']}")
            return jsonify({"success": True, "message": "Article disapproved"}), 200
        else:
            return jsonify({"success": False, "message": "Failed to disapprove article"}), 500
    except Exception as e:
        logger.error(f"Error disapproving article: {e}")
        return jsonify({"success": False, "message": str(e)}), 500

@app.route("/admin/approvals")
@admin_required
def admin_approvals():
    """Admin page to review both pending politician updates and news articles"""
    try:
        # Get all pending updates (including both approved and unapproved for history)
        pending_updates = get_all_pending_updates()
        logger.info(f"Admin view: Retrieved {len(pending_updates)} pending politician updates")

        # Get all articles (both approved and unapproved for review)
        articles = get_all_articles()
        logger.info(f"Admin view: Retrieved {len(articles)} total articles")

        return render_template("admin-approvals.html",
                             pending_updates=pending_updates,
                             articles=articles)
    except Exception as e:
        logger.error(f"Error fetching approvals data: {e}")
        return render_template("admin-approvals.html", pending_updates=[], articles=[])

@app.route("/pending_update/approve/<update_id>", methods=["POST"])
@admin_required
def approve_update_route(update_id):
    """Approve a pending update and apply it to the elected official (admin only)"""
    try:
        success = approve_pending_update(update_id)
        if success:
            logger.info(f"Pending update {update_id} approved by {session['user']['email']}")
            return jsonify({"success": True, "message": "Update approved and applied"}), 200
        else:
            return jsonify({"success": False, "message": "Failed to approve update"}), 500
    except Exception as e:
        logger.error(f"Error approving pending update: {e}")
        return jsonify({"success": False, "message": str(e)}), 500

@app.route("/pending_update/disapprove/<update_id>", methods=["POST"])
@admin_required
def disapprove_update_route(update_id):
    """Disapprove a pending update (admin only)"""
    try:
        success = disapprove_pending_update(update_id)
        if success:
            logger.info(f"Pending update {update_id} disapproved by {session['user']['email']}")
            return jsonify({"success": True, "message": "Update disapproved"}), 200
        else:
            return jsonify({"success": False, "message": "Failed to disapprove update"}), 500
    except Exception as e:
        logger.error(f"Error disapproving pending update: {e}")
        return jsonify({"success": False, "message": str(e)}), 500

if __name__ == "__main__":
    # Get port from environment variable (for local development and Cloud Run)
    port = int(os.environ.get('PORT', 8080))
    # Bind to 0.0.0.0 to accept external traffic (required for Cloud Run)
    app.run(host='0.0.0.0', port=port, debug=True)