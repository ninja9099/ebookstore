## project description

Fixtures to be loaded after project set-up
python manage.py loaddata category.json
python manage.py loaddata books.json
python manage.py dumpdata books.Category --indent=2 > apps/books/fixtures/category.json
python manage.py dumpdata books.Book --indent=2 > apps/books/fixtures/books.json