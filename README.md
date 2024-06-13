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
  <li>AJAX to update content without a page refresh</li>
</ul>

<h2>Contributing</h2>

<h3>Install</h3>

1. Install the required prequisites. If you want, install the recommended ones.

Required prequisite downloads:
- **Git**
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
- **SQLiteStudio** - See database contents and execute SQL for debugging

2. Clone the repository to your device

```sh
git clone https://github.com/zgstumpf/ratemyresume.git
```

3. Navigate into the new cloned directory

```sh
cd ratemyresume
```

4. Create the `.env` file

In the root project directory, create a file named `.env`. Copy the template from `docs` > `env.md` and paste into the `.env` file.

5. Build the Docker container (must have Docker Desktop open)
```sh
docker-compose up
```

<h3>Run locally for development</h3>

1. There are two `ratemyresume` directories. If you haven't already, `cd` into the outer `ratemyresume` directory so you are in the directory containing `manage.py`.

2. Run the Docker container (must have Docker Desktop open)
```sh
docker-compose up
```

4. In a browser of your choice, search [http://localhost:8000/](http://localhost:8000/).

Any changes you make to most files will automatically trigger page reloads. If you edit files in a `static` directory (CSS/JS files), you need to **manually** refresh the page to see the changes. Your browser may cache previous versions of a file to reduce refresh loading times, so if you don't see changes after refreshing, **hard reload**. Look up how to hard reload for your chosen browser. On Mac for Edge it is **command + shift + r**.

If you edit `models.py` to edit the database structure, you need to run some commands before the changes take place. To enter the commands in the same command line that is running the server, you need to first quit the server with **control + c**.

```sh
python manage.py makemigrations
python manage.py migrate
```

If you make any changes in the `.env` file, restart the server (quit the server and run `docker-compose up`) for your changes to take place.

When you are done developing, quit the Docker container with **control + c**.

<h4>Install Python package</h4>

Manually add the package to `environment.yaml` then run `docker-compose build`.

<h2>Developers</h2>

<ul>
  <li>Zach Stumpf</li>
</ul>
