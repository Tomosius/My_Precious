# My Precious

## Introduction

"My Precious" is an innovative online platform designed to reconnect individuals with their lost valuables. Understanding the distress and frustration of losing personal items, My mission was to create a community-driven space where users can post about lost or found items, facilitating the joyful reunion of people with their belongings. Whether it's a key fob or a cherished heirloom, "My Precious" stands as a beacon of hope and solidarity.

## User Experience and Design

### Strategy

**Site Aims**: "My Precious" caters to anyone who has lost or found an item, emphasizing the power of community assistance. It's about transforming despair into joy, one post at a time. By fostering connections, we not only return lost items but also have the potential to forge lasting friendships.

### Execution

**Project Milestones**:

1. **Project Setup**: Establish the foundational structure, including initial app creation, database setup, GitHub repository, and Heroku deployment.
2. **User Authentication**: Implement secure login mechanisms and personal profile management.
3. **CRUD for Posts**: Enable users to create, read, update, and delete posts about lost and found items.
4. **Messaging System**: Facilitate user communication through direct messages.
5. **User-Friendly Design**: Prioritize intuitive navigation and layout design for an optimal user experience.
6. **Final Deployment**: Ensure a bug-free launch with full access to all project features.

### User Stories

- Authentication: Users can log in, authenticate, and log out.
- Profile Management: Users can update their profiles and add personal images.
- Post Interaction: Users have full control over creating and managing their posts, including adding photos and locations.
- Community Engagement: Authenticated users can view, search, and interact with posts and profiles of other users.
- Direct Messaging: Users can communicate privately through the built-in messaging system.

## App Structure

"My Precious" is built around three core applications:

1. **Users**: Manages user authentication and profiles.
2. **Posts**: Handles the creation and management of lost and found posts.
3. **Conversations**: Facilitates user-to-user messaging.

### Project was created based on Agile:

#### Milestones

1. Project Setup (This is the most important part):
    * Create Fist app, setup database, create repository on GitHub and ofcourse deploy to Heroku, just to make sure all
      is working.
2. User Login and Authentication:
    * Allow user to login and be authenticated on website, what will open all content of project
    * User can update add more personal information to profile
3. Posts:
    * Includes all features of CRUD
4. Messages:
    * Users can communicate through messages
5. UX:
    * Layouts are designed to be easy to understand and navigate through website
6. Final Deployment:
    * Project is completed with no errors and users are able to access al project features

#### User Stories:
1. User can log in, be authenticated and Logout
   * User can log in
   * user is authenticated
   * User can log out
2. User can access personal profile and update it
   * User can add additional information to profile
   * User can add personal Photo/Image to Profile
3. User can create a post
   * User can create a post
   * User can update a post
   * User can add photos to post
   * User can add location to post
   * User can delete post
4. User can access other users posts
   * Only authenticated users can see posts details
5. User can search for specific post
   * User can Search Posts
   * User can filtrate posts
6. Users can communicate - messaging
   * User can send a message
   * User can receive a message
7. Users can access/see other user profile, and see posts made by that specific user
   * Only authenticated users can see profile details

## Website / App structure
All Project is made out of only 3 apps:
1. Users
2. Posts
3. Conversations
![](/Users/pecukevicius/PycharmProjects/My_Precious/staticfiles/assets/images/database_structuee.png "database structure")
### Users:
1. Users App is made of 2 tables:
   * Auth User - This is Default Django model, I could, but I did not want to implement more fields to model, I left it as it is, simple and reliable Django built in Model for Authentication
   * Profile - This table is linked to Auth-User as 1-to-1 relationship:
     * This allows me to add as many fields as I want to user Profile
     * Do not have to touch Django build in User model for Authentication
     * If needed (for this project I did not see need), one user can have multiple Profiles. Just change relationship as 1-to-many
     * And most important 0- scalability. In such existing structure, App can be very fast, easy to create as many fields in profile, and light on database
   • Photo - Profile picture, linked to Profile with 1-to-1 relationship
2. Posts App consists of several tables:
   * Posts - This is Polymorphic Model. Yes, I had to use it, as initially (start of project) I wanted to implement DRY coding and used standard model Post as abstract, and then create 2 models based on it:
     * Lost Post
     * Found Post
     * Photos - Lost and Found posts have sub tables of Photos
     
Smart Explanation why I had to switch from Abstract model to Polymorphic:

All is because of search Field!

In standard model I can search Lost Posts, I can search Found posts, I can search both. But if I search 2 tables, and then I want to paginate it - it becomes complicated, this is where polymorphic model comes in.

3. Conversations consists of 2 tables:
    * Conversations - This is where one conversation can have as many participants as it is needed
    * Messages - this is just simple message linked to conversation and sender

Each app was built with intention of future re-usability, so they are pretty much independent:
1. They have their own templates in app/templates folder
2. They have their own urls in app/urls.py, these urls are imported to project urls.

## Tools and Technologies:
1. Tools:
* Pycharm - as Coding IDE
* Git - Source control
2. Services:
* GitHub - Source code hosting and source control
* Heroku - Django Deployment
* Cloudinary  Images hosting
* Elephant SQL - Database hosting
* Google Maps API - to show post location on maps
3. Languages:
* HTML - Used for static HTML files and templates
* Bootstrap5 and custom styles.css - layouts styling
* Javascript - page interactivity and dynamic content management
* Python - main language of project
* Django - Python framework
* Some Jquery/Ajax - some pages required some background interactions to database, so I adapted code snippets from internet for my project
* SQL - database queries 
    


   


## Navigation Menu
### Navigation is divided into 3 parts:
#### Big Screen:
* Top Navigation has fields:
  * ![big_screen_top_nav.png](staticfiles%2Fassets%2Fimages%2Fbig_screen_top_nav.png)
  * Branding - My precious, navigates to home page
  * Search field
  * Home Button
  * Users - All Users List
  * Create a post
  * Account:
    * ![big_screen_top_nav_dropdown.png](staticfiles%2Fassets%2Fimages%2Fbig_screen_top_nav_dropdown.png)
    * User Messages
    * Create a post
    * User Profile
    * Update Profile
    * Log Out
* Bottom Navigation:
  * ![big_screen_bottom_nav.png](staticfiles%2Fassets%2Fimages%2Fbig_screen_bottom_nav.png)
  * Branding with Year
  * Link to Source Code
  * Link to Linked In
#### Medium Screen:
* Top Navigation:
  * ![med_screen_top_nav.png](staticfiles%2Fassets%2Fimages%2Fmed_screen_top_nav.png)
  * Branding
  * Search button
  * Drop Down menu:
    * ![med_screen_top_nav_dropdown.png](staticfiles%2Fassets%2Fimages%2Fmed_screen_top_nav_dropdown.png)
    * Home
    * Users - List of users
    * Create a post
    * Account - drop down
      * ![med_screen_top_nav_acc_dropdown.png](staticfiles%2Fassets%2Fimages%2Fmed_screen_top_nav_acc_dropdown.png):
      * Messages
      * Create A post
      * User Profile
      * Update Profile
      * Log Out
* Bottom Navigation - Same as on Big Screen
#### Small screen Navigation:
* Top Navigation:
![small_screen_top_nav.png](staticfiles%2Fassets%2Fimages%2Fsmall_screen_top_nav.png)
  * Branding
  * Search Field
* Bottom Navigation:
![small_screen_bottom_nav.png](staticfiles%2Fassets%2Fimages%2Fsmall_screen_bottom_nav.png)
  * Home Button
  * Messages
  * Account Icon:
  * ![small_screen_bottom_account_dropdown.png](staticfiles%2Fassets%2Fimages%2Fsmall_screen_bottom_account_dropdown.png)
    * Create A post
    * User List
    * Profile
    * Update Profile
    * Log Out
  * Question Mark drop down:
  ![small_screen_bottom_links_dropdown.png](staticfiles%2Fassets%2Fimages%2Fsmall_screen_bottom_links_dropdown.png)
  * Link to Source Code
  * Link to Linked In
### 
  
