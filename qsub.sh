## These are flags you must include - Two memory and one runtime.
## Runtime is either seconds or hours:min:sec
#
##$ -l tmem=1G
##$ -l h_vmem=1.5G
##$ -l h_rt=100000
##$ -pe smp 1
##$ -R y
##$ -wd /home/dristea/projects/Generic-MITLP
#
##These are optional flags but you probably want them in all jobs
#
##$ -S /bin/bash
##$ -j y
##$ -N benchmarkCycles
#
##The code you want to run now goes here.
#
#export PATH=/share/apps/python-3.9.5-shared/bin:$PATH
#export LD_LIBRARY_PATH=/share/apps/python-3.9.5-shared/lib:$LD_LIBRARY_PATH
#
cat /proc/cpuinfo
#lscpu
#sudo apt-get install libmpfr-dev libgmp3-dev python3-dev libmpc-dev


#python3 -m venv .venv
#source ./.venv/bin/activate

curl -o get-pip.py https://bootstrap.pypa.io/get-pip.py
python3 get-pip.py

python3 -m pip install -r requirements.txt
python3 -m pip install -e .
python3 benchmarks/benchmark_squarings.py