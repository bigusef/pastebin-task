# Pastebin Poorject
this project will help user to share and save his snippets with other user or on public air on privet so he is the only one can see this paste

## Man Functions
i will list all project features and functions provided 

#### User Register
any user can resister with our site using unique username and password. when he register the system will create unique authentcation token and create empty profile for this user
he can login after that using username and password that he was choised before to login
after user login he can view and  complete his profile data and set his information
- first name
- last name
- gender
- birth date
and any user can signout and will delete his authentication token and when he want he can login again

#### Create Paste
any authenticated user or guest user can create new paste and take it's shorten url to get back to it. every paste will create user can determin if he want to show this paste in public or shear with his site register frind or not accesable by any one except him
every created paste have expiration option and include
- __Never__ on this option paste will never expire
- __Hour__ on this option paste will expire after an hour
- __Day__ on this option paste will expire after a day
- __Week__ on this option paste will expire after a week
- __Month__ on this option paste will expire after a month

when user create pastes with privacy option __Shared__ he can determin list of user to share thi pase with thim

#### Update and Delete Paste
only register active login user can update or delete his owne pastes and no one other can do that

#### See paste details
based on paste privacy and user auth the pate show and i will list all this cases:
- anonymous user can see only all public paste.
- authenticated user can see all public pastes.
- authenticated user can see all his owne privet pastes.
- authenticated user can see pastes that the owner of paste shared with him.

#### Filter pastes by date
any user can filter pastes by date using three querys
1. __date__ get all pastes created on this date
2. __lte__ get all pastes created less than or equal this date
3. __gte__ get all pastes created less grate or equal this date

#### List Pastes
i provide three API to list pastes
1. get all pastes user can be see based on paste show credential and his API available for both guest user and auth user
2. get public pastes return only public pastes and his API available for both guest user and auth user
3. get auth user pastes and this return all auth user pastes based on paste show credential and exclude public pastes

#### Super Admin Statistics
i provied way to let super admin and stauff aware about site statistics by introduce API to return CSV file contain all user date and statistic information
- username
- Email
- Full Name
- Total Pastes
- Available Pastes
- Unavailable Pastes 

and this statistic will be available for list of user or individual user


#### Helper methods
i create two helper methods
1. `code_generator` created to provide unique code pased on dynamic size and an instance search on instance model class if this code exist before or not and if it is not exist will return this code otherwise will genrate another code 
2. `csv_file_render` created to provide way to create `CSV` file and fill this file with date comes from context parameters and create file with header comes from headers parameters