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
- **Git** - version management
- **Anaconda** - Python environment and package manager

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

4. Use Anaconda to install project dependencies

```sh
conda create --name ratemyresume --file requirements.txt
```

<h3>Run locally for development</h3>

1. There are two `ratemyresume` directories. If you haven't already, `cd` into the outer `ratemyresume` directory.

2. Activate the conda environment

```sh
conda activate ratemyresume
```

(If you get `conda command not found`, restart the terminal and try again.)

3. Start the localhost server

```sh
python manage.py runserver
```

4. In a browser of your choice, search [http://127.0.0.1:8000/](http://127.0.0.1:8000/).

Any changes you make to most files will automatically trigger page reloads. If you edit files in a `static` directory (CSS/JS files), you need to **manually** refresh the page to see the changes. Your browser may cache previous versions of a file to reduce refresh loading times, so if you don't see changes after refreshing, **hard reload**. Look up how to hard reload for your chosen browser. On Mac for Edge it is **command + shift + r**.

If you edit `models.py` to edit the database structure, you need to run some commands before the changes take place. To enter the commands in the same command line that is running the server, you need to first quit the server with **control + c**.

```sh
python manage.py makemigrations
python manage.py migrate
```

When you are done developing, quit the server (**control + c**) and deactivate the conda environment.

```sh
conda deactivate
```


<h2>Developers</h2>

<ul>
  <li>Zach Stumpf</li>
</ul>
