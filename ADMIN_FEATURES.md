# Admin Features Documentation

## Overview
The California Black Power Book application now includes a comprehensive admin system for managing news articles. Admins can approve or disapprove articles that are pulled from RSS feeds before they appear to public users.

## Features

### 1. Admin Collection
- **Location**: Firestore `admins` collection
- **Fields**:
  - `email`: Admin's email address (used for authentication)
  - `user_name`: Display name
  - `phone`: Optional phone number for MFA notifications
  - `mfa_enabled`: Boolean flag for MFA status
  - `created_at`: Timestamp of when admin was added

### 2. Articles Collection
- **Location**: Firestore `articles` collection
- **Fields**:
  - `title`: Article title
  - `link`: URL to the article
  - `published`: Publication date
  - `source`: Source of the article (e.g., "RSS Feed")
  - `approved`: Boolean - whether the article is approved for public viewing
  - `created_at`: Timestamp of when article was added

### 3. Admin Features in News Page
- **For Admins**:
  - See all articles (approved and pending)
  - Visual indicators: Green border for approved, orange for pending
  - Approve/Disapprove buttons with green (✓) and red (✗) icons
  - Approval badge showing article status
  - Buttons are disabled based on current status

- **For Public Users**:
  - See only approved articles
  - No admin controls visible
  - Clean viewing experience

## How to Use

### Adding an Admin
Use the `admin_utils.py` script to add admins:

```bash
# Add a basic admin
python admin_utils.py add admin@example.com "John Doe"

# Add admin with phone number
python admin_utils.py add admin@example.com "John Doe" --phone "+1234567890"

# Add admin with MFA enabled
python admin_utils.py add admin@example.com "John Doe" --phone "+1234567890" --mfa
```

### Listing All Admins
```bash
python admin_utils.py list
```

### Checking Admin Status
```bash
python admin_utils.py check admin@example.com
```

## Workflow

### Article Approval Process
1. **RSS Feed Sync**: When users visit `/news`, RSS feeds are automatically synced to the articles collection
2. **New Articles**: All new articles are marked as `approved=False` by default
3. **Admin Review**: Admins can see all articles and approve/disapprove them
4. **Public View**: Only approved articles (`approved=True`) are visible to non-admin users

### Admin Login
1. Admin logs in through the Firebase authentication system
2. System checks if user's email exists in the `admins` collection
3. If found, `is_admin=True` is added to the session
4. Admin controls become visible on the news page

## API Endpoints

### News Page
- **Route**: `/news`
- **Method**: GET
- **Behavior**:
  - Syncs RSS feeds to articles collection
  - Returns all articles for admins
  - Returns only approved articles for public users

### Approve Article
- **Route**: `/article/approve/<article_id>`
- **Method**: POST
- **Auth**: Admin required
- **Response**: JSON with success status

### Disapprove Article
- **Route**: `/article/disapprove/<article_id>`
- **Method**: POST
- **Auth**: Admin required
- **Response**: JSON with success status

## Code Structure

### Modified Files
1. **fire_store_client.py**:
   - Made collection names parameterized
   - Added admin-related functions
   - Added article management functions

2. **app.py**:
   - Added `admin_required` decorator
   - Updated login to check admin status
   - Added article approval/disapproval routes
   - Added RSS feed sync function

3. **templates/news.html**:
   - Added admin controls (approve/disapprove buttons)
   - Added visual indicators for article status
   - Added JavaScript for AJAX calls to approve/disapprove

4. **templates/home.html**:
   - Enabled the News card (removed "COMING SOON" badge)

### New Files
1. **admin_utils.py**: Utility script for managing admins
2. **ADMIN_FEATURES.md**: This documentation file

## Security Considerations

1. **Admin Decorator**: The `@admin_required` decorator ensures only logged-in admins can access approval endpoints
2. **Session Validation**: Admin status is checked from the session during login
3. **Firestore Rules**: Ensure Firestore security rules restrict write access to the `admins` collection
4. **MFA Ready**: The admin schema includes fields for MFA implementation

## Future Enhancements

1. **Email Notifications**: Send email notifications to admins when new articles arrive
2. **MFA Implementation**: Add multi-factor authentication for admin logins
3. **Article Analytics**: Track which articles are most viewed
4. **Bulk Actions**: Add ability to approve/disapprove multiple articles at once
5. **Article Categories**: Add categorization for better organization
6. **Search/Filter**: Add search and filter capabilities for admins

## Troubleshooting

### Admin Can't See Admin Controls
- Verify admin is in the `admins` collection
- Check that email matches exactly
- Log out and log back in to refresh session

### Articles Not Appearing
- Check Firestore connection
- Verify RSS feeds are working (check console logs)
- Ensure articles collection has proper permissions

### Approval Not Working
- Check browser console for JavaScript errors
- Verify admin has proper session token
- Check Flask logs for error messages
