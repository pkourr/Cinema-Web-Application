# Cinema Paradiso

## Overview

Cinema Paradiso is a web application for managing movie ticket bookings. Users can select movies, choose ticket types, showtimes, and seats. Administrators can manage users and bookings, providing a seamless experience for both customers and admin staff.

## Features

- **User Authentication:** Secure login and registration system.
- **Movie Selection:** Browse and select movies currently showing.
- **Booking Management:** Choose ticket types, showtimes, and seats.
- **Admin Panel:** Manage users and bookings, including viewing, editing, and deleting.
- **Responsive Design:** Mobile-friendly interface for ease of use on various devices.

## Technologies Used

- **Frontend:**
  - HTML5
  - CSS3
  - JavaScript
- **Backend:**
  - Python (Flask)
  - MongoDB Atlas

## Folder Structure

- **`static/`**: Contains static files like CSS and JavaScript.
- **`templates/`**: HTML templates for rendering pages.
- **`app.py`**: Main application file.
- **`config.py`**: Configuration settings for the application.
- **`requirements.txt`**: List of dependencies.

## Installation

### Prerequisites

- Python 3.7+
- MongoDB Atlas account

### Steps

1. Clone the repository:
   ```bash
   git clone https://github.com/pkourr/Cinema-Web-Application.git
   ```
2. Navigate to the project directory:
   ```bash
   cd Cinema-Web-Application
   ```
3. Create a virtual environment and activate it:
   ```bash
   python -m venv venv
   source venv/bin/activate   # On Windows use `venv\Scripts\activate`
   ```
4. Install the required packages:
   ```bash
   pip install -r requirements.txt
   ```
5. Configure MongoDB Atlas:
    - Create a MongoDB Atlas account and set up a cluster.
    - Obtain the connection string and update `config.py` with your MongoDB URI.

6. Run the application:
   ```bash
   flask run
   ```

7. Access the application:
    - Open your web browser and navigate to `http://localhost:5000`.

## Usage

- **User Registration:** Users can sign up by providing necessary details.
- **Movie Selection:** Browse and select movies, choose ticket types, showtimes, and seats.
- **Booking Confirmation:** Users receive a booking code for in-person validation.
- **Admin Panel:** Accessible via `/admin` for user and booking management.

## Database Schema

- **`users` Collection:**
    - `_id`
    - `name`
    - `username`
    - `password`
    - `email`
    - `city`
    - `country`
    - `address`
- **`movie` Collection:**
    - `_id`
    - `name`
- **`projection` Collection:**
    - `_id`
    - `username`
    - `hall`
    - `time`
    - `seat`
    - `movie`

## Admin Instructions

1. **Login as Admin:**
    - Default credentials: `username: admin`, `password: admin`.
2. **Manage Users and Bookings:**
    - View, edit, and delete users and their bookings from the admin panel.

## Contributing

Contributions are welcome! Please follow these steps to contribute:

1. Fork the repository.
2. Create a new branch (`git checkout -b feature-branch`).
3. Commit your changes (`git commit -m 'Add some feature'`).
4. Push to the branch (`git push origin feature-branch`).
5. Open a pull request.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

---

**Note:** Ensure you have the necessary permissions and configurations on your server to avoid any issues during setup.