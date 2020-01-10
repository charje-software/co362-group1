# Participants
This directory contains scripts for a realistic demo with real timings.

Each script runs an agent for a prediction market participant (e.g. a
household, person, organization, ...). These scripts should be run on a
VM e.g. using screen. Make sure that accounts given to the agents
correspond to accounts on Ganache.

Run the participants scripts like this:
```
python p1.py '2020-02-02 14:48:00' '2020-02-28 00:00:00' '30min'
```
In addition, run the `Oracle`:
```
python -m agents.oracle '2020-02-02 14:48:00' '2020-02-28 00:00:00' '30min'
```
The arguments are the actual start and end times and time intervals mapped to
the virtual time in the demo.
