# The Hammer

Home to the work-in-progress known as The Hammer, _a discord bot_.

## Setup

Setup is rather quick and simple.

- Pull the repo down to wherever you would like

  ```bash
  git clone git@github.com:trjahnke/the_hammer.git
  ```

  or you can download whatever the latest release zip is [here](https://github.com/trjahnke/the_hammer/releases).

- You will need two environment variables:
  - The first of which is a bot token which has admin capabilities, this can be done through [Discord Developers Page](https://discord.com/login?redirect_to=%2Fdevelopers%2Fapplications)
  - You will also need a postgresql database URL. I have done this via Heroku as it to me is a quick and solid free option. [More Information](https://data.heroku.com)
- You will need some sort of virtual env container for the pips, I use `virtualenv`. You can use whatever method you would like as long as it is using Python3.6 and above.

  - With the virtual env install the requirements

  ```bash
   pip install -r requirements
  ```

- Now you can `export` your two variables as `BOT_KEY` and `DATABASE_URL`
- Once done you can now run:

  ```python
  python main.py
  ```

  Now you can run around and test it all out!

## To Do

- [ ] New custom help command with more information and design
  - [ ] Starting off [point](https://gist.github.com/StudioMFTechnologies/ad41bfd32b2379ccffe90b0e34128b8b)and [this](https://stackoverflow.com/questions/64092921/how-do-i-put-discord-py-help-command-in-an-embed)
- [ ] Add descriptions to all cogs
- [ ] Add a function for when someone enters or leaves the server
- [ ] Music cog feature
  - [ ] Ability to connect to more than one voice channel
  - [ ] Ability to have 24/7 channels along with user input music channel
- [ ] A leveling system
- [ ] A task loop that checks to make sure a user hasn't removed any of their roles and if so bot removes the member role and re-adds the newbie role
- [ ] User facing website too allow for toggles and management (probably in flask or django)
- [x] Fix concurrent database connections issues
- [ ] Hide load and unload functions
