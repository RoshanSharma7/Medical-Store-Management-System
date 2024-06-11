# Medical Store Management System

## Project Description
This project is a simple Medical Store Management System developed using Python and Tkinter for the graphical user interface (GUI) and SQLite for the database. The system allows users to manage medicines, including adding new medicines, viewing the list of medicines, modifying medicine details, and deleting medicines.

## Features
- Add new medicines
- View all medicines
- Search for specific medicines
- Modify existing medicines
- Delete medicines

## Prerequisites
Make sure you have the following installed on your system:
- Python 3.x
- `pip` (Python package installer)

## Installation
1. Clone the repository:
    ```bash
    git clone https://github.com/RoshanSharma7/medical-store-management-system.git
    cd medical-store-management-system
    ```

2. Create and activate a virtual environment (optional but recommended):
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```

3. Install the required packages:
    ```bash
    pip install -r requirements.txt
    ```

## Running the Application
1. Execute the `main.py` file to start the application:
    ```bash
    python main.py
    ```

2. After running the main.py automatically database files are generated, name of the database is "medical_store_db.db". 

## Usage
- **Add Medicine**: Click the "Add Medicine" button and fill in the details to add a new medicine.
- **View Medicines**: Click the "View Medicines" button to see the list of all medicines.
- **Modify Medicine**: Click the "Modify Medicine" button, search for the medicine, and update its details.
- **Delete Medicine**: Click the "Delete Medicine" button, search for the medicine, and delete it.
- **Make the Bill**: Click the "Make Bill" button to make the bill, after making the bill we print and download the bill
- **Bill History**: Click the "Bill History" button to show the all bill history with the name of customer name, cost and Bill id 

## Requirements
The `requirements.txt` file should include all necessary dependencies. Ensure the file contains the following:

## Contributing
If you wish to contribute to the project, please fork the repository and submit a pull request.

## License
This project is licensed under the MIT License.
