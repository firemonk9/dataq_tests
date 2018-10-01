

for file in '/Users/dhiraj/Documents/dataq/azkaban/azkaban-db/src/main/sql/create*' ; do
	cat $file >> `pwd`/postgres_setup.sql
done	