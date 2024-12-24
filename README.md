# FRC2025
Code for 2025 season.

# Initializing environment

After you have cloned this repository, you will need to initialize the enironment. This will install the necessary dependencies for the project. 

Follow the instructions at [Installation.md](docs/Installation.md) to initialize the environment.

# Using Git

Git is used for "version control." Git is a programming's team "time machine". It allows you to go back in time to see what the code looked like at a certain point in time. It also allows you to see who made changes to the code and when.

Unlike, say, Google Docs and more like, say, Microsoft Word, the changes you make to the code on your machine are not automatically shared with the rest of the team. You have to "commit" your changes to the "repository" (the shared codebase) in order to take a snapshot. You then have to "push" all your recent commits to share them with other team members.

If you make a mistake, you can use Git to go back to a previous version of the code.

Always **start** a new programming session by running `git pull`. This will update your local copy of the code with any changes that other team members have made.

Commit your code **early and often**. Programmers will often make dozens of commits per day. 

- Just added a blank new file? Commit it.
- Just added a comment? Commit it.
- Just changed some logic? Commit it.
- Just tweaked some variables until the code worked? Commit it.
- Robot working as desired with your changes? **Absolutely** commit it
- **Before you go home for the day**:
  - Is the robot working? **Commit it**
  - Is the robot not working? This is the hard one. 
    - Is there **any** chance of someone else working on the robot code? **Commit it**. 
      - Your message should begin with "WIP" (Work In Progress). 
    - If you're the only one working on the robot code, you can wait. 

Pretty much the only time you **shouldn't** commit is when the code, if run on the robot, works worse than it did before. 

When you commit, add a brief descriptive message of what you did. For instance: 

- `Added new file SomeCommand.py for drive subsystem`
- `Added comments to SomeCommand.py`
- `Changed logic in SomeCommand.py to fix bug`
- `Tweaked variables in SomeCommand.py to improve performance`
- `Robot working with new command SomeCommand.py`

Git is a complex tool. If you don't know how to make a commit and add a message, **ask for help.** "Rolling back" changes (time traveling) can be difficult. If you aren't sure what to do, **ask for help**. 

If you ever receive a message about a "merge conflict", **ask for help**. 

