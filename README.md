Description of the approach

1. 
The task requires to print the log entries on a blog. 
Two main features are taken into account:
  - For each new entry, the code must check if an active session exists.
  - Once the information stops, all sessions are closed in order of arrival.
These two points where the main conditionings on the data structure used to store active sessions.
  - Because I had to perform a search for every new data stream (existing active sessions), I chose to store the data in an ordered dictionary called new_dict
  - This dictionary takes a key (ip) and outputs an item with an list containing time and vistits information.
  - Because the data needs to be printed in order at the end, I used an Ordered Dictionary data structure from python. Hence I get the same functionalities and advantages of a regular dict, while keeping the data stored in order. Hence, at the end I just need to loop over the dictionary to print the active sessions.

2. 
Besides that, the code only implements a separate function addline, which determines wether a session has expired 
and prints the corresponding line.

3.
It is important to note that the main feature speeding out the code was the fact that there is no need to check for clossed
sessions on every pull, but only when some time has advanced. This feature has been implemented via the Previous time (PrevTime)
and Current time (CurrTime) variables. Ideally, not only should the time have changed, but also we should only check for 
new sessions if the inactivity period has passed. This would reduce the number of searches. Unfortunately I had not time 
to add this feature.

4. 
Since every entry was counted as a different request (regardless of the document or website accessed), I did not find/need
the values of cik, acc, ext. I may have missed something when reading the challenge.

5. 
On a large file of 2.5 GB downloaded directly from EDGAR, the code takes around 320 sec to process 23 million entries. I could not add this test on GitHub

6. 
Packages used.
datetime (to add and substract time stamps)
OredredDict from collections, 
islice from itertools (to partially read the first two lines of the file)
sys (to read bash arguments)
