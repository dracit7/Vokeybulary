
"""Defines the function which prints help information
"""

def helper(command = ""):

  if command == "":
    print('''

Usage: COMMAND [ARGUMENTS]

A simple k-v storage app for memorizing.
Base k-v structure: `key` -> list of (`name`, list of `description`)

Commands:
  find/f          Find a key-values pair by a certain key
  findval/fv      Find a certain value by its name and show its appearances in the database
  add/a           Add a value to a key's value-list or add a description to a value's desc-list
  delete/del/d    Delete a key/value/description
  list/ls/l       List all existing k-v pairs, or something defined by ARGUMENTS
  set/s           Set something defined by ARGUMENTS
  test/t          Pick a key-values pair at random and generate a simple test based on it
  history/hist/h  Modify and re-execute a command in command-history
  help            Display help information
  exit/quit/q     Exit this program

Run `help COMMAND` for more information on a command.
''')

  elif command == "find" or command == "f":
    print('''
Usage: find KEY

Find a key-values pair by a certain key. KEY should be the name of that key.

Example:

```
>> find programmingLang

Values corresponding to <programmingLang> are:
  <C>
    C is a general-purpose, procedural computer programming language.
    Originally developed at Bell Labs by Dennis Ritchie between 1972 and 1973.
  <Python>
    Python is an interpreted, high-level, general-purpose programming language.
    Created by Guido van Rossum and first released in 1991.
  <Java>
    Write once, debug everywhere.
  <Golang>
    Go is an language that makes it easy to build simple, reliable, and efficient software.
  <C++>
    What a "A w e s o m e" language.
  <Javascript>
    "I HAVE NOTHING TO DO WITH JAVA!"
```
''')

  elif command == "findval" or command == "fv":
    print('''
Usage: findval VALUE
    
Find a certain value by its name(VALUE) and show its appearances in the database.

Example:

```
>> findval python

There are 2 hits in database:

In <programmingLang>:
  Python is an interpreted, high-level, general-purpose programming language.
  Created by Guido van Rossum and first released in 1991.
In <Dictionary>:
  [Noun] a large heavy-bodied nonvenomous constrictor snake
```
''')

  elif command == "add" or command == "a":
    print('''
Usage: add KEY VALUE [DESCRIPTION]    

Add a value to a key's value-list or add a description to a value's desc-list.

Example:

```
>> add samplekey samplevalue

Succeed

>> find samplekey

Values corresponding to <samplekey> are:
  <samplevalue>
    No description yet

>> add samplekey samplevalue sampledesc

Succeed

>> find samplekey

Values corresponding to <samplekey> are:
  <samplevalue>
    sampledesc
```
''')

  elif command == "delete" or command == "del" or command == "d":
    print('''
Usage: delete KEY [VALUE] [SERIAL]

Delete a key/value/description.

`delete KEY` deletes an existing key; `delete KEY VALUE` deletes a value
in KEY's value-list(and KEY would be deleted if there is no value left
in its value-list); `delete KEY VALUE SERIAL` deletes the SERIALth(start
by 0) description of VALUE.
''')

  elif command == "list" or command == "ls" or command == "l":
    print('''
Usage: list [OPTION]

List all existing k-v pairs, or something defined by OPTION.

OPTION could be:
- history/hist/h: list all operation histories
''')

  elif command == "test" or command == "t":
    print('''
Usage: test

Pick a key-values pair at random and generate a simple test based on it.
If you want to quit the test, just input 'quit'.

Example:

```
>> test

Key: <programmingLang>
Can you remember its values? There are 6 values in all.

('v') C
Correct!
('v') HTML
Missed.
(>_<) Golang 
Correct!
('v') Markdown
Missed.
(>_<) quit
That's fine. here're answers...

  You have tried 4 times
  2 of them are correct.

  <C>
    C is a general-purpose, procedural computer programming language.
    Originally developed at Bell Labs by Dennis Ritchie between 1972 and 1973.
  <Python>
    Python is an interpreted, high-level, general-purpose programming language.
    Created by Guido van Rossum and first released in 1991.
  <Java>
    Write once, debug everywhere.
  <Golang>
    Go is an language that makes it easy to build simple, reliable, and efficient software.
  <C++>
    What a "A w e s o m e" language.
  <Javascript>
    "I HAVE NOTHING TO DO WITH JAVA!"
```
''')

  elif command == "history" or command == "hist" or command == "h":
    print('''
Usage: history <PART OF COMMAND>

Pick the previous command you executed out, modify its last `x` arguments
to <PART OF COMMAND>(where `x` is the length of <PART OF COMMAND> in words)
and execute this new command.

It's possible to use `h2`, `h3` or commands like that to execute older commands
as well.

**Cautious**: some commands would **not** be recorded. Like:
- `history` itself
- wrong commands(not failed, but with wrong syntax)
- commands like `list`, `help`

Example:

```
>> find testing     

Values corresponding to <testing> are:
  <test>
    example!
    example2!

>> list history

History 3: add testing test
History 2: av test example!
History 1: find testing

>> history testing

Hist-operation: find testing 

Values corresponding to <testing> are:
  <test>
    example!
    example2!

>> h2 example3!

Hist-operation: av test example3! 

Succeed

>> h3 testb

Hist-operation: add testing testb 

Succeed

>> h2 testb example!

Hist-operation: av testb example! 

Succeed

>> history testing

Hist-operation: find testing 

Values corresponding to <testing> are:
  <test>
    example!
    example2!
    example3!
  <testb>
    example!
```
''')

  else:
    print("No information about this command.")

if __name__ == "__main__":
  helper()