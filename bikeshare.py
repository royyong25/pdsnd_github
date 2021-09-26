import time
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }
months = ['january', 'february', 'march', 'april', 'may', 'june','july','august','september','october','november','december']

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
    while True:
        try:
            city = input("Would you like to see data for Chicago, New York, or Washington?\n")
            city = city.lower()
        except ValueError:
            print("Sorry, it is a not a valid city name.")
            continue
        if city.lower() not in ("chicago","new york city","washington"):
            print("Sorry, it is a not a valid city name.")
            continue
        else:
            break
    # get user input for month (all, january, february, ... , june)
    while True:
        try:
            month = input("Would you like to filter the data by month (e.g. June) or not at all? Type \"all\" to apply no month filter.\n")
            month = month.lower()
        except ValueError:
            print("Sorry, it is a not a valid month name.")
            continue
        if month.lower() not in ("all","january","february","march","april","may","june","july","august","september","october","november","december"):
            print("Sorry, it is a not a valid month name.")
            continue
        else:
            break
    # get user input for day of week (all, monday, tuesday, ... sunday)
    while True:
        try:
            day = input("Would you like to filter the data by day of week (e.g. Sunday) or Not at all? Type \"all\" to apply no day of week filter.\n")
            day = day.lower()
        except ValueError:
            print("Sorry, it is not a valid name for day of week.")
            continue
        if day.lower() not in ("all","monday","tuesday","wednesday","thursday","friday","saturday","sunday"):
            print("Sorry, it is not a valid name for day of week.")
            continue
        else:
            break

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
    # load data file into a dataframe
    df = pd.read_csv(CITY_DATA[city.lower()])

    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # extract month and day of week from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.weekday_name


    # filter by month if applicable
    if month != 'all':
       # use the index of the months list to get the corresponding int
        month = months.index(month) + 1

        # filter by month to create the new dataframe
        df = df[df['month'] == month]

    # filter by day of week if applicable
    if day != 'all':
        # filter by day of week to create the new dataframe
        df = df[df['day_of_week'] == day.title()]

    return df


def time_stats(df,month,day):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display current month filter or display the most common month
    if month != 'all':
        print('The current month filter: ', month.title())
    else:
        popular_month = df['month'].mode()[0]
        popular_month_name = months[popular_month-1]
        print('Most popular month: ', popular_month_name.title())

    # display current day filter or display the most common day of week
    if day != 'all':
        print('The current day filter: ', day.title())
    else:
        popular_day = df['day_of_week'].mode()[0]
        print('Most popular day of week: ', popular_day.title())

    # display the most common start hour
    df['hour'] = df['Start Time'].dt.hour
    popular_hour = df['hour'].mode()[0]
    print('Most popular hour: ', popular_hour)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    popular_start_station = df['Start Station'].mode()[0]
    print('Most popular start station: ', popular_start_station)

    # display most commonly used end station
    popular_end_station = df['End Station'].mode()[0]
    print('Most popular end station: ', popular_end_station)

    # display most frequent combination of start station and end station trip
    popular_start_end = df.groupby(['Start Station','End Station']).size().nlargest(1)
    print('Most popular combination: ', popular_start_end)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    total_travel_time = df['Trip Duration'].sum()
    print('Total travel time: ', total_travel_time)

    # display mean travel time
    mean_travel_time = df['Trip Duration'].mean()
    print('Mean travel time: ', mean_travel_time)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display breakd of user types
    user_types = df['User Type'].value_counts()
    print(user_types)
    print('\n')

    # Display counts of gender
    gender = df['Gender'].value_counts()
    print(gender)
    print('\n')

    # Display earliest, most recent, and most common year of birth
    earliest_year = df['Birth Year'].min()
    recent_year = df['Birth Year'].max()
    popular_year = df['Birth Year'].mode()[0]

    print('Earliest year of birth: ', earliest_year)
    print('Most recent year of birth: ', recent_year)
    print('Most common year of birth: ', popular_year)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('\n')

def raw_data(df):
    """Ask user to displays 5 rows of raw data."""
    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Check if users want to see data
    # Continue to load another 5 rows of data or move to next question
    start_loc = 0
    question = '\nWould you like to view 5 rows of user data? Enter yes or no.\n'
    while True:
        display_data = input('\nWould you like to see 5 lines of raw data? Enter yes or no.\n')
        if display_data.lower() != 'yes':
            break
        print(tabulate(df_default.iloc[np.arange(0+i,5+i)], headers ="keys"))
        i+=5

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df, month, day)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        raw_data(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
