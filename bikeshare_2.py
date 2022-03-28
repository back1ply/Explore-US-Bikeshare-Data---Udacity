import time
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

MONTH_DATA = [ "january", "february", "march", "april", "may", "june" ]

DAY_DATA = [ "monday", "tuesday", "wednesday" , "thursday", "friday" , "saturday" ,"sunday" ]

FILTER_CHOICE = [ "month", "day", "both", "none" ]

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    [print(city, end = "  ") for city in CITY_DATA.keys()]
    city = input('\nSelect your city from the above: ').lower()
    while not city in CITY_DATA:
        [print(city, end = "  ") for city in CITY_DATA.keys()]
        city = input('\nPlease select a VALID city from the above or type Q to exit: ').lower()
        if city == "q":
            exit()
    print(city)

    # get user input for month & day or all or none or all
    [print(input_choice, end = "  ") for input_choice in FILTER_CHOICE]
    input_choice = input('\nPlease select your filter choice from the above: ').lower()
    while not input_choice in FILTER_CHOICE:
        [print(input_choice, end = " ") for input_choice in FILTER_CHOICE]
        input_choice = input('\nPlease select a VALID filter choice from the above: ').lower()
    if input_choice == "both" or input_choice == "month": 
        # get user input for month (all, january, february, ... , june)
        month = ""
        while not month in MONTH_DATA:
            [print(month, end = "  ") for month in MONTH_DATA]
            month = input('\nPlease select a month from the above or type "all" for all months: ').lower()
            if month  == "all":
                month = "none"
                break
        print(month)
    else: month = "none"

    if input_choice == "both" or input_choice == "day":
        # get user input for day of weechik (all, monday, tuesday, ... sunday)
        day = ""
        while not day in DAY_DATA:
            [print(day, end = "  ") for day in DAY_DATA]
            day = input('\nPlease select a day from the above or "all" for all days: ').lower()
            if day == "all":
                day = "none"
                break
        print(day)
    else: day = "none"

    print('-'*40)
    return city, month, day


def load_data(city, month, day):
    """
    Loads data for the specified city and filters by month and day if applicable.

    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    Returns:
        df - Pandas DataFrame containing city data filtered by month and day
    """
    df = pd.read_csv(CITY_DATA[city])
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['month'] = df['Start Time'].dt.month_name().str.lower()
    df["day"] = df['Start Time'].dt.day_name().str.lower()
    df['hour'] = df['Start Time'].dt.hour

    if month != "none":
        df = df[df['month'] == month]

    if day != "none":
        df = df[df['day'] == day]

    print(df)
    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    popular_month = df['month'].mode()[0]
    print("Most popular month is", popular_month)

    # display the most common day of week
    popular_day = df['day'].mode()[0]
    print("Most popular day is", popular_day)

    # display the most common start hour
    popular_hour = df['hour'].mode()[0]
    print("Most popular start hour is", popular_hour)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    popular_start = df['Start Station'].mode()[0]
    print("Most popular start station is", popular_start)

    # display most commonly used end station
    popular_end = df['End Station'].mode()[0]
    print("Most popular end station is", popular_end)

    # display most frequent combination of start station and end station trip
    popular_comb = (df['Start Station'] + " + " + df['End Station']).mode()[0]
    print("Most popular start and end station is", popular_comb)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    total_travel = df['Trip Duration'].sum()
    print("Total travel time is", total_travel, "seconds.")

    # display mean travel time
    mean_travel = df['Trip Duration'].mean()
    print("Mean travel time is", mean_travel, "seconds.")


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    user_type_count = df['User Type'].value_counts()
    print("User type count is\n",user_type_count)

    # Display counts of gender
    if "Gender" in df.columns:
        user_gender_count = df['Gender'].value_counts()
        print("\nUser gender count is\n",user_gender_count)
    else:
        print("\nSorry no gender data available")

    # Display earliest, most recent, and most common year of birth
    if "Birth Year" in df.columns:
        earliest_bd = df['Birth Year'].min()
        print("\nEarliest year of birth is:", earliest_bd)
        recent_bd = df['Birth Year'].max()
        print("Recent year of birth is:",recent_bd)
        comm_bd = df['Birth Year'].mode()[0]
        print("Comman year of birth is:", comm_bd)
    else:
        print("\nSorry no birth year data available")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def read_rows(df):
    """Asks user if wants to read 5 rows of raw data"""
    user_input = "y"
    x = 0
    while user_input != "n":
        user_input = input('\nWould you like to read 5 rows of raw data? (y/n)?\n')
        if user_input == "y":
            temp_df = df.copy()
            print(temp_df.iloc[x:x+5])
            x+= 5

def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        read_rows(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
