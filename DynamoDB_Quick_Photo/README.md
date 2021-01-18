# Methodology: Design and Implementation for a Mobil App
[AWS Tutorial](https://aws.amazon.com/getting-started/hands-on/design-a-database-for-a-mobile-app-with-dynamodb/4/)

## Data Model:
Application will have the following entities:
    - User
    - Photo
    - Reaction
    - Friendship
    
 A "User" can have many "Photos", and a "Photo" can have many "Reactions". Fianlly, the "Friendship" entity represents a many-to many relationship between "Users", as a "User"can follow multiple "Users" and be followed by multiple other "Users"
 
 ![alt text](https://d1.awsstatic.com/Projects/Module_2_Step_1.435e9196c954a037b9aaa5040e6ea5cba2656b47.png)
    
   ## Access Paterns:
   ### USER Access Patterns:
   The users of our mobile application will need to create user profiles. These profiles will include information such as a username, profile, picture, location, current status, and interest for a given user.
     
   Users will be able to browse the profile of other users. A user may want to browse the profile of another user to see if the user is interesting to follow or simply to read 
   background on an exisitng friend.
     
   Over time, a user will want to upade their profile to display a new status or to update their interest as they change.
     
   #### Based on this information, we have three access patterns:
   - Create user profile (Write)
   - Update user profile (Write)
   - Get user profile (Read)
      
   ### PHOTO Access Patterns:
   When users upload a photo, you will need to store information such as the time the photo was uploaded and the location of the file on your Content Delivery Network (CDN)
     
   When a users aren't uploading photos, they will want to browse photos of their friends. If they vist a friend's profile, they should see the photos for a user withh the          most recent photos showing first. If they really like a photo, they can 'react' to the photo using one of four predefined reactions --a heart, a smiley face, a thumbs up,        or a pair of sunglasses. Viewing a photo should display the current reactions for the photo.
     
   #### In this section, we have the following access pattern:
   - Upload photo for user (Write)
   - View recent photos for user (Read)
   - React to a photo (Write)
   - View photo and reactions (Read)
      
   ### FRIENDSHIP Access Patterns:
   In your application, a friendship is a one-way relationship, like Twitter. One user can choose to follow another user, and that user may choose to follow the user back.          For our application, we will call the users that follow a user "followers", and we will call the users that a user is following the "followed"
      
   #### Based on this information, we have the following access patterns:
   - Follow user (Write)
   - View followers for user (Read)
   - View followed for user (Read)
     
   ## Primary Key - Design
   Each user on your application will have a single user profile represented by "User" entity in your table.
   A "User" will have multiple photos represented in your application, and a photo will have multiple reactions. These are both one-to-many relationships.
   
   "Friendship" entity is a represenation of a many-to-many relationship as one user may follow multiple other users, and a user may have multiple followers.
   
   Having a many-to-many mapping is usually an indication that you will want to satisfy two query patterns, and our application is no exception.
   
   We will use a composite primary key with both a "HASH" and "RANGE" value. Because it's a one-to-one mapping, the acces pattern will be basic key-value lookup. Since your table design requires a "RANGE" property, you can provide a filler value for "RANGE" key.
