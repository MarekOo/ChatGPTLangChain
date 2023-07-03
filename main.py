#!pip install langchain
#!pip install chromadb
#!pip install tiktoken
#!pip install openai

import random
import os


from datetime import datetime, timedelta
from langchain.document_loaders import TextLoader
from langchain.indexes import VectorstoreIndexCreator
from langchain.llms import OpenAI
from langchain.chat_models import ChatOpenAI
from dotenv import load_dotenv

# define global variable data_file
data_file = "schedule.txt"

# create some demo data
def create_data():
    # List of possible activities
    activities = [
        "Meeting with client",
        "Lunch break",
        "Project deadline",
        "Team brainstorming",
        "Training session",
        "Coffee break",
        "Presentation preparation",
        "Networking event",
        "Code review",
        "Project meeting"
    ]

    # List of possible names for meetings
    meeting_names = [
        "Emma",
        "Daniel",
        "Olivia",
        "Andrew",
        "Sophia"
    ]

    client_names = [
        "John",
        "Jane",
        "Michael",
        "Emily",
        "David"
    ]

    # Number of schedule entries to generate
    num_entries = 30

    # Generate random schedule entries with dates, times, and names for meetings
    schedule_entries = []
    start_date = datetime.now()

    for _ in range(num_entries):
        entry_date = start_date + timedelta(days=random.randint(0, 7))
        entry_time = random.randint(8, 17), random.randint(0, 59)
        activity = random.choice(activities)

        if activity == "Meeting with client":
            person = random.choice(client_names)
            schedule_entry = f"{entry_date.strftime('%Y-%m-%d')} {entry_time[0]:02d}:{entry_time[1]:02d} - {activity} with {person}"
        elif activity == "Project meeting":
            person = random.choice(meeting_names)
            schedule_entry = f"{entry_date.strftime('%Y-%m-%d')} {entry_time[0]:02d}:{entry_time[1]:02d} - {activity} with {person}"
        else:
            schedule_entry = f"{entry_date.strftime('%Y-%m-%d')} {entry_time[0]:02d}:{entry_time[1]:02d} - {activity}"

        schedule_entries.append(schedule_entry)

    # Write schedule entries to a text file
    with open(data_file, "w") as file:
        for entry in schedule_entries:
            file.write(entry + "\n")

    print(f"{num_entries} schedule entries have been written to schedule.txt.")



if __name__ == '__main__':
    create_data()
    # show head (10 lines) of data_file
    with open(data_file) as f:
        print(f.read(10 * 1000))


    load_dotenv()

    # Access the environment variable
    api_key = os.getenv("API_KEY")

    os.environ["OPENAI_API_KEY"] = api_key

    loader = TextLoader(data_file)
    index = VectorstoreIndexCreator().from_loaders([loader])

    # test some queries on the index
    query = "Sum up the schedule"
    print(index.query(query))

    query = "Do I have Project meetings?"
    print(index.query(query))

    query = "What Meetings with clients do I have?"
    print(index.query(query))

    query = "Do I have Meetings with Olivia?"
    print(index.query(query))

