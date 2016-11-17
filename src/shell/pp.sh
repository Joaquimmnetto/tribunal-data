for dir in `ls ../../dataset/*/ -d`
do
echo "Processing dir $dir"
python ../python/preprocessing.py $dir
done

