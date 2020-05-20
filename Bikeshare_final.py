def main():
    import time
    import pandas as pd
    import numpy as np

    CITY_DATA = { 'chicago': 'chicago.csv',
                'new york city': 'new_york_city.csv',
                'washington': 'washington.csv' }

    def get_filters():
        """
        Asks user to specify a city, month, and day to analyze.

        Returns:
            (str) city - name of the city to analyze
            (str) month - name of the month to filter by, or "all" to apply no month filter
            (str) day - name of the day of week to filter by, or "all" to apply no day filter
        """
        print('-'*40)
        print('\nHello! Let\'s explore some US bikeshare data!\n')

        #Gathers user input for city
        print('First, enter which city would you like to explore: Chicago, New York City, or Washington? ')
        city = input('Choice: ').lower()
        while city not in ('chicago', 'new york city', 'washington'):
            print('Whoops! Please enter one of the following: Chicago, New York City, Washington...')
            city = input().lower()

        #Gathers user input for month
        print('\nNext, enter which month you would like to look at from January to June.\nOr, you can enter "All" for to look at all months: ')
        month = input('Choice: ').lower()
        while month not in ('january', 'february', 'march', 'april', 'may', 'june', 'all'):
            print('Whoops! Please enter one of the following: January, February, March, April, May, June, or All...')
            month = input().lower()

        #Gathers user input for day of the week
        print('\nFinally, choose a day of the week to look at. Or, you can enter "All" to look at all days of the week.')
        day = input('Choice: ').lower()
        while day not in ('sunday', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'all'):
            print('Whoops! Please enter one of the following: Sunday, Monday, Tuesday, Wednesday, Thursday, Friday, Saturday, or All...')
            day = input().lower()

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
        # read in csv corresponding to city choice
        df = pd.read_csv(CITY_DATA[city])

        # convert the Start Time column to datetime
        df['Start Time'] = pd.to_datetime(df['Start Time'])

        # extract month and day of week from Start Time to create new columns
        df['month'] = df['Start Time'].dt.month
        df['day_of_week'] = df['Start Time'].dt.weekday_name
        df['hour'] = df['Start Time'].dt.hour


        # filter by month if applicable
        if month != 'all':
            months = ['january', 'february', 'march', 'april', 'may', 'june']
            month = months.index(month) + 1
        
            # filter by month to create the new dataframe
            df = df[df['month'] == month]

        # filter by day of week if applicable
        if day != 'all':
            # filter by day of week to create the new dataframe
            df = df[df['day_of_week']== day.title()]
        
        return df

    def time_stats(df):
        """Displays statistics on the most frequent times of travel."""
        print('All right, let\'s take a look at the data for {}.'.format(city.title()))

        print('\nCalculating The Most Frequent Times of Travel...\n')
        start_time = time.time()

        #Most common month
        if month == 'all':
            popular_month = df['month'].mode()[0]
            popular_day = df['day_of_week'].mode()[0]
            popular_hour = df['hour'].mode()[0]

            print('In {}, the most common month to use Bikeshare is {}.\n'.format(city.title(), popular_month))
            print('The most common day to use Bikeshare is {}.\n'.format(popular_day))
            print('Also, it may be a good idea to avoid using Bikeshare in hour {}.\n'.format(popular_hour))

        #Most common day of week
        elif day == 'all':
            popular_day = df['day_of_week'].mode()[0]
            popular_hour = df['hour'].mode()[0]

            print('In {}, the most common day in {} to use Bikeshare is {}.\n'.format(city.title(), month.title(), popular_day))
            print('Also, it may be a good idea to avoid using Bikeshare in hour {}.\n'.format(popular_hour))

        #Most common start hour
        else:
            popular_hour = df['hour'].mode()[0]
            popular_month = df['month'].mode()[0]
            popular_day = df['day_of_week'].mode()[0]
            popular_hour = df['hour'].mode()[0]
            print('If you\'re in {} on a {} in {}, it may be a good idea to avoid using Bikeshare in hour {}.\n'.format(city.title(), popular_day, month.title(), popular_hour))

        print("\nThis took %s seconds." % (time.time() - start_time))
        print('-'*40)

    def station_stats(df):
        """Displays statistics on the most popular stations and trip."""

        print('\nCalculating The Most Popular Stations and Trip...\n')
        start_time = time.time()

        #most commonly used start station
        popular_start = df['Start Station'].mode()[0]
        print('The most popular place to start a ride is at the {} Bikeshare station.\n'.format(popular_start))

        #most commonly used end station
        popular_end = df['End Station'].mode()[0]
        print('The most popular place to end a ride is at the {} Bikeshare station.\n'.format(popular_end))

        #most frequent route
        trips = []
        trip_count = {}
        for trip in zip(df['Start Station'], df['End Station']):
            trips.append('{} to {}.'.format(*trip))
        for route in trips:
            if route not in trip_count:
                trip_count[route] = 1
            else:
                trip_count[route] += 1
        most_trips = max(trip_count.values())
        popular_trip = [route for route, count in trip_count.items() if count == most_trips]

        print('The most common trip(s) taken in {} for this time frame is/are from {}.\n'.format(city.title(), popular_trip))

        print("\nThis took %s seconds." % (time.time() - start_time))
        print('-'*40)

    def trip_duration_stats(df):
        """Displays statistics on the total and average trip duration."""

        print('\nCalculating Trip Duration...\n')
        start_time = time.time()

        # Total travel time and average length of each trip
        total_travel_time = np.sum(df['Trip Duration'])
        mean_travel_time = np.mean(df['Trip Duration'])
        print('The total travel time during this time frame is {} minutes, and the average ride lasted {} minutes.'.format(total_travel_time/60, mean_travel_time/60))

        print("\nThis took %s seconds." % (time.time() - start_time))
        print('-'*40)

    def user_stats(df):
        """Displays statistics on bikeshare users."""

        print('\nCalculating User Stats...\n')
        start_time = time.time()

        #User Type Count
        user_type = df['User Type'].value_counts()
        print('Below is the number of each type of user during this time frame.')
        print(user_type)

        #User Count based on Gender
        if city in ('chicago', 'new york city'):
            user_gender = df['Gender'].value_counts()
            print('\nBelow is the total number of users for both Males and Females during this time.')
            print(user_gender)

        #earliest, most recent, and most common year of birth for users
            user_birth_year = df['Birth Year']
            print('\nThe earlist birth year of a user in this time frame is {}.'.format(int(user_birth_year.min())))
            print('\nThe most recent birth year of a user in this time frame is {}.'.format(int(user_birth_year.max())))
            print('\nThe most common birth year of a user in this time frame is {}.'.format(int(user_birth_year.mode()[0])))

            print("\nThis took %s seconds." % (time.time() - start_time))
        
        print('-'*40)

    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)
        
        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)

        see_data = input('Would you like to see the raw data for these statistics?\nPlease enter "yes" or "no": ')
        raw_data = pd.read_csv(CITY_DATA[city])
        x = 0
        y = 5
        while see_data.lower() == 'yes':
            print(raw_data[x:y])
            x += 5
            y += 5
            see_data = input('Would you like to see 5 more rows of raw data?\nPlease enter "yes" or "no": ')

        print('-'*40)

        restart = input('\nWould you like to start over with different filters? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break
        else:
            continue
        main()


if __name__ == "__main__":
	main()
