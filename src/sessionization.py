import sys
import csv
import datetime

def unique(inputList) -> list: 
    '''
    given a list return unique elements of that list preserving the order
    '''
    unique_list = [] 

    for item in inputList: 
        if item not in unique_list: 
            unique_list.append(item) 
    
    return unique_list


def sessionize(intermediate, inactivity_period, current_time, file_handle, mode = "inactivity") -> None:
    '''
    given the intermediate queue and inactivity period find the inactive users and sessionize their log entry
    '''
    
    #get all user ip in intermediate queue
    intermediate_users = [item["user_ip"] for item in intermediate]
    #reduce to unique user ips
    uniq_intermediate_users = unique(intermediate_users)
   
    
    for user in uniq_intermediate_users:
        
        #get all entries that belong to a user in the intermediate
        user_intermediate = [item for item in intermediate if(item["user_ip"] == user)]
        
        #get first and last entry for that user
        first_entry = user_intermediate[0]
        last_entry = user_intermediate[-1]
        
        #if the user has been inactive based on the last entry
        #OR
        #if the end of log.csv is reached (mode="end")
        #sessionize the entries for that user and insert into sessionization list
        if((int((current_time - last_entry["datetime"]).total_seconds()) > inactivity_period) or (mode=="end")):           
            insert_sessionization = [None, None, None, None, None]
            insert_sessionization[0] = user
            insert_sessionization[1] = first_entry["datetime"].strftime("%Y-%m-%d %H:%M:%S")
            insert_sessionization[2] = last_entry["datetime"].strftime("%Y-%m-%d %H:%M:%S")
            insert_sessionization[3] = str(int((last_entry["datetime"] - first_entry["datetime"]).total_seconds() + 1))
            insert_sessionization[4] = str(len(user_intermediate))
            
            #sessionization.append(insert_sessionization)
            sessionization_str = ','.join(insert_sessionization) + "\n"
            file_handle.write(sessionization_str)
            
            #once the entries for the user is sessionized, remove those entries
            for item in user_intermediate:
                intermediate.remove(item)

def main():
    intermediate = []
    
    #read inactivity_period.txt
    f=open(sys.argv[2], "r")
    contents = f.read()
    inactivity_period = int(contents)
    f.close()
    
    #each sessionized entry will be appended to output.txt
    f=open(sys.argv[3], "a+")
    
    
    #read log.csv
    with open(sys.argv[1]) as csvfile:
        readCSV = csv.reader(csvfile, delimiter=',')
        header = next(readCSV)
    
        #order of columns from the input is not guaranteed 
        #get index of relevant columns
        index_ip = header.index("ip")
        index_date = header.index("date")
        index_time = header.index("time")
    
        #iterate over the entries of log.csv    
        for row in readCSV:
            
            #get user_ip and datetime from each row of log.csv
            insert = dict()
            insert["user_ip"] = row[index_ip]
            insert["datetime"] = datetime.datetime.strptime(row[index_date] + " " + row[index_time], "%Y-%m-%d %H:%M:%S")
            
            #insert into intermediate queue
            intermediate.append(insert)
            
            #use the datetime of current row to find inactive entries in the queue
            current_time = insert["datetime"]
            sessionize(intermediate, inactivity_period, current_time, f, mode ="inactivity")
               
        #at the end of the log everything becomes inactive and must be sessionized
        sessionize(intermediate, inactivity_period, current_time, f, mode="end")
        
    #close output file
    f.close()
    
if __name__ == '__main__':
    main()
        

