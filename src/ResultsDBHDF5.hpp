/*  _______________________________________________________________________

    DAKOTA: Design Analysis Kit for Optimization and Terascale Applications
    Copyright (c) 2010, Sandia National Laboratories.
    This software is distributed under the GNU Lesser General Public License.
    For more information, see the README file in the top Dakota directory.
    _______________________________________________________________________ */

//- Class:        ResultsDBHDF5
//- Description:  Class for interfacing to HDF5 results database in/out of core
//- Owner:        Brian Adams
//- Version: $Id:$

#ifndef DAKOTA_RESULTS_DB_HDF5_H
#define DAKOTA_RESULTS_DB_HDF5_H

#include "dakota_global_defs.hpp"
#include "dakota_results_types.hpp"
#include "BinaryIO_Helper.hpp"
#include <boost/scoped_ptr.hpp>
#include <boost/lexical_cast.hpp>
#include <boost/algorithm/string.hpp>

namespace Dakota {


class ResultsDBHDF5
{

public:

  ResultsDBHDF5(bool in_core, const String& base_filename):
    hdf5Stream(new HDF5BinaryStream(base_filename + 
				    (in_core ? ".tmp.h5" : ".h5"), 
				    in_core, false)
	       )
  { 

  }

  /// insert a RealMatrix with metadata
  template<typename StoredType>
  void insert(const StrStrSizet& iterator_id,
	      const std::string& data_name,
	      const StoredType& stored_data,
	      const MetaDataType metadata=  MetaDataType()) 
  {
    hdf5Stream->store_data(dataset_name(iterator_id, data_name),
			   stored_data);
  }

 
  /// allocate an entry with sized array of the StoredType, e.g.,
  /// array across response functions or optimization results sets
  template<typename StoredType>
  void array_allocate(const StrStrSizet& iterator_id,
		      const std::string& data_name, size_t array_size,
		      const MetaDataType& metadata)
  {
    // TODO: consider whether alloc should be no-op in this case,
    // otherwise perhaps it should use array_size and maybe even a
    // non-default constructed StoredType
    //StoredType initial_entry;
    std::vector<StoredType> initial_array(array_size, StoredType());
    //initial_array[0] = initial_entry;

    hdf5Stream->store_data(dataset_name(iterator_id, data_name),
			   initial_array);
  }
 
  template<typename StoredType>
  void array_insert(const StrStrSizet& iterator_id,
		    const std::string& data_name, size_t index,
		    const StoredType& stored_data)
  {
    // TODO: store at index specified...
    // BUT, for now, just to get some data written, ignore the index

    hdf5Stream->store_data(dataset_name(iterator_id, data_name),
     			   stored_data);
  }


private:

  /// Create a dataset name from the unique identifiers passed
  String dataset_name(const StrStrSizet& iterator_id, const String& data_name)
  {
    const String& method_name = iterator_id.get<0>();
    String method_id = iterator_id.get<1>();
    const size_t& exec_num = iterator_id.get<2>();

    if (method_id.empty())
      method_id = "anonymous";

    String data_name_wospace(data_name);
    //    boost::replace_all(data_name_wospace, " ", ":");
    //boost::erase_all(data_name_wospace, " ");

    return '/' + method_name + '/' + method_id + '/' + 
      boost::lexical_cast<String>(exec_num) + '/' + data_name_wospace;
  }

  /// BMA TODO: would prefer not to have a pointer, but no way to
  /// default construct an output handler
  boost::scoped_ptr<HDF5BinaryStream> hdf5Stream;


};


}  // namespace Dakota

#endif //  DAKOTA_RESULTS_DB_HDF5_H