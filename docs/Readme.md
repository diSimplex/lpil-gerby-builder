# Design of the LPiL LaTeX Gerby builder

To build a LPiL LaTeX based Gerby website, we have a number of independent
tasks followed by a single run of the `plastex` tool. This means that we
can use the Python `asyncio` library to "parallelize" the independent
tasks.

## Problems

- We want to run independent tasks and keep the output "intelligible".

- We also want a "summary" of progress. Since the independent tasks
  consist of many sub-tasks each of which can be lengthy, we do need some
  sort of progress reporting.

- We could use `cfdoit` with its associated collector, *but* we also want
  to run these tasks from both `VSCodium` as well as `cron`.

This suggests:

- We run each command with pipes which can look for a "progress marker" in
  the output stream.

  The full log gets saved to a file in a well know place, but one where
  the output can be cleaned up regularly.

  The progress markers trigger a summary line, which is reported to the
  user, denoting the progress of each independent task. This summary
  should include whether or not a sub-task failed.

- To run the independent tasks, we have a "task queue" and a (small) pool
  of task runners. Each task runner takes a single task from the task
  queue and runs it. Each task runner returns if the task queue is empty.

  The main "thread" fills the task queue, starts the task runner pool and
  waits for all tasks runners to return. The main "thread" then runs
  plastex. Before running plastex, the main thread refreshes the tag
  database.


## New tools

We need:

1. a simple tool which refreshes a (PlasTeX/Gerby) tag database

2. a simple tool which pulls all parts of a plastex document into "one
   place". (IS THIS A SEPARATE TOOL?)

## Independent tasks

Each independent task does the following:

1. changes directory to a specified directory

   - if this directory does not exist then it is cloned from the given
     git-url.

2. the git repository is pulled to be up to date

3. the `lpilMagicRunner` is run on the given LaTeX file

## Questions

Can we plastex/gerby in multiple directories and then rsync the results
together?

OR do we have to rsync the parts together and then plastex/gerby the
whole?

