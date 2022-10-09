import mysql.connector

class my_db:
    
    def __init__(self, user, password, host, database):
        self.user = user
        self.password = password
        self.host = host
        self.database = database
        
    def SQL_command(self, command):
        # setup SQL access
        cnx = mysql.connector.connect(user=self.user, password=self.password,
                                      host=self.host,
                                      database=self.database)
        cursor = cnx.cursor()
        
        query = command  
        # print(query)
        
        cursor.execute(query)
        out_data = cursor.fetchall()
        
        cnx.commit()
        cursor.close()
        cnx.close()
        return out_data
    
    def update_table(self, table_name, column, value, constrain = ""):
        if constrain == "":
            command = "UPDATE {} SET {} = {}".format(table_name, column, value)
        else:
            command = "UPDATE {} SET {} = {} WHERE {}".format(table_name, column, value, constrain)
        self.SQL_command(command)
        return
    
    def delete_from_table(self, table, constrain):
        command = "DELETE FROM {} WHERE {}".format(table, constrain)
        self.SQL_command(command)
        return
    
    def get_from_table(self, table_name, column, constrain = ""):
        if constrain == "":
            command = "SELECT {} FROM {}".format(column, table_name)
        else:
            command = "SELECT {} FROM {} WHERE {}".format(column, table_name, constrain)
        data_out = self.SQL_command(command)
        return data_out