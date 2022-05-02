import faker
import pandas as pd
from collections import defaultdict

fake_result = defaultdict(list)
fake = faker.Faker()
faker.Faker.seed(0)
for i in range(30):
    data_dict = fake.simple_profile()
    for k,v in data_dict.items():
        fake_result[k].append(v)

fake_df = pd.DataFrame(fake_result)
fake_df['dt'] = '20220430'
fake_df.to_csv('fake_data.csv',index=False,header=True)