source /home/itop/.bash_profile
WORKDIR=/home/itop/scripts/mycmdb/myproject/cmdb/etl
python3 $WORKDIR/ext_vc.py --host vc06
python3 $WORKDIR/ext_vc.py --host vc02
python3 $WORKDIR/ext_vc.py --host ppvc06