import pandas as pd
from faker import Faker
#from faker.providers import address, person # tried this withoout success
#from faker.providers.person import es_CO # tried this as well

fake = Faker('es_MX')
# fake.add_provider(person) doesn't help
# fake.add_provider(address) doesn't help

def generate_name():
    fake_name = fake.name()
    return fake_name
    
def generate_address():
    fake_address = fake.street_address()
    return fake_address

# Usage example
# df = pd.DataFrame({'id': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]})
# df["name"] = df.apply(lambda x: generate_name(), axis=1)
# df["address"] = df.apply(lambda x: generate_address(), axis=1)
# df