#### Getting started using Docker:
`docker build -f docker/app/Dockerfile -t bookcamel:latest .`
`docker run --name bookcamel -d -p 5000:8000 bookcamel:latest`

You may also launch the "production" deployment using
`docker-compose -f docker/docker-compose.yaml up -d --build`

Currently the database **must** be populated manually

#### Getting started on Unix:

    Install:
      Python 2.7 (package)

    Run: (or run start.sh)
      # virtualenv --python=python2.7 nv
      # source nv/bin/activate
      # sudo pip install -r reqs.txt
      # ./cmd.py runserver

#### Getting started on Windows:

    Install:
      Download Python 2.7.*, link: https://www.python.org/downloads/
      Install in the default "C:\Python27" (or suffer custom startup commands)
    
    Run: (or run start.bat)
      # SET PATH=C:\Python27;C:\Python27\Lib;C:\Python27\DLLs;C:\Python27\Scripts
      # SET PYTHONPATH=C:\Python27;C:\Python27\Lib;C:\Python27\DLLs
      # SET PYTHONHOME=C:\Python27
      # pip install virtualenv
      # virtualenv-2.7 nv
      # nv\Scripts\activate.bat
      # pip install -r reqs.txt
      # python cmd.py runserver

#### Getting started on Mac OS:

    Install Python 2.7 with Easy Install
    - Open Terminal
    - sudo easy_install pip
    
    Run: (use Unix run instructions)

## Viewing the site:

    Open "http://localhost:5000" in your web browser

Initializing the database with filler content (model definitions):
This is automatically done in dev (default) environment

    On Unix: (in nv prompt)
      # ./cmd.py shell
      # db.create_all()
      Ctrl + D
    
    On Windows: (in nv prompt)
      # python .\cmd.py shell
      # db.create_all()
      Ctrl + C

#### Exiting the virtual environment:
`deactivate`
