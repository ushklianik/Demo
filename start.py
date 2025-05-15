import csv
from datetime import datetime

def read_and_order_users(file_path, username, password):
    """
    Reads user data from a CSV file, authenticates the user, and returns the users
    ordered by their creation date in ascending order.

    Parameters:
        file_path (str): Path to the CSV file containing user data.
        username (str): Username for authentication.
        password (str): Password for authentication.

    Returns:
        list: A list of dictionaries representing users, ordered by creation date.

    Raises:
        ValueError: If the credentials are invalid.
        FileNotFoundError: If the CSV file does not exist.
        Exception: For other errors, such as malformed CSV or missing data.
    """
    try:
        # Read the CSV file
        with open(file_path, mode='r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            users = list(reader)

        # Authenticate the user
        authenticated = any(
            user['username'] == username and user['password'] == password
            for user in users
        )
        if not authenticated:
            raise ValueError("Invalid credentials")

        # Parse and sort users by creation_date
        for user in users:
            try:
                # Convert creation_date to a datetime object for sorting
                user['creation_date'] = datetime.strptime(user['creation_date'], '%Y-%m-%d')
            except (KeyError, ValueError):
                raise Exception(f"Invalid or missing creation_date for user: {user}")

        # Sort users by creation_date in ascending order
        users.sort(key=lambda x: x['creation_date'])

        # Convert creation_date back to string format for the output
        for user in users:
            user['creation_date'] = user['creation_date'].strftime('%Y-%m-%d')

        return users

    except FileNotFoundError:
        raise FileNotFoundError(f"The file at path '{file_path}' does not exist.")
    except Exception as e:
        raise Exception(f"An error occurred while processing the file: {e}")


# Example usage
if __name__ == "__main__":
    try:
        ordered_users = read_and_order_users(
            file_path="users.csv",
            username="admin",
            password="password123"
        )
        print("Ordered Users:")
        for user in ordered_users:
            print(user)
    except Exception as e:
        print(f"Error: {e}")
