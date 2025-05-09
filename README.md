# add project name here  <img src='https://21centuryweather.org.au/wp-content/uploads/Hackathon-Image-WCRP-Positive-1536x736.jpg' align="right" height="139" />

Project description, please include the main idea and questions that motivate the project.


**Project leads:** name, affiliation/github username

**Project members:** name, affiliation/github username

**Collaborators:** list here other collaborators to the project.

**Data:**
* Name, link
* Name, link

## Contributing Guidelines

> The group will decide how to work as a team. This is only an example. 

This section outlines the guidelines to ensure everyone can work and collaborate. All project members have write access to this repository, to avoid overlapping and merge issues make sure you discuss the plan and any changes to existing code or analysis.

### Project organisation

All tasks and activities will be managed through GitHub Issues. While most discussions will take place face-to-face, it is important to document the main ideas and decisions on an issue. Issues will be assigned to one or more people and classified using labels. If you want to work on an issue, comment and make sure is assigned to you to avoid overlapping. If you find a problem in the code or a new task, you can open an issue. 

### How to collaborate

* **Main branch:** We want to keep things simple, if you are working on a notebook alone you can push changes to the main branch. Make sure to 1) only add and ccommit that file and nothing else, 2) pull from the remote repo and 3) push.

* **Working on a branch:** if you want to fix or propose a change to someone else code you will need to create a branch and open a pull request. Make sure you explain your suggestion in the pull request message. **This also applies to collaborators outside the project team.**

### Repository structure

This is how the project should look like but make sure to change the name `template-hackathon-project` to something meaningful. 

```bash
template-hackathon-project/
├── LICENCE
├── README.md
├── template_project_hackathon
│   ├── analysis.py
│   ├── __init__.py
│   └── read.py
└── tests
    ├── test_analysis.py
    └── test_read.py
```
* `template_hackathon_project/` this folder will include the code to analysis the data.
* `tests/` this folder contains test code that verifies that your code does what it should.

