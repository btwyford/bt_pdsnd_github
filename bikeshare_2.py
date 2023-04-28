import time
import pandas as pd
import numpy as np

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
        
        input_value = input('\n' + '   Sorry but "' + input_value + '" is not a valid value.\n   Valid options are: ' + valid_values_string + '\n')

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
    
    print('-'*40)  
    print('Processing City=' + city + ' Month=' + month + '(' + str(MONTHS[month]) + ') Day=' + day + '(' + str(DAYS[day]) +')' )  
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
        print('\nSorry there is no time data to report on.\n')
        return

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    common_month = df['start_month'].mode()[0]
    print('The most common month is:', get_month_name(common_month))

    # display the most common day of week
    common_day = df['start_weekday'].mode()[0]
    print('The most common day is:', get_day_name(common_day))

    # display the most common start hour
    common_hour = df['start_hour'].mode()[0]
    print('The most common hour is:', common_hour)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    # Check if there is any station data
    if df['Start Station'].count() == 0:
        print('\nSorry there is no station data to report on.\n')
        return

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    common_start_station = df['Start Station'].mode()[0]

    print('The most common start station is:', common_start_station)

    # display most commonly used end station
    common_end_station = df['End Station'].mode()[0]

    print('The most common end station is:', common_end_station)

    # display most frequent combination of start station and end station trip
    # Add a column containng the start and end stations
    df['start_end_station'] = df['Start Station'] + ' - ' + df['End Station']
    common_start_end_station = df['start_end_station'].mode()[0]

    print('The most common start and end station combo is:', common_start_end_station)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    # Check if there is any trip data
    
    if df['Trip Duration'].count() == 0:
        print('\nSorry there is no trip data to report on.\n')
        return

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    total_trip_duration = df['Trip Duration'].sum()
    print('The total trip duration is ' + str(total_trip_duration) + ' seconds')

    # display mean travel time
    mean_trip_duration = df['Trip Duration'].mode()[0]
    print('The mean trip duration is ' + str(mean_trip_duration) + ' seconds')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    # Check if there is any user data
    if df['User Type'].count() == 0:
        print('\nSorry there is no user data to report on.\n')
        return

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    user_types = df.value_counts(['User Type'])
    print("\nThe following table shows the count of different user types:\n")
    print (user_types)

    # Display counts of gender    
    if 'Gender' in df.columns:
        print("\nThe following table shows the count of different genders:\n")
        gender_counts = df.value_counts(['Gender'])        
        print (gender_counts)
    else:
        print("\nThis data contains no gender data\n")

    if 'Birth Year' in df.columns:
        # Display earliest, most recent, and most common year of birth
        earliest_year_of_birth = df['Birth Year'].min()
        recent_year_of_birth = df['Birth Year'].max()
        common_year_of_birth = df['Birth Year'].mode()[0]

        print('\nThe earliest year of birth is :', int(earliest_year_of_birth))
        print('\nThe most recent year of birth is :', int(recent_year_of_birth))
        print('\nThe most common year of birth is :', int(common_year_of_birth))
    else:
        print('\nThis data does not contain birth years.\n')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def display_data(df):
    """Displays data 5 records at a time."""
    
    start_time = time.time()

    start_row = 0
    end_row = 5
    max_rows = len(df.index)
    answer = get_valid_input('Would you like to display the raw data?', YES_NO)
    if answer == 'yes':
        print((df[start_row:end_row]).to_string(index=False))
        print ('Displayed rows ' + str(start_row) + ' to ' + str(end_row) + ' of ' + str(max_rows) + ' rows')
    else:
        return

    while end_row < max_rows:
        answer = get_valid_input('Display more raw data?', YES_NO)
        if answer == "yes":           
            start_row += 5
            end_row += 5
            print((df[start_row:end_row]).to_string(index=False, header=False))
            print ('Displayed rows ' + str(start_row) + ' to ' + str(end_row) + ' of ' + str(max_rows) + ' rows')
        else:
            print("\n")
            break
    else:
        end_row = max_rows
        print("\nYou have reached the end of the data\n")


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

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
