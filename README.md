# Instructions to run
- Put all json files whose schemas are to be sniffed in the ./data folder.
- cd to root of this project and run `python3 ./main.py

# Other details
- Generated schemas should be stored in the ./schema folder.
- The program has no dependencies.
- The program was tested on Python 3.10.6

# Dev phase
- Still riddled with bugs. There seems to be a RecursionError that prevents json dump.