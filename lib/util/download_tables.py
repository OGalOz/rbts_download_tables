

import logging, os
import random, string

def download_table_from_ref_to_dir(ref, ret_dp, dfu):
    """
    Args:
        ref (str): ID of object within KBase, looks like 'A/B/C'
                    where A, B, and C are integers
        ret_dp (str): Path to directory where we place
                    the downloaded tables
        dfu (Object): DataFileUtil Object
    """
    GetObjectsParams = {
            'object_refs': [ref]
            }
    
    ResultantData = dfu.get_objects(GetObjectsParams)['data'][0]['data']
    logging.info(f"Resultant data for ref {ref}:")
    logging.info(ResultantData)
    
    if "file_type" not in ResultantData:
        raise Exception("Expecting file_type to be in data object, won't download.")
    if "file_name" not in ResultantData:
        logging.warning("Expecting file_name to be in data object, creating random name.")
        op_file_name = create_random_string(6) + ".tsv"
    else:
        original_file_name = ResultantData["file_name"]
        if "." in original_file_name:
            op_file_name = original_file_name.split(".")[0]
        else:
            op_file_name = original_file_name

    ft = ResultantData["file_type"]
    if ft == "KBaseRBTnSeq.RBTS_PoolFile":
        op_file_name += ".pool"
        KB_fh = ResultantData["poolfile"] 
    elif ft == "KBaseRBTnSeq.RBTS_InputGenesTable":
        op_file_name = ref.replace("/","_") + "_" + op_file_name + ".GC" 
        KB_fh = ResultantData["input_genes_table"] 
    elif ft == "KBaseRBTnSeq.RBTS_PoolCount":
        op_file_name += ".poolcount"
        KB_fh = ResultantData["poolcount"] 
    elif ft == "KBaseRBTnSeq.RBTS_ExperimentsTable":
        op_file_name += ".experiments.tsv"
        KB_fh = ResultantData["expsfile"] 
    else:
        raise Exception(f"Cannot recognize filetype: {ft}")
    
    # If there is a duplicate
    if op_file_name in os.listdir(ret_dp):
        logging.warning(f"File name {op_file_name} already in output directory, creating random name.")
        op_file_name = create_random_string(8) + ".tsv"
    # Output filepath
    op_fp = os.path.join(ret_dp, op_file_name)

    # Set params for shock to file
    ShockToFileParams = {
            "handle_id": KB_fh,
            "file_path": op_fp, 
            "unpack": "uncompress"
            }
    ShockToFileOutput = dfu.shock_to_file(ShockToFileParams)
    logging.info(ShockToFileOutput)
    
    logging.info(f"Downloaded file for ref {ref}")




def create_random_string(length):
    # length should be int
    return ''.join([random.choice(string.ascii_lowercase) for i in range(length)])



# Gets poolfile path
def download_poolfile(poolfile_ref, poolfile_path, dfu):

    GetObjectsParams = {
            'object_refs': [poolfile_ref]
            }

    # We get the handle id
    PoolFileObjectData = dfu.get_objects(GetObjectsParams)['data'][0]['data']
    logging.info("DFU Pool File Get objects results:")
    logging.info(PoolFileObjectData)

    poolfile_handle = PoolFileObjectData['poolfile']

    # Set params for shock to file
    ShockToFileParams = {
            "handle_id": poolfile_handle,
            "file_path": poolfile_path,
            "unpack": "uncompress"
            }
    ShockToFileOutput = dfu.shock_to_file(ShockToFileParams)
    logging.info(ShockToFileOutput)
    # Poolfile is at location "poolfile_path"

    return None 
