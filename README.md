# Quills

A simple random question-answer generator from a set of tagged questions in markdown format

## Usage

First import the library using:

```python
import Quills
```

You need to create sorted collection first from your unsorted questions in markdown. It can be done by calling:

```python
def generateSortedTaskCollection(unsortedTasksPattern_IN : str, sortedTaskPath_OUT : str) -> None
```

Then you can produce your final questions by calling the following function with appropriate values:

```python
def generateTasksSolvesFromSortedTaskCollection(taskname : str, sortedTaskPath_IN : str, studentListPath_IN : str, taskPath_OUT : str, solvePath_OUT : str, **perTagCount) -> None
```

A sample execution is written in [`driver.py`](./driver.py). Make sure you have the necessary files and folders.

```python
# driver.py
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
```

## Question Format

A question must have three header tags:

1. `# Question` : Anything after it is treated as the question part.
2. `# Answer` : Anything after it is treated as the answer part.
3. `# Tag` : Anything after it is treated as a tag.

Sample questions can be found under the `UCOLLECTION` folder. One is given next.

```markdown
# Question
This is a *Sample Question*, numbered **1**.\
Take a look at the following code,

```C 
#include <stdio.h>

int main(void)
{
    for(int i = 0; i < 10; i++)
    {
        printf("Hello World 1\n");
    }
    return 0;
}
```// Remove this comment in the real case

# Answer
This is answer to question 1.

# Tag
Easy
```
