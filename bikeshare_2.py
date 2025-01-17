import time
import pandas as pd
import numpy as np
import ctypes

# Constants from the Windows API
STD_OUTPUT_HANDLE = -11
FOREGROUND_RED    = 0x0004 # text color contains red.
FOREGROUND_GREEN  = 0x0002 # text color contains green.

"""
Script to analyse and filter bike share data

Changelog:

Date       Version Author Comments
---------- ------- ------ ------------------------
24/04/2023     1.1     BT Added changelog


"""

YES_NO = ['yes', 'no']

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

MONTHS = { 'january': 1,
               'february' : 2,
               'march' : 3, 
               'april' : 4,
               'may' : 5,
               'june' : 6,
               'july' : 7,
               'august' : 8,
               'september' : 9,
               'october' : 10,
               'november' : 11,
               'december' : 12,
               'all' : -1 }

DAYS = { 'monday': 0,
         'tuesday' : 1,
         'wednesday' : 2, 
         'thursday' : 3,
         'friday' : 4,
         'saturday' : 5,
         'sunday' : 6,               
         'all' : -1 }

def get_csbi_attributes(handle):
    # Based on IPython's winconsole.py, written by Alexander Belchenko
    import struct
    csbi = ctypes.create_string_buffer(22)
    res = ctypes.windll.kernel32.GetConsoleScreenBufferInfo(handle, csbi)
    assert res

    (bufx, bufy, curx, cury, wattr,
    left, top, right, bottom, maxx, maxy) = struct.unpack("hhhhHhhhhhh", csbi.raw)
    return wattr

def display_message(message, message_level = "info"):
    """
    Displays message to the user
    Args:
        (str) - message - what to display to the user

    """
    handle = ctypes.windll.kernel32.GetStdHandle(STD_OUTPUT_HANDLE)
    reset = get_csbi_attributes(handle)

    if (message_level == "error"):
        ctypes.windll.kernel32.SetConsoleTextAttribute(handle, FOREGROUND_RED)
        print(message)
        
    else:
        ctypes.windll.kernel32.SetConsoleTextAttribute(handle, FOREGROUND_GREEN)
        print(message)
    
    ctypes.windll.kernel32.SetConsoleTextAttribute(handle, reset)

    #print(CREDBG2 + message)
        
def get_valid_input(prompt, valid_values):
    """
    Get input from the user and validates against a valid list of options
    Args:
        (str) - prompt to display to the user
        (array) - array of valid input options
    Returns:
        (str) - input value 
    """
    valid_values_string = "/".join(valid_values)

    input_value = input('\n' + prompt + '\n   Valid options are: ' + valid_values_string + '\n')

    while True:
        for valid_value in valid_values:
            #print ("Checking " + input_value + ' against ' + valid_value)
            if input_value.lower() == valid_value.lower():
                return valid_value
        
        display_message('   Sorry "' + input_value + '" is not a valid value.','error')
        input_value = input('\n' + prompt + '\n   Valid options are: ' + valid_values_string + '\n')

    return ""

def get_month_name(month_number):
    """
    Get the name of a month based on its number
    Args:
        (int) month_number
    Returns:
        (str) month - name of the month 
    """
    for m_name, m_number in MONTHS.items():
        if m_number == month_number:
            return m_name
    
    return ''

def get_day_name(day_number):
    """
    Get the name of a day based on its number
    Args:
        (int) day_number
    Returns:
        (str) day - name of the day 
    """
    for d_name, d_number in DAYS.items():
        if d_number == day_number:
            return d_name
    
    return ''

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
    city = get_valid_input('Which city do you want to analyse?',CITY_DATA.keys())   

    # get user input for month (all, january, february, ... , june)
    month = get_valid_input('Which month do you want to analyse?',MONTHS.keys())
        
    # get user input for day of week (all, monday, tuesday, ... sunday)
    day = get_valid_input('Which day do you want to analyse?',DAYS.keys())
    
    display_message('-'*40)  
    display_message('Processing City=' + city + ' Month=' + month + '(' + str(MONTHS[month]) + ') Day=' + day + '(' + str(DAYS[day]) +')' )  
    display_message('-'*40) 

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
    
    # Set the start and end times to be of the datetime type
    df['Start Time']= pd.to_datetime(df['Start Time'])
    df['End Time']= pd.to_datetime(df['Start Time'])
   
    # Create some helper columns
    df['start_month'] = df['Start Time'].dt.month
    df['start_weekday'] = df['Start Time'].dt.weekday
    df['start_hour'] = df['Start Time'].dt.hour
    
    # Apply filters, if requested
    if month != 'all':
        # Filter on month
        #df = df[df['Start Time'].dt.strftime('%B') == month]
        df = df[df['start_month'] == MONTHS[month]]

    if day != 'all':
        # Filter on day
        df = df[df['start_weekday']== DAYS[day]]

    #print(df)    
    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    # Check if there is any time data
    if df['Start Time'].count() == 0:
        display_message('Sorry there is no time data to report on.','error')
        return

    display_message('Calculating The Most Frequent Times of Travel...')
    start_time = time.time()

    # display the most common month
    common_month = df['start_month'].mode()[0]
    display_message('The most common month is: ' + get_month_name(common_month))

    # display the most common day of week
    common_day = df['start_weekday'].mode()[0]
    display_message('The most common day is: ' + get_day_name(common_day))

    # display the most common start hour
    common_hour = df['start_hour'].mode()[0]
    display_message('The most common hour is: ' + str(common_hour))

    display_message("This took %s seconds." % (time.time() - start_time))
    display_message('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    # Check if there is any station data
    if df['Start Station'].count() == 0:
        display_message('Sorry there is no station data to report on.','error')
        return

    display_message('Calculating The Most Popular Stations and Trip...')
    start_time = time.time()

    # display most commonly used start station
    common_start_station = df['Start Station'].mode()[0]

    display_message('The most common start station is: ' + common_start_station)

    # display most commonly used end station
    common_end_station = df['End Station'].mode()[0]

    display_message('The most common end station is: ' + common_end_station)

    # display most frequent combination of start station and end station trip
    # Add a column containng the start and end stations
    df['start_end_station'] = df['Start Station'] + ' - ' + df['End Station']
    common_start_end_station = df['start_end_station'].mode()[0]

    display_message('The most common start and end station combo is: ' + common_start_end_station)

    display_message("This took %s seconds." % (time.time() - start_time))
    display_message('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    # Check if there is any trip data
    
    if df['Trip Duration'].count() == 0:
        display_message('Sorry there is no trip data to report on.','error')
        return

    display_message('Calculating Trip Duration...')
    start_time = time.time()

    # display total travel time
    total_trip_duration = df['Trip Duration'].sum()
    display_message('The total trip duration is ' + str(total_trip_duration) + ' seconds')

    # display mean travel time
    mean_trip_duration = df['Trip Duration'].mode()[0]
    display_message('The mean trip duration is ' + str(mean_trip_duration) + ' seconds')

    display_message("This took %s seconds." % (time.time() - start_time))
    display_message('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    # Check if there is any user data
    if df['User Type'].count() == 0:
        display_message('Sorry there is no user data to report on.','error')
        return

    display_message('Calculating User Stats...')
    start_time = time.time()

    # Display counts of user types
    user_types = df.value_counts(['User Type'])
    display_message("The following table shows the count of different user types:")
    display_message (user_types)

    # Display counts of gender    
    if 'Gender' in df.columns:
        display_message("The following table shows the count of different genders:")
        gender_counts = df.value_counts(['Gender'])        
        display_message (gender_counts)
    else:
        display_message("This data contains no gender data")

    if 'Birth Year' in df.columns:
        # Display earliest, most recent, and most common year of birth
        earliest_year_of_birth = df['Birth Year'].min()
        recent_year_of_birth = df['Birth Year'].max()
        common_year_of_birth = df['Birth Year'].mode()[0]

        display_message('The earliest year of birth is : ' + str(int(earliest_year_of_birth)))
        display_message('The most recent year of birth is : ' + str(int(recent_year_of_birth)))
        display_message('The most common year of birth is : ' + str(int(common_year_of_birth)))
    else:
        display_message('This data does not contain birth years.')

    display_message("This took %s seconds." % (time.time() - start_time))
    display_message('-'*40)

def display_data(df):
    """Displays data 5 records at a time."""
    
    start_time = time.time()

    start_row = 0
    end_row = 5
    max_rows = len(df.index)
    answer = get_valid_input('Would you like to display the raw data?', YES_NO)
    if answer == 'yes':
        display_message((df[start_row:end_row]).to_string(index=False))
        display_message ('Displayed rows ' + str(start_row) + ' to ' + str(end_row) + ' of ' + str(max_rows) + ' rows')
    else:
        return

    while end_row < max_rows:
        answer = get_valid_input('Display more raw data?', YES_NO)
        if answer == "yes":           
            start_row += 5
            end_row += 5
            display_message((df[start_row:end_row]).to_string(index=False, header=False))
            display_message ('Displayed rows ' + str(start_row) + ' to ' + str(end_row) + ' of ' + str(max_rows) + ' rows')
        else:
            display_message("")
            break
    else:
        end_row = max_rows
        display_message("You have reached the end of the data")


    display_message("This took %s seconds." % (time.time() - start_time))
    display_message('-'*40)

def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)
        display_data(df)
        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)

        answer = get_valid_input('Would you like to restart?', YES_NO)
        if answer == "no":         
            break


if __name__ == "__main__":
	main()
