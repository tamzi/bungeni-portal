wget ftp://ftp.cs.tu-berlin.de/pub/misc/postgresql/v8.3.4/postgresql-8.3.4.tar.bz2
tar xvf postgresql-8.3.4.tar.bz2
cd postgresql-8.3.4
./configure --prefix=/home/undesa/disk1/postgres --enable-thread-safety --with-readline
make && make install

