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

## Over all tasks

1. Pull the SQLite database containing the tags to a local location and
   then extract the tags database in a form suitable for PlasTeX/Gerby.

   Really this should be run a program which obtains the tag database.
   This then allows different users to maintain their tag database using
   their own tool.

2. Run the independent tasks

3. Rsync the output to the Gerby-website location (should we build the
   Gerby-website database at this point?)

## Independent tasks

Each independent task does the following:

1. changes directory to a specified directory.

   - if this directory does not exist then it is cloned from the given
     git-url.

2. the git repository is pulled to be up to date.

3. the `lpilMagicRunner` is run on the given LaTeX file.

4. PlasTeX/Gerby is run on the result.

## Questions

### Tag database tool



### PlasTeX/Gerby document merging

**Q**: Can we plastex/gerby in multiple directories and then rsync the
       results together? OR do we have to rsync the parts together and
       then plastex/gerby the whole?

**A**: We would *rather* assemble the Gerby website "late", so that
       individual parts can be plastex/gerbied separately *and* *then*
       assembled into a whole. This *should* be facilitated by the tags
       which are unique across the "whole" exposition.

**Problems**:

  - the gerby runner assumes ONE paux file (which is a pickled python
    structure). This is however *only* used when loading a given
    document's list of tagged items

  - the footnote numbering will clash between plastex/gerby documents.
    Should we hack the Gerby plugin to allow external control of the
    sequences OR should we fix-this-up at the end (i.e. a
    compiler/linker)?

  - the image numbering will clash between plastex/gerby runs. Again
    should we hack the Gerby plugin to allow external control of the
    sequences OR should we fix-this-up at the end (i.e. a
    compiler/linker)?

  - the lemma/theorem/definitions as well as chapter/section numbers will
    have to be (re)set for each document at the LaTeX level. This *is*
    something we do want to manage.

    Fortunately the HTML cross links are based upon "tag/XXXX" instead of
    actual filenames, so no linker link patch-ups are needed.

**Solutions**:

  - we probably should take ownership of *our* version of the gerby runner
    (the existing gerby-website has hard references to Stack specific
    data). The question is how to do this as cleanly as possible....

  - we can then implement the "linker" in the actual gerby-website code
    itself. (EXCEPT the plastex/gerby output contains some hard references
    which will need to be altered on the fly (or when loaded into the
    database))