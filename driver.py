import Quills

def main():
    Quills.generateSortedTaskCollection("./UCOLLECTION/*.md", "./SCOLLECTION/SC.json")
    Quills.generateTasksSolvesFromSortedTaskCollection("Quiz1",\
        "./SCORPUS/SC.json",\
            "./STUDENTLIST/StudentList.csv",\
                "./OUTPUT/Tasks",\
                    "./OUTPUT/Solves",\
                        easy=1, medium=1, hard=1)
    
    # Still need to solve without-replacement randomizer


main()