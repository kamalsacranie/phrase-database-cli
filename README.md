# Jot

## What is it

I want this to be a ncurses-style TUI app which allows me to create different
tables in a datable to manage phrases I like/want to store.

## Plan

### Logistical needs

- CLI programme
- I should be able to create a table from anywhere and it should be created in
  either a user specified file, `$XDG_DATA_DIR`, or within the root directory of
  the project (I'm surely not going to force a creation in the home folder)
- Clearly I'm going to need a config (a yaml config maybe)

### Desired functionality

- Simply create tables in a user defined database and
  1. view those databases with a TUI
  1. using ncurses

## Problems

Unfortunately `urwid` is very unin**tui**tive^[Haha, TUI... like "terminal user
interface"]. I have found a viable alternative, `PyTermGUI`, but this does mean
learning another whole framework at 1am. Which, to be fair, I think I'm going to
do...^[Despite having my professional ACA exams in about a week-and-a-half.]
