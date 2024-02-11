# TODO: add GUI
# TODO: add RL to recommend tasks
# TODO: add visualizations

import pandas as pd
import os 
class Task:
    def __init__(self, task, deadline, time_expected, priority, time_spent, tag, completed=False):
        self.task = task
        self.deadline = deadline
        self.time_expected = time_expected
        self.priority = priority
        self.time_spent = time_spent
        self.tag = tag
        self.completed = completed

    def __str__(self):
        return f"{self.task} {self.deadline} {self.time_expected} {self.priority} {self.time_spent} {self.tag} {self.completed}"

# Create a IO to create a task and add to dataframe
def create_task():
    task = input("Enter the task: ")
    deadline = input("Enter the deadline: ")
    time_expected = input("Enter the time expected: ")
    priority = input("Enter the priority: ")
    time_spent = input("Enter the time spent: ")
    tag = input("Enter the tag: ")
    return Task(task, deadline, time_expected, priority, time_spent, tag)

def update_task(tasks):
    tt = input("Enter the task to update: ")
    # print(here)
    if tt in [task.task for task in tasks]:
        print("here?")
        for task in tasks:
            if task.task == tt:
                print(task)
                print("1. Update name")
                print("2. Update deadline")
                print("3. Update time expected")
                print("4. Update priority")
                print("5. Update time spent")
                print("6. Update tag")
                print("7. Update completed")
                choice = input("Enter your choice: ")
                if choice == "1":
                    task.task = input("Enter the task: ")
                elif choice == "2":
                    task.deadline = input("Enter the deadline: ")
                elif choice == "3":
                    task.time_expected = input("Enter the time expected: ")
                elif choice == "4":
                    task.priority = input("Enter the priority: ")
                elif choice == "5":
                    task.time_spent = input("Enter the time spent: ")
                elif choice == "6":
                    task.tag = input("Enter the tag: ")
                elif choice == "7":
                    task.completed = input("Enter the completed: ")
                else:
                    print("Invalid choice")
    else:
        print("Task not found")
    return tasks


# algorithm: find the shortest task that is not done with the closest deadline weighted by priority
def recommend_task(tasks):
    # convert to df
    df = convert_to_df(tasks)
    df["time_remaining"]=df["time_expected"]-df["time_spent"]
    
    df=df[df["time_spent"]<df["time_expected"]] # replace by completed tag
    
    # calculate the time left
    df["time_left"]=df["deadline"]-pd.Timestamp.now()
    df["time_left"]=df["time_left"].dt.total_seconds()
    df["time_left"]=df["time_left"]/3600 # convert to hours
    # calculate the priority
    df["priority"]=df["priority"].astype(int)
    df["priority"]=round(df["priority"]+(df["time_left"]*-0.05))
    
    # # find the tasks with the highest priority
    # df=df[df["priority"]==df["priority"].max()]
    # # find the tasks with the shortest time excepted left
    
    # df=df[df["time_remaining"]==df["time_remaining"].min()]
    # order by max priority, min time remaining
    df=df.sort_values(by=["priority","time_remaining"],ascending=[False,True])

    return df


def convert_to_df(tasks):
    df = pd.DataFrame([vars(task) for task in tasks])
    df["deadline"] = pd.to_datetime(df["deadline"])
    df["time_expected"] = pd.to_timedelta(df["time_expected"])
    df["time_spent"] = pd.to_timedelta(df["time_spent"])
    df["completed"] = df["completed"].astype(bool)
    return df

def main():
    # read csv 
    # if exists
    if os.path.exists("tasks.csv"):
        df = pd.read_csv("tasks.csv")
        tasks = [Task(**row) for row in df.to_dict(orient="records")]
    else:
        tasks = []
    while True:
        # print all choices in 1 line
        choices=["Create a task","View tasks","Update tasks","Delete tasks","Recommend tasks","Exit"]
        print("\t".join([f"{i+1}. {choice}" for i,choice in enumerate(choices)]))
        choice = input("Enter your choice: ")
        if choice == "1":
            tasks.append(create_task())
        elif choice == "2":
            df = convert_to_df(tasks)
            df.sort_values(by=["completed","deadline"], inplace=True)
            # convert time expected and time spent to hours
            df["time_expected"] = df["time_expected"].dt.total_seconds()/3600
            df["time_spent"] = df["time_spent"].dt.total_seconds()/3600
            # round both and add hrs
            df["time_expected"] = df["time_expected"].round(2).astype(str) + " hrs"
            df["time_spent"] = df["time_spent"].round(2).astype(str) + " hrs"
            print()
            print(df)
            print()
        elif choice == "3":
            update_task(tasks)
        elif choice == "4":
            tasks = [task for task in tasks if task.task != input("Enter the task to delete: ")]
        elif choice == "5":
            print(recommend_task(tasks))
            print()
        elif choice == "6":
            break
        else:
            print("Invalid choice")
    # convert to df
    df = convert_to_df(tasks)
    print(df)
    df.to_csv("tasks.csv", index=False)

if __name__ == "__main__":
    main()