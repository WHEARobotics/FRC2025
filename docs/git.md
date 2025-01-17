# Normal workflow

* Pull any changes from the cloud GitHub repository.
* If there were changes to `pyproject.toml`, execute `robotpy sync` to get
  the latest wpilib, robotpy, etc. code, both for your computer and ready
  for when you deploy to a robot.
* Edit and test your code.
* When you have something working, even an intermediate step, make
  a commit.  
* At the end of a work session (or more often) push your commits.

TODO: add more detail.
TODO: talk about branching?


# Merge conflicts

Merge conflicts happen when two people have modified the same file at
the same time, and then both try to push to GitHub.  The first push
will succeed, but if the changes overlap, you get a merge conflict that
shows up like an error.

They are not the end of the world, but they are a little more work
because you need to decide which changes from each edit will be kept.
The best ways to avoid them are:
* Communicate with your teammates, coordinate to not overlap changes
  and let them know when you push changes.
* When you have working changes, commit and push.  Don't leave uncommitted
  changes on your computer for days.
* When you start working on something, pull from the repository before
  editing files.  