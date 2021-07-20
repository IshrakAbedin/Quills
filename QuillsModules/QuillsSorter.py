import glob
import json
from typing import Dict, Iterator, List

class TaskFillTarget:
    Question = 0
    Answer = 1
    Tag = 2

class QuestionAnswerPair:
    def __init__(self, question : str, answer : str) -> None:
        self.Question = question
        self.Answer = answer

class Task:
    def __init__(self, question : str = "", answer : str = "", tags : List[str] = []) -> None:
        self.Question = question
        self.Answer = answer
        self.Tags = tags.copy()

    def _printSelf(self):
        print("---Tag---")
        print(self.Tags)
        print("---Question---")
        print(self.Question)
        print("---Answer---")
        print(self.Answer)

    def generateTaskFromFile(self, filePath : str) -> None:
        lines : List[str] = []
        questionLines : List[str] = []
        answerLines : List[str] = []
        target = TaskFillTarget.Question
        with open(filePath, 'r') as taskFile:
            lines = taskFile.readlines()
        
        for line in lines:
            if(line.lstrip().rstrip().lower() == "# question"):
                target = TaskFillTarget.Question
            elif(line.lstrip().rstrip().lower() == "# answer"):
                target = TaskFillTarget.Answer
            elif(line.lstrip().rstrip().lower() == "# tag"):
                target = TaskFillTarget.Tag
            else:
                if(target == TaskFillTarget.Question):
                    questionLines.append(line)
                elif(target == TaskFillTarget.Answer):
                    answerLines.append(line)
                elif(target == TaskFillTarget.Tag):
                    splittedTags = line.split(',')
                    for tag in splittedTags:
                        self.Tags.append(tag.lstrip().rstrip().lower())

        self.Question = "".join(questionLines).lstrip().rstrip()
        self.Answer = "".join(answerLines).lstrip().rstrip()

class UnsortedTaskCollection:
    def __init__(self, taskList : List[Task] = []) -> None:
        self.TaskList : List[Task] = []

    def __iter__(self) -> Iterator[Task]:
        return self.TaskList.__iter__()

    def generateFromPathPattern(self, pathPattern : str) -> None:
        taskFiles = glob.glob(pathPattern)
        for taskFile in taskFiles:
            task = Task()
            task.generateTaskFromFile(taskFile)
            self.TaskList.append(task)

    def getLength(self) -> int:
        return len(self.TaskList)

    def getAllTagsList(self) -> List[str]:
        tagSet = set()
        for task in self.TaskList:
            for tag in task.Tags:
                tagSet.add(tag)
        return list(tagSet)

class SortedTaskCollection:
    def __init__(self) -> None:
        self.TaskDictionary : Dict[str, List[QuestionAnswerPair]] = {}

    def __iter__(self) -> Iterator[str]:
        return self.TaskDictionary.__iter__()

    def addQuestionAnswerPair(self, tag : str, qa : QuestionAnswerPair) -> None:
        keys = self.TaskDictionary.keys()
        if(tag in keys):
            self.TaskDictionary[tag].append(qa)
        else:
            self.TaskDictionary[tag] = []
            self.TaskDictionary[tag].append(qa)

    def generateFromUnsortedTasks(self, unsortedTaskCorpus : UnsortedTaskCollection) -> None:
        for task in unsortedTaskCorpus.TaskList:
            for tag in task.Tags:
                self.addQuestionAnswerPair(tag, QuestionAnswerPair(task.Question, task.Answer))

    def generateFromPathPattern(self, pathPattern : str) -> None:
        uTaskCollection = UnsortedTaskCollection()
        uTaskCollection.generateFromPathPattern(pathPattern)
        self.generateFromUnsortedTasks(uTaskCollection)

    def getTags(self) -> List[str]:
        return self.TaskDictionary.keys()

    def getLengths(self) -> List[int]:
        lengths : List[int] = []
        for key in self.TaskDictionary.keys():
            lengths.append(len(self.TaskDictionary[key]))
        return lengths

    def getQuestionAnswerPairListByTag(self, tag : str) -> List[QuestionAnswerPair]:
        if (tag not in self.TaskDictionary.keys()) : return []
        else : return self.TaskDictionary[tag]

    def serializeToJson(self, outJsonPath : str) -> None:
        with open(outJsonPath, 'w+') as outJsonFile:
            taskDict : Dict[str, List[Dict[str, str]]] = {}
            for tag in self.getTags():
                taskDict[tag] = []
                qapList = self.getQuestionAnswerPairListByTag(tag)
                for qa in qapList:
                    taskDict[tag].append(qa.__dict__)
            taskDictStr = json.dumps(taskDict)
            outJsonFile.write(taskDictStr)

    def deserializeFromJson(self, inJsonPath : str) -> None:
        taskDict : Dict[str, List[Dict[str, str]]] = {}
        with open(inJsonPath, 'r') as jsonFile:
            taskDict = json.load(jsonFile)
        for key in taskDict.keys():
            for qap in taskDict[key]:
                self.addQuestionAnswerPair(key, QuestionAnswerPair(qap["Question"], qap["Answer"]))
