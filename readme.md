This repository contains examples from django related blog posts on http://timmyomahony.com

To set it up as a working repository (with django 1.6):

    mkvirtualenv django-blog-examples --no-site-packages
    workon django-blog-examples
    cdvirtualenv
    pip install django
    git clone https:// blog_examples
    cd blog_examples
    pip install -r requirements.txt
    python manage.py syncdb
    python manage.py migrate
    python manage.py runserver
