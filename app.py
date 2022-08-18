import sys, json, argparse
sys.path.append(".")
from db_connect import Connection

with open('env.json', 'r') as myfile:
    data=myfile.read()


# accept json file with values
parser = argparse.ArgumentParser()
parser.add_argument('--infile', nargs=1, help="JSON file to be processed", type=argparse.FileType('r'))
arguments = parser.parse_args()
json_config = json.load(arguments.infile[0])


# parse file, json holds env variables 
env_json = json.loads(data)
env = env_json["environments"]
dev_db_host= env['Dev']["host"]
dev_db_user= env['Dev']["db_user"]
dev_db_password= env['Dev']["db_password"]


def ncs_new_client_insert(values, flag: str='--json'):
    if values and "--json" in flag:
        ncs_insert_query  = f"""
        INSERT INTO client_data_import.IMPORT_FILE_TYPE 
            (
            client_group,
            file_type,
            file_group,
            div_id,
            process_language,
            customer_profile_class,
            ingest_target_table,
            ingest_notice_days,
            ingest_warning_days,
            active,
            email_operations_team,
            use_custom_schedule
            ) 
        VALUES 
            (
                {values["client_group"]},
                {values["file_type"]},
                {values["file_group"]},
                {values["div_id"]},
                {values["process_language"]},
                {values["customer_profile_class"]},
                {values["ingest_target_table"]},
                {values["ingest_notice_days"]},
                {values["ingest_warning_days"]},
                {values["active"]},
                {values["email_operations_team"]},
                {values["use_custom_schedule"]}
                
            )
            
        """
        return ncs_insert_query

    else:
        return None
    
#('Inventory Manufacturers dba', "raci_chart",'raci_chart',21143,'PHP',null,null,31,61,1,0, 0);

arg_vals = sys.argv


connection = Connection(dev_db_host, dev_db_user, dev_db_password)
new_insert = connection.execute_query(ncs_new_client_insert(json_config["insert_values"],  '--json'))
select_query = "select * from client_data_import.import_file_type"
client_import_file_type = connection.execute_read_query(select_query)
print(client_import_file_type[-1])
if new_insert:
    connection.execute_query(f"delete from client_data_import.IMPORT_FILE_TYPE  where id = {client_import_file_type[-1][0]}")
