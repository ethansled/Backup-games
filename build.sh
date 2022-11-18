sd=$(pwd)

for f in $(ls)
do
    mkdir -p $sd/html/$f
    cd $f
    python -m pygbag --build --html main.py
    cp -r build/web/* $sd/html/$f/
    cd $sd
done
