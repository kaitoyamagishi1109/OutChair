# OutChair v2
BUJSA Attendance Software

Copywrite 2019, Kaito Yamagishi, all rights reserved

## Updated Documentation as of January 2020:
*Version 2.0.0*

After operating with the OutChair program for a semester with my student organization, various problems with the app surfaced:
1. Other users cannot operate the app because of its dependency on multiple python libraries (No packaging was done)
2. Since there is only one swiper, the swipe-in attendance process is very inefficient
3. Swiper operation is hardware-dependent, so people swipe the wrong way, forgets their student ID, etc. : This lead to some of the attendances to be manually entered every meeting

Because I was so focused on the "swiper" aspect and making the hardware-software sync work, I didn't see some integral frauds related to the format of this application. Therefore, I am going to make some drastic changes to this program, including but not limited to:
1. A GitHub pages based web application
2. Google Sign-In widget for user identification
3. Simple and more efficient way to sign-in to meetings

I hope that these changes can not only create a more efficient system for the organization, but also to be a prime example of software engineering improvement.

## Original Documentation as of July 2019:
*Version 1.0.0*

This is an attendance software which has features corresponding to the google sheets API and the slack API.
Specifically, you can use a USB card swiper in order to fill in their attendance status to a google spreadsheet,
and to notify them via a slack API bot. Although many parts are hardcoded such as the swiper input and the slack API bot settings,
the code itself should be pretty straightfoward, with the help of detailed comments. Once the program is more solidified,
there will be a detailed description on how to get this up and running for your organization.

This version ran on my local environment, which made it very inflexible. (It was my first project!) The legacy of this version can be found in the OutChair.py file.
