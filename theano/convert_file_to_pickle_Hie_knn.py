import codecs
import six.moves.cPickle as pickle
import os
import sys
import numpy

def convert_pickle_format(data_path):
    data_dir, data_file = os.path.split(data_path)
    if data_dir == "" and not os.path.isfile(data_path):
        new_path = os.path.join(
            os.path.split(__file__)[0],
            "data",
            data_path
        )
        if os.path.isfile(new_path):
            data_path = new_path

    print('......loading data')
    pickle_path = os.path.join(
            os.path.split(__file__)[0],
            "data",
            "samples3"
        )
    # open the file for writing
    fileObject = open(pickle_path, 'wb')

    # open the input datafile and read the data
    # write the data into the file
    f = codecs.open(data_path, 'rU')
    list1 = []
    for line in f:
    	mylist = line.split()
        mylist1 = map(lambda x: int(x), mylist)
        list1.append(mylist1)
    myarray = numpy.array(list1)

    pickle.dump(myarray, fileObject)
    # close the file
    fileObject.close()
    f.close()

if __name__ == "__main__":
	convert_pickle_format("sample3.txt")
