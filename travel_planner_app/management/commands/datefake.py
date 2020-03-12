import datetime
from dateutil.relativedelta import relativedelta
from faker import Faker
fake = Faker("en_US")

date_end = datetime.datetime.now()
date_start = date_end + relativedelta(months=-1)
fake.date_between_dates(date_start=date_start, date_end=date_end)
datetime.date(2019, 10, 27)
fake.date_between_dates(date_start=date_start, date_end=date_end)