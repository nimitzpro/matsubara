import h5py

filename = "data/msd_summary_file.h5"

h5 = h5py.File(filename,'r')

print(list(h5.keys()))
musicbrainz = h5['musicbrainz']  # also metadata, analysis
print(list(musicbrainz))
h5.close()