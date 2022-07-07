import pandas as pd
from faker import Faker

def generate_name():
    fake = Faker()
    fake_name = fake.name()
    return fake_name
    
# # Usage example
# df = pd.DataFrame({'id': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]})
# df["name"] = df.apply(lambda x: generate_name(), axis=1)
# df