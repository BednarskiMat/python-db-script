import sys, json, argparse, os
from string import Template
from db_connect import Connection
from php_format.format_php import format_php

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
batch_path = env_json["paths"]["batch"]



def ncs_new_client_insert(values, flag: str='--json'):
    ncs_insert_query  = """
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
        {insert_values}
            
        """
    if values and "--json" in flag:
        json_values = f"""
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
        return ncs_insert_query.format(insert_values = json_values)
    elif values and '--list' in flag:
        insert_values= f"""
        VALUES 
            (
                '{values[0]}',
                '{values[1]}',
                '{values[2]}',
                {values[3]},
                '{values[4]}',
                {values[5]},
                {values[6]},
                {values[7]},
                {values[8]},
                {values[9]},
                {values[10]},
                {values[11]}
            )
        """
        return ncs_insert_query.format(insert_values = insert_values)

    else:
        return  None

    

arg_vals = sys.argv


connection = Connection(dev_db_host, dev_db_user, dev_db_password)
#new_insert = connection.execute_query(ncs_new_client_insert(json_config["insert_values"],  '--json'))

#new_insert = connection.execute_query(ncs_new_client_insert(json_config["values_list"],  '--list'))
select_query = "select * from client_data_import.import_file_type"
client_import_file_type = connection.execute_read_query(select_query)
print(client_import_file_type[-1])
#if new_insert:
#    connection.execute_query(f"delete from client_data_import.IMPORT_FILE_TYPE  where id = {client_import_file_type[-1][0]}")



client_name = "placeholder"
path = f'{batch_path}/client_data_import/{client_name}'

if not os.path.exists(path):
    os.makedirs(path)





text = format_php('inventorymanufacturersdba', 'inventorymanufacturersdba', 21134, 21143)


# writing new content to the file
fp = open(f"{path}/img_alt.php", 'w')
fp.write(text)
print('Done Writing')
fp.close()


