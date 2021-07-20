import Quills

def main():
    Quills.generateSortedTaskCollection("./UCOLLECTION/*.md", "./SCOLLECTION/SC.json")
    Quills.generateTasksSolvesFromSortedTaskCollection("Quiz1",\
        "./SCOLLECTION/SC.json",\
            "./STUDENTLIST/StudentList.csv",\
                "./OUTPUT/Tasks",\
                    "./OUTPUT/Solves",\
                        easy=1, medium=2, hard=1)


main()