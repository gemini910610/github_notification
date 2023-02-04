# Github Notification
when someone makes a push or pull request to the repository, a discord notification will be sent to the channel or user
## How to use
1. clone this repository<br>
    ```
    git clone https://github.com/gemini910610/github_notification.git
    ```
2. delete .git folder and README.md
3. create your repository on github
4. go to Settings > Security > Secrets and variables > Actions, click "New repository secret" button
    * if you want to send notification to the channel<br>
       Name: WEBHOOK<br>
       Secret: discord channel webhook url
    * if you want to send notification to the user<br>
        Name: TOKEN<br>
        Secret: discord bot token
5. invite your bot to your discord server
    * if you want to send notification to the channel, you can skip this step
    * note: all users need to have a common server with the bot (users can be in different servers)
6. modify value in config.json
    * if you want to send notification to the channel<br>
      set mode to `"channel"`
    * if you want to send notification to the user<br>
      set mode to `"user"`<br>
      set user to list of user id
7. push to your repository
    ```
    git init
    git remote add origin <repository url>
    git add .github
    git commit -m "init"
    git push origin master
    ```
## config.json
### target
1. push<br>
  **default: `[]`**<br>
  list of specified branches<br>
  if the list is not empty, notifications will be sent only for push to branches in the list
2. pull_request<br>
  **default: `[]`**<br>
  list of specified branches<br>
  if the list is not empty, notifications will be sent only for pull request to branches in the list
* for example:<br>
  ```
  "target" : { "push" : ["master"], "pull_request" : [] }
  ```
  only push to master branch will send notification, and pull request to any branch will send notification
### mode<br>
**default: `"channel"`**<br>
define whether to send notifications to channel or user
### user<br>
**default: null**<br>
define the ids of the users to send the message to
## Help
### How to get channel webhook url
1. open "Edit Channel"
2. go to "Integrations" on the side menu
3. click "Create Webhook" button
4. click webhook
5. click "Copy Webhook URL" button
### How to get user id
1. open "User Settings"
2. go to "Advanced" on the side menu
3. enable "Developer Mode"
4. right click user's profile picture
5. click "Copy ID"
### How to get discord bot token
1. go to [`https://discord.com/developers/applications/`](https://discord.com/developers/applications/) and login with your discord account
2. click "New Application" button
3. go to "Bot" on the side menu
4. click "Add Bot" button
5. click "Reset Token" button
6. click "Copy" button
### How to invite bot to server
1. go to [`https://discord.com/developers/applications/`](https://discord.com/developers/applications/) and login with your discord account
2. go to "OAuth2" on the side menu
3. go to "URL Generator" on the side menu
4. select "bot" in "SCOPES"
5. select "Send Messages" in "BOT PERMISSIONS"
6. click "Copy" button in "GENERATED URL"
