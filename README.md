# Project description

## Hosting
      Using pythonanywhere
      URL: http://pythonninja9099.pythonanywhere.com
      admin: http://pythonninja9099.pythonanywhere.com/admin/
      username: admin
      password: p@ssword
      Note: Login to first admin tod see the protected endpoints in swagger
      swagger Link: http://pythonninja9099.pythonanywhere.com/swagger-ui/

### Fixtures to be loaded after project setup
        python manage.py loaddata category.json
        python manage.py loaddata books.json

### Dump data to fixture files
        python manage.py dumpdata books.Category --indent=2 > apps/books/fixtures/category.json
        python manage.py dumpdata books.Book --indent=2 > apps/books/fixtures/books.json
       
## front-end Application:
   Ignore the current homepage
   Only template has been integrated
   Thanks @Vitor Fraietas for the wonderful Opportunity.
   following zen of python(https://simpleisbetterthancomplex.com) since I have started coding 