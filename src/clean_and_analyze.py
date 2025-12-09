# -------------------------------------------------------------
# Profitable App Profiles for the App Store and Google Play
#
# This script:
#   1. Loads the Apple Store and Google Play datasets (CSV files)
#   2. Cleans the Google Play data by:
#        - Removing wrong rows (inconsistent column length)
#        - Detecting and removing duplicate app entries
#          (keeping only the row with the highest number of reviews)
#   3. Filters to English, free apps
#   4. Computes average ratings (Apple) and installs (Google Play)
#      per genre/category.
# -------------------------------------------------------------

from csv import reader


# -------------------------------------------------------------
# Helper function: open a CSV and return it as a list of lists
# -------------------------------------------------------------
def opencsv(file_location):
    """
    Opens a CSV file and returns its content as a list of lists.

    Parameters:
        file_location (str): Path to the CSV file.

    Returns:
        list[list[str]]: The dataset, where each inner list is a row.
    """
    with open(file_location, encoding='utf8') as data:
        dataset = list(reader(data))
    return dataset


# -------------------------------------------------------------
# Helper function: explore a slice of the dataset
# -------------------------------------------------------------
def explore_data(dataset, start, end, rows_and_columns=False):
    """
    Prints rows from 'start' to 'end' (non-inclusive) from a dataset.
    Optionally prints the number of rows and columns.

    Parameters:
        dataset (list[list]): The dataset to explore.
        start (int): Start index (inclusive).
        end (int): End index (exclusive).
        rows_and_columns (bool): If True, prints dataset shape.
    """
    dataset_slice = dataset[start:end]
    for row in dataset_slice:
        print(row)
        print('\n')  # adds a blank line after each row for readability

    if rows_and_columns:
        print('Number of rows:', len(dataset))
        print('Number of columns:', len(dataset[0]))


# -------------------------------------------------------------
# Helper function: separate header row from data rows
# -------------------------------------------------------------
def separatefromheader(dataset, hdataset=None):
    """
    Separates the header row from the rest of the dataset.

    Parameters:
        dataset (list[list]): The full dataset including the header.
        hdataset (list): Placeholder variable to store the header.

    Returns:
        tuple:
            dataset (list[list]): Data rows only (header removed).
            hdataset (list): The header row.
    """
    hdataset = dataset[0]   # first row is the header
    dataset = dataset[1:]   # the rest is the actual data
    return dataset, hdataset


# -------------------------------------------------------------
# Step 1: Remove wrong data (rows with incorrect number of columns)
# -------------------------------------------------------------
def delwrongdata(dataset):
    """
    Detects and removes any row that doesn't have the same number
    of columns as the first data row. This helps us remove corrupted
    rows (like the known bad row in the Google Play dataset).

    Parameters:
        dataset (list[list]): Dataset without header.

    Returns:
        list[list]: Cleaned dataset with consistent row length.
    """
    ref_len = len(dataset[0])
    wrong_indices = []

    # Find indices of rows with a different length than the reference.
    for i, row in enumerate(dataset):
        if len(row) != ref_len:
            print("Wrong row at index:", i)
            wrong_indices.append(i)

    # Delete from the end so that indices don't shift while deleting.
    for i in reversed(wrong_indices):
        del dataset[i]

    return dataset


# -------------------------------------------------------------
# Step 2: Detect duplicate apps in the Google Play dataset
# -------------------------------------------------------------
def finduplicate(dataset):
    """
    Detects duplicate app entries based on the app name (column 0).

    It:
      - prints example rows for a known duplicated app ('Instagram')
      - counts how many duplicate app names exist

    Parameters:
        dataset (list[list]): Google Play dataset without header.
    """
    unique_app = []      # app names we see for the first time
    duplicate_app = []   # app names that appear more than once

    for app in dataset:
        appname = app[0]

        # Print example duplicated rows for Instagram to illustrate the issue.
        if appname == 'Instagram':
            print("example of duplicates rows:", app)

        # If we've already seen this app name, it's a duplicate.
        if appname in unique_app:
            duplicate_app.append(appname)
        else:
            unique_app.append(appname)

    print("number of duplicate app entries:", len(duplicate_app))
    # Show a sample of duplicate app names as evidence.
    print("example of duplicate app names:", duplicate_app[0:15])


# -------------------------------------------------------------
# Step 3: Build a dictionary of max reviews per app (reviews_max)
# -------------------------------------------------------------
def createdicodup(dataset):
    """
    Creates a dictionary mapping each app name to its maximum number
    of reviews.

    We use this to choose the "best" row for each app when duplicates
    exist: the row with the highest number of reviews is assumed to be
    the most recent and reliable one.

    Parameters:
        dataset (list[list]): Google Play dataset without header.

    Returns:
        dict[str, float]: { app_name: max_number_of_reviews }
    """
    reviews_max = {}

    for app in dataset:
        name = app[0]              # app name
        n_reviews = float(app[3])  # number of reviews (as float)

        # If the app is already in the dictionary and this row has more reviews,
        # we update the stored max.
        if name in reviews_max and reviews_max[name] < n_reviews:
            reviews_max[name] = n_reviews
        # If it's not yet in the dictionary, we add it.
        elif name not in reviews_max:
            reviews_max[name] = n_reviews

    return reviews_max


# -------------------------------------------------------------
# Step 4: Remove duplicate app rows using reviews_max
# -------------------------------------------------------------
def deldupdata(dataset, reviews_max):
    """
    Uses the reviews_max dictionary to remove duplicate app rows.

    For each app, we keep only the row where the number of reviews
    matches the maximum for that app (from reviews_max).

    Parameters:
        dataset (list[list]): Google Play dataset without header.
        reviews_max (dict[str, float]): Max reviews per app name.

    Returns:
        list[list]: android_clean, the cleaned Google Play dataset
                    with one row per app and no duplicates.
    """
    android_clean = []   # final cleaned dataset
    already_added = []   # app names we've already added to android_clean

    for app in dataset:
        name = app[0]
        n_reviews = float(app[3])

        if (name not in already_added) and (reviews_max[name] == n_reviews):
            android_clean.append(app)
            already_added.append(name)

    return android_clean


# -------------------------------------------------------------
# Step 5: Function to detect whether a string is "English enough"
# -------------------------------------------------------------
def is_english(name):
    """
    Returns True if the app name is considered English, False otherwise.

    Logic:
      - We count how many characters have an ASCII code > 127.
      - If there are more than 3 such characters, we consider the name
        as non-English and return False.
      - This allows names with emojis or a few special characters
        (e.g., 'Docs To Go™ Free Office Suite', 'Instachat 😜') to still
        be treated as English.
    """
    non_ascii = 0

    for character in name:
        if ord(character) > 127:
            non_ascii += 1
        if non_ascii > 3:
            return False  # too many "non-English-looking" characters

    return True  # 3 or fewer non-ASCII chars → considered English


# -------------------------------------------------------------
# Step 7: Calculate Frequency to determine the most common genre
# -------------------------------------------------------------
def freq_table(database, index):
    table = {}
    table_percentages = {}
    total = 0
    for row in database:
        total += 1
        genre = row[index]
        if genre in table:
            table[genre] += 1
        else:
            table[genre] = 1

    for key in table:
        table_percentages[key] = (table[key] / total) * 100
    return table_percentages


def display_table(dataset, index):
    table = freq_table(dataset, index)
    table_display = []
    for key in table:
        key_val_as_tuple = (table[key], key)
        table_display.append(key_val_as_tuple)

    table_sorted = sorted(table_display, reverse=True)
    for entry in table_sorted:
        print(entry[1], ':', entry[0])



def load_and_clean_datasets(apple_path, google_path):
    """Load CSVs, separate headers, and clean wrong rows in Google Play."""
    # Load raw datasets
    apple_data = opencsv(apple_path)
    google_data = opencsv(google_path)

    # Separate headers
    google_data, header_google_data = separatefromheader(google_data)
    apple_data, header_apple_data = separatefromheader(apple_data)

    # Clean wrong data in Google Play
    google_data = delwrongdata(google_data)

    return apple_data, google_data, header_apple_data, header_google_data


def clean_google_duplicates(google_data):
    """Inspect and remove duplicates from Google Play dataset."""
    # For exploration (can be commented out later if too noisy)
    finduplicate(google_data)

    reviews_max = createdicodup(google_data)
    print("Number of unique app names in reviews_max:", len(reviews_max))

    google_data_clean = deldupdata(google_data, reviews_max)
    return google_data_clean


def filter_english_and_free(google_data, apple_data):
    """Filter both datasets to English-only, then free-only apps."""
    android_english = []
    for app in google_data:
        name = app[0]  # App name column in Google Play
        if is_english(name):
            android_english.append(app)

    ios_english = []
    for app in apple_data:
        name = app[1]  # App name column in Apple Store
        if is_english(name):
            ios_english.append(app)

    # Replace with English-only datasets
    google_data = android_english
    apple_data = ios_english

    # Filter free apps
    android_free = []
    for app in google_data:
        price = app[7]   # Google Play "Price" column as string
        if price == '0':  # free apps have price '0'
            android_free.append(app)

    apple_free = []
    for app in apple_data:
        price = app[4]   # Apple Store "price" column as string
        if price == '0.0' or price == '0':
            apple_free.append(app)

    print("Number of rows in cleaned (English) Google Play dataset:", len(google_data))
    print("Number of rows in cleaned (Free) Google Play dataset:", len(android_free))
    print("Number of rows in cleaned (English) Apple dataset:", len(apple_data))
    print("Number of rows in cleaned (Free) Apple dataset:", len(apple_free))

    return android_free, apple_free


def compute_apple_genre_avg_ratings(apple_data):
    """
    Computes average number of ratings per genre for the Apple Store
    and returns a dict {genre: avg_num_ratings}.
    """
    genre_freq = freq_table(apple_data, 11)
    results = {}
    for genre in genre_freq:
        total = 0
        len_genre = 0
        for row in apple_data:
            genre_app = row[11]
            if genre_app == genre:
                rating = float(row[5])
                total += rating
                len_genre += 1
        av_num_rating = total / len_genre
        results[genre] = av_num_rating
    return results


def compute_google_category_avg_installs(google_data):
    """
    Computes average number of installs per category for Google Play
    and returns a dict {category: avg_installs}.
    """
    category_freq = freq_table(google_data, 1)
    results = {}
    for category in category_freq:
        total = 0
        len_category = 0
        for row in google_data:
            category_app = row[1]
            if category_app == category:
                installs = row[5]
                installs = installs.replace('+', '').replace(',', '')
                installs = float(installs)
                total += installs
                len_category += 1
        av_installs = total / len_category
        results[category] = av_installs
    return results


# -------------------------------------------------------------
# Main entry point
# -------------------------------------------------------------
def main():
    # 1. Load and clean basic structure
    apple_data, google_data, header_apple_data, header_google_data = load_and_clean_datasets(
        'data/AppleStore.csv',
        'data/googleplaystore.csv'
    )

    # Optional: quick peek at data
    print("Google Play header:")
    print(header_google_data)
    explore_data(google_data, 1, 2)

    print("Apple Store header:")
    print(header_apple_data)
    explore_data(apple_data, 1, 2)

    # 2. Clean duplicates in Google Play
    google_data = clean_google_duplicates(google_data)

    # 3. Filter to English + free apps
    google_data, apple_data = filter_english_and_free(google_data, apple_data)

    # 4. Analysis – Apple Store
    print("average number of rating by genre for the Apple Store:\n")
    apple_genre_avgs = compute_apple_genre_avg_ratings(apple_data)
    for genre, avg_rating in apple_genre_avgs.items():
        print(genre, ':', avg_rating)

    # 5. Analysis – Google Play
    print("\naverage number of installs by Category for the Google Play Store:\n")
    google_category_avgs = compute_google_category_avg_installs(google_data)
    for category, avg_installs in google_category_avgs.items():
        print(category, ':', avg_installs)


if __name__ == "__main__":
    main()
