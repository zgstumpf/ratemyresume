<h1 align="center">Ratemyresume</h1>

<p align="center">Real people rate your resume</p>

<hr/>

<p>A website where you can upload your resume and get a rating from 0-10 from other users. Built with Django.</p>

<h2>Features</h2>

<ul>
  <li>User authentication</li>
  <li>File uploads</li>
  <li>Comment sections</li>
  <li>Create or join groups of users</li>
  <li>Invite users to your group and request to join a group</li>
  <li>Granular privacy controls for resumes</li>
  <li>Search functionality</li>
  <li>Responsive</li>
  <li>AJAX</li>
</ul>

<h2>Install</h2>

1. Install the required prequisites.

    Required prequisite downloads:
    - **Docker** - [Make an account](https://hub.docker.com/) and [download Docker Desktop](https://docs.docker.com/engine/install/)

    Recommended downloads:
    - **Visual Studio Code** - code editor
        - Recommended Extensions:
            - **CSS Peek** by Pranay Prakash
            - **Django Support** by Al Mahdi
            - **django-intellisense** by shamanu4
            - **GitLens - Git supercharged** by GitKraken
            - **Pylance** by Microsoft
            - **Python** by Microsoft
            - **Python Debugger** by Microsoft
    - **GitHub Desktop** - GUI for Git
    - **pgAdmin 4** - See database contents and execute SQL for debugging

1. Clone the repository to your device

    ```sh
    git clone https://github.com/zgstumpf/ratemyresume.git
    ```

1. Navigate into the new cloned directory

    ```sh
    cd ratemyresume
    ```

1. Create the `.env` file

    In the root project directory, create a file named `.env`. Copy the template from `docs` > `env.md` and paste into the `.env` file. You need to fill in the values for each key. Ask a team member for help, or retrieve the values from AWS.

1. Open Docker Desktop

1. Build the Docker container

    ```sh
    docker-compose up
    ```

<h2>Run locally for development</h2>

1. `cd` into the directory containing `manage.py`

1. Open Docker Desktop

1. Run `docker-compose up`

1. In a browser, search [http://localhost:8000/](http://localhost:8000/). (The terminal output may give a different URL - ignore it.)

Any changes you make to most files will automatically trigger page reloads. If you edit files in a `static` directory, you need to manually refresh the page to see the changes. If that doesn't work, **hard reload** the page.

If you edit `models.py` to edit the database structure, you need to run some commands before the changes take place. To enter the commands in the same command line that is running the server, you need to first quit the server with **control + c**.

```sh
python manage.py makemigrations
python manage.py migrate
```

If you make any changes in the `.env` file, restart the server (quit the server and run `docker-compose up`) for your changes to take place.

When you are done developing, quit the Docker container with **control + c**, or stop it in Docker Desktop.

<h3>Install Python package</h3>

1. Manually add the package name and version in `environment.yaml`
1. ```sh
    docker-compose build
    ```
