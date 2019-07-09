gz_name="pubmed_parser.tar.gz"
tar --exclude=.git --exclude=$gz_name --exclude=data --exclude=venv -vzcf $gz_name ../$(basename `pwd`)/  
scp ./$gz_name app13:workspace/
#&& rm -r zeppelin-docker
ssh app13 "cd workspace  && tar -vzxf $gz_name && rm ./$gz_name"
rm ./$gz_name
