import pandas as pd
import random

data = {
    'Mentor ID': [f'M{str(i).zfill(4)}' for i in range(1, 11)],
    'Name': [f'Mentor {i}' for i in range(1, 11)],
    'Gender': [random.choice(['Male', 'Female']) for _ in range(10)],
    'Age': [random.randint(30, 60) for _ in range(10)],
    'Expertise': [random.choice(['Data Science', 'Software Engineering', 'Cybersecurity', 'Cloud Computing', 'AI & ML']) for _ in range(10)],
    'Experience': [random.randint(5, 20) for _ in range(10)],
    'Skills': [', '.join(random.sample(['Python', 'Java', 'SQL', 'Machine Learning', 'Cloud Services'], 3)) for _ in range(10)],
    'Current Position': [random.choice(['Senior Developer', 'Data Scientist', 'Software Engineer', 'Systems Analyst', 'Cloud Architect']) for _ in range(10)],
    'Preferred Domain': [random.choice(['AI & ML', 'Data Science', 'Software Development', 'Cybersecurity']) for _ in range(10)],
    'Availability': [random.choice(['Weekdays', 'Weekends', 'Flexible']) for _ in range(10)]
}

mentor_df = pd.DataFrame(data)

mentor_df.to_csv('mentors_dataset.csv', index=False)
