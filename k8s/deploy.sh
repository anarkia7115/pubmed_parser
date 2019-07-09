gz_name="pubmed-parser-k8s.tar.gz"
dest_dir="pubmed-parser-k8s"
#dest_dir="$(basename `pwd`)"
tar --exclude=.git --exclude=$gz_name -vzcf $gz_name ../$(basename `pwd`)/  
scp ./$gz_name app12:workspace/
rm $gz_name
ssh app12 "cd workspace  && mkdir -p $dest_dir && tar -C $dest_dir -vzxf $gz_name && rm $gz_name"
