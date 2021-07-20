from typing import List
from QuillsModules.QuillsSorter import SortedTaskCollection
from QuillsModules.QuillsRandom import nonRepeatingRandomInRange
from os import path
import csv
import random

def _writeTaskSolveForStudent(taskOutPath : str, solveOutPath : str, title : str, sortedTasks : SortedTaskCollection, **perTagCount) -> None:
    taskLines : List[str] = [f"# {title}\n"]
    solveLines : List[str] = [f"# SOLVE : {title}\n"]
    questionCounter = 1

    for tag in perTagCount:
        taskCount = perTagCount[tag]
        qapList = sortedTasks.getQuestionAnswerPairListByTag(tag)
        if(taskCount > len(qapList)):
            print(f"[ERROR!] (tag: {tag}) Task count ({taskCount}) is more than collection ({len(qapList)}).")
            exit(1)
        indiceCollection = nonRepeatingRandomInRange(len(qapList), taskCount)
        for chosenIndex in indiceCollection:
            taskLines.append(f"## Question {questionCounter} (tag: {tag})\n---\n")
            solveLines.append(f"## Question {questionCounter} (tag: {tag})\n---\n")
            qap = qapList[chosenIndex]
            taskLines.append(qap.Question)
            solveLines.append(qap.Question)
            solveLines.append(f"## Answer {questionCounter} (tag: {tag})\n---\n")
            solveLines.append(qap.Answer)
            taskLines.append("\n")
            solveLines.append("\n")
            questionCounter += 1

    taskStr = "\n".join(taskLines)
    solveStr = "\n".join(solveLines)

    with open(taskOutPath, 'w+') as taskFile:
        taskFile.write(taskStr)
    with open(solveOutPath, 'w+') as solveFile:
        solveFile.write(solveStr)

def generateSortedTaskCollection(unsortedTasksPattern_IN : str, sortedTaskPath_OUT : str) -> None:
    inPath = path.abspath(unsortedTasksPattern_IN)
    outPath = path.abspath(sortedTaskPath_OUT)
    sortedTasks = SortedTaskCollection()
    sortedTasks.generateFromPathPattern(inPath)
    sortedTasks.serializeToJson(outPath)

def generateTasksSolvesFromSortedTaskCollection(taskname : str, sortedTaskPath_IN : str, studentListPath_IN : str, taskPath_OUT : str, solvePath_OUT : str, **perTagCount) -> None:
    absInTaskPath = path.abspath(sortedTaskPath_IN)
    absInStdListPath = path.abspath(studentListPath_IN)
    absOutTaskPath = path.abspath(taskPath_OUT)
    absOutSolvePath = path.abspath(solvePath_OUT)
    sortedTasks = SortedTaskCollection()
    sortedTasks.deserializeFromJson(absInTaskPath)

    with open(absInStdListPath) as csvfile:
        studentRowDict = csv.DictReader(csvfile)
        for row in studentRowDict:
            ID = row['ID']
            name = row['Name']
            title = f"{taskname} for {ID} ({name})"
            taskOutpath = path.join(absOutTaskPath, f"{taskname}_{ID}.md")
            solveOutpath = path.join(absOutSolvePath, f"{taskname}_{ID}_SOLVE.md")
            _writeTaskSolveForStudent(taskOutpath, solveOutpath, title, sortedTasks, **perTagCount)
    