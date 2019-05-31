# simple way
python tf_simulation.py FS-cell CONFIG1 -s --SEED 4 --tstop 10
python theoretical_tools.py -f data/FS-cell_CONFIG1.npy --With_Square
python tf_simulation.py RS-cell CONFIG1 -s --SEED 4 --tstop 10
python theoretical_tools.py -f data/RS-cell_CONFIG1.npy --With_Square
