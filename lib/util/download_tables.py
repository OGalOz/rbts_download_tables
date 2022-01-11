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
    GetObjectsParams = {"object_refs": [ref]}

    getObjectsResults = dfu.get_objects(GetObjectsParams)
    obj_info = getObjectsResults["data"][0]["info"]
    ft = parse_file_type(obj_info[2]) 
    logging.info("Caught file type: " + ft)
    ResultantData = getObjectsResults["data"][0]["data"]
    logging.info(f"Resultant data for ref {ref}:")
    logging.info(ResultantData)

    op_file_name = None
    '''
    if "file_type" not in ResultantData:
        raise Exception("Expecting file_type to be in data object, won't download.")
    '''
    if "file_name" not in ResultantData:
        if "fitness_file_name" not in ResultantData:
            logging.warning(
                "Expecting file_name to be in data object, creating random name."
            )
            op_file_name = create_random_string(6) + ".tsv"
    else:
        original_file_name = ResultantData["file_name"]
        if "." in original_file_name:
            op_file_name = original_file_name.split(".")[0]
        else:
            op_file_name = original_file_name

    op_fns = []
    #ft = ResultantData["version"]
    if ft == "KBaseRBTnSeq.RBTS_MutantPool":
        op_file_name += ".pool"
        op_fns.append(op_file_name)
        KB_fh_list = [ResultantData["mutantpool"]]
    elif ft == "KBaseRBTnSeq.RBTS_BarcodeCount":
        op_file_name += ".poolcount"
        op_fns.append(op_file_name)
        KB_fh_list = [ResultantData["barcodecount"]]
    elif ft == "KBaseRBTnSeq.RBTS_ExperimentsTable":
        op_file_name += ".experiments.tsv"
        op_fns.append(op_file_name)
        KB_fh_list = [ResultantData["expsfile"]]
    elif ft == "KBaseRBTnSeq.RBTS_Gene_Fitness_T_Matrix":
        fit_file_name = ResultantData["fitness_file_name"]
        t_score_file_name = ResultantData["t_score_file_name"]
        # strain_fit table is optional in the data type
        if "strain_fit_file_name" not in ResultantData:
            op_fns = [fit_file_name, t_score_file_name]
            KB_fh_list = [
                ResultantData["fit_scores_handle"],
                ResultantData["t_scores_handle"],
            ]
        else:
            # strain_fit included.
            op_fns = [
                fit_file_name,
                t_score_file_name,
                ResultantData["strain_fit_file_name"],
            ]
            KB_fh_list = [
                ResultantData["fit_scores_handle"],
                ResultantData["t_scores_handle"],
                ResultantData["strain_fit_handle"],
            ]
    else:
        raise Exception(f"Cannot recognize filetype: {ft}")

    for i in range(len(op_fns)):
        op_file_name = op_fns[i]
        KB_fh = KB_fh_list[i]
        # If there is a duplicate
        if op_file_name in os.listdir(ret_dp):
            logging.warning(
                f"File name {op_file_name} already in output directory, " + \
                "creating random name."
            )
            op_file_name = create_random_string(8) + ".tsv"
        # Output filepath
        op_fp = os.path.join(ret_dp, op_file_name)

        # Set params for shock to file
        ShockToFileParams = {
            "handle_id": KB_fh,
            "file_path": op_fp,
            "unpack": "uncompress",
        }
        ShockToFileOutput = dfu.shock_to_file(ShockToFileParams)
        logging.info(ShockToFileOutput)

        logging.info(f"Downloaded file for ref {ref} to location {op_fp}")

def parse_file_type(ft_str):
    ''' The goal of this is to convert a string of the form:
     KBaseRBTnSeq.RBTS_Gene_Fitness_T_Matrix-3.0  TO ->
     KBaseRBTnSeq.RBTS_Gene_Fitness_T_Matrix
    '''

    if not isinstance(ft_str, str):
        raise Exception("Upon downloading object, expecting obj info " + \
                        "to be a string.")

    split_str = ft_str.split("-")
    num = split_str[-1]
    last_is_num = True
    try:
        float(num)
    except ValueError:
        last_is_num = False 
    if not last_is_num:
        logging.warning("File Type ending expected float at end: " + ft_str)

    ft = ''.join(split_str[:-1])
    return ft
    



def create_random_string(length):
    # length should be int
    return "".join([random.choice(string.ascii_lowercase) for i in range(length)])


# Gets poolfile path
def download_poolfile(poolfile_ref, poolfile_path, dfu):

    GetObjectsParams = {"object_refs": [poolfile_ref]}

    # We get the handle id
    PoolFileObjectData = dfu.get_objects(GetObjectsParams)["data"][0]["data"]
    logging.info("DFU Pool File Get objects results:")
    logging.info(PoolFileObjectData)

    poolfile_handle = PoolFileObjectData["poolfile"]

    # Set params for shock to file
    ShockToFileParams = {
        "handle_id": poolfile_handle,
        "file_path": poolfile_path,
        "unpack": "uncompress",
    }
    ShockToFileOutput = dfu.shock_to_file(ShockToFileParams)
    logging.info(ShockToFileOutput)
    # Poolfile is at location "poolfile_path"

    return None
