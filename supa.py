import os
import datetime
from supabase import create_client, Client


url = "https://ifascjywgukzfdxfttqv.supabase.co"
key = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImlmYXNjanl3Z3VremZkeGZ0dHF2Iiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTY1NTQ2NTg3NCwiZXhwIjoxOTcxMDQxODc0fQ.SorE5d5Vw152ZJ3fSeHBpb9f8THEU-skyl5V5j9XVoM"


def insert_csv(path):
    if not os.path.isfile(path):
        return "csv not found"
    try:
        supabase: Client = create_client(url, key)
        if(check_file(os.path.basename(path))):
            supabase.storage().from_("csv").remove(os.path.basename(path))
        # concat name with today's date
        name_with_date = os.path.basename(path).split(".")[0] + "_" + str(datetime.date.today()) + ".csv"
        supabase.storage().from_("csv").upload(name_with_date,path)
        #os.remove(path)
        return "done"
    except:
        return "error uploading"

def check_file(name):
    try:
        supabase: Client = create_client(url, key)
        objects = supabase.storage().from_("csv").list()
        names = [o['name'] for o in objects]
        return name in names
    except:
        return "error retrieving file names"