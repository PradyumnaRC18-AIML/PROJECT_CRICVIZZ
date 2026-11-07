import builtins
import os
import sys

class QueryError(Exception):
    def __init__(self, message):
        self.message = message
    def __str__(self):
        return self.message

def SilientDisplay(*args, **kwargs):
    pass

class FIND_FILE:
    PATH = None
    @staticmethod
    def goToRoot(display = print):
        path = os.getcwd()
        try:
            if os.name == 'nt':
                if sys.version_info[0:2:1] < (3,12):
                    component_path = os.path.splitdrive(path)
                    root_path = component_path[0]+'\\' 
                else :
                    component_path = os.path.splitroot(path)
                    root_path = component_path[0]+component_path[1] 
            else :
                root_path = '/' 
            if path != root_path:
                os.chdir(root_path)
            return True
        except Exception as err:
            display("NAME:",err.__class__.__name__)
            display("Cause of error",str(err))
            display("__traceback__",err.__traceback__)
            try:
                os.chdir(path)
            except Exception as err:
                display("NAME:",err.__class__.__name__)
                display("Cause of error",str(err))
                display("__traceback__",err.__traceback__)
                return False

    @staticmethod
    def getStartingDirectory(display,starting_directory = None):
        current = os.getcwd()
        FIND_FILE.PATH = current
        if starting_directory is None:
            x = FIND_FILE.goToRoot(display)
            return x
        else:
            if os.path.isdir(starting_directory):
                try:
                    os.chdir(starting_directory)
                except Exception as err:
                    display("NAME:",err.__class__.__name__)
                    display("Cause of error",str(err))
                    display("__traceback__",err.__traceback__)
                    FIND_FILE.PATH = None
                    return False
                return True
            return False
    
    def __new__(cls, file, starting_directory = None, * ,display = SilientDisplay, iter_mode = False):
        SUCCESS_WORK = cls.getStartingDirectory(display,starting_directory)
        if not SUCCESS_WORK:
            cls.PATH = None
            return None
        try:
            os.chdir(cls.PATH)
        except Exception as err:
            display("NAME:",err.__class__.__name__)
            display("Cause of error",str(err))
            display("__traceback__",err.__traceback__)
            cls.PATH = None
            return None
        return super().__new__(cls)

    def __init__(self, file, starting_directory = None, * ,display = SilientDisplay, iter_mode = False):
        self.file = file
        self.visited = []
        self.display = display
        self.starting_directory = starting_directory
        self.visitedSet = set()
        self.iter_mode = iter_mode
        self.iter_count = 0
    
    def __recursive_depth_first_search(self,current_directory):
        if current_directory in self.visited:
            return None
        else:
            if self.iter_mode == False:
                self.display(current_directory)
            else:
                self.display("iteration:",self.iter_count,current_directory)
            self.iter_count += 1
            self.visited.append(current_directory)
        
        if not os.path.isdir(current_directory):
            if self.file == os.path.basename(current_directory):
                return current_directory
            else:
                return None
        else:
            path_list = []
            try:
                path_list = os.listdir(current_directory)
            except (OSError, PermissionError):
                return None
            for i in path_list:
                next_path = os.path.join(current_directory,i)
                next_dfs = self.__recursive_depth_first_search(next_path)
                if next_dfs is not None:
                    return next_dfs
        return None

    def __iterative_depth_first_search(self,current_directory):
        STACK = []
        if current_directory not in self.visitedSet:
            self.visitedSet.add(current_directory)
            STACK.append(current_directory)
        while len(STACK) > 0:
            popped_value = STACK.pop()
            if self.iter_mode == False:
                self.display(popped_value)
            else:
                self.display("iteration:",self.iter_count,popped_value)
            self.iter_count += 1
            if os.path.isfile(popped_value):
                if self.file == os.path.basename(popped_value):
                    return popped_value
            elif os.path.isdir(popped_value):
                path_list = []
                try:
                    path_list = os.listdir(popped_value)
                except(OSError, PermissionError):
                    continue
                for i in path_list:
                    next_path = os.path.join(popped_value,i)
                    if next_path not in self.visitedSet:
                        self.visitedSet.add(next_path)
                        STACK.append(next_path)
        return None
    
    def search(self,query):
        if self.iter_count != 0:
            self.iter_count = 0
        
        query = query.lower()
        
        dict_query = {"recursive":self.__recursive_depth_first_search, "iterative":self.__iterative_depth_first_search}
        if query not in dict_query:
            raise QueryError("query is not valid")
        try:
            SUCCESS = FIND_FILE.getStartingDirectory(self.display,self.starting_directory)
            if not SUCCESS:
                try:
                    if FIND_FILE.PATH is not None:
                        os.chdir(FIND_FILE.PATH)
                except Exception as err:
                    self.display("NAME:", err.__class__.__name__)
                    self.display("Cause of error", str(err))
                    self.display("__traceback__", err.__traceback__)
                finally:
                    FIND_FILE.PATH = None
                return None
        except Exception as err:
            self.display("NAME:",err.__class__.__name__)
            self.display("Cause of error",str(err))
            self.display("__traceback__",err.__traceback__)
            try:
                if FIND_FILE.PATH is not None:
                    os.chdir(FIND_FILE.PATH)
            except Exception as err:
                self.display("NAME:",err.__class__.__name__)
                self.display("Cause of error",str(err))
                self.display("__traceback__",err.__traceback__)
            finally:
                FIND_FILE.PATH = None
            return None

        try:
            return dict_query[query.lower()](os.getcwd())
        finally:
            if query == "iterative":
                self.visitedSet = set()
            elif query == "recursive" :
                self.visited = []
            try:
                os.chdir(FIND_FILE.PATH)
            except Exception as err:
                self.display("NAME:",err.__class__.__name__)
                self.display("Cause of error",str(err))
                self.display("__traceback__",err.__traceback__)
            finally:
                FIND_FILE.PATH = None
                
if __name__ == '__main__':
    system_list = sys.argv
    system_count = len(sys.argv)

    dict_info = {
        'file': None,
        'starting_directory' : None,
        'display' : print,
        'iter_mode' : True
    }

    class WrongUsageException(Exception):
        def __init__(self,message):
            super().__init__(message)
    
    if system_count < 3 or system_count > 9:
        raise WrongUsageException("Not proper prompt. usage: python path_finder.py file_name method -s starting_directory -i iter_mode -d display")
    if system_list[2].lower() not in ('iterative','recursive'):
        raise WrongUsageException("Invalid Method")     
    if (('-i' not in system_list) and ('-s' not in system_list) and ('-d' not in system_list))  and system_count > 3:
        raise WrongUsageException("Python couldn't identify the invalid command")
    for i in system_list:
        if len(i) > 0:
            if i[0] == '-' and (len(i) == 1 or i[1::] not in ['d','s','i']):
                raise WrongUsageException("Invalid option: "+i)
        else:
            raise WrongUsageException("Empty prompt detection")   
    for i in range(0,system_count):
        if len(system_list[i]) > 0:
            if (system_list[i][0] == '-') and ((i == system_count-1) or len(system_list[i+1]) < 1 or system_list[i+1][0] == '-'):
                raise WrongUsageException("No value provided for the option "+system_list[i])
        else:
            raise WrongUsageException("Empty prompt detection")
    dict_count = {}
    for i in system_list:
        if i[0] == '-':
            try:
                dict_count[i] += 1
            except:
                dict_count[i] = 1
    if len(dict_count) >= 1 and max(dict_count.values()) > 1:
        raise WrongUsageException("Duplicate command")
    
    for i in range(0,system_count):
        if system_list[i].lower() == '-s' and not(os.path.isdir(os.path.abspath(system_list[i+1]))):
            raise WrongUsageException("Invalid Starting Directory")     
        if system_list[i].lower() == '-i' and not (system_list[i+1].lower() in ('true','false')):
            raise WrongUsageException("Invalid Iterative Mode. Please provide -i <True/False>")
        if system_list[i].lower()== '-d':
            default = {'print':print, 'silientdisplay':SilientDisplay}
            if system_list[i+1].lower() in default:
                x = default[system_list[i+1].lower()] 
            else:
                x = getattr(builtins,system_list[i+1],None)
            if x is None:
                raise WrongUsageException("Invalid Display mode")
            if not callable(x):
                raise WrongUsageException("Display mode must be callable")     
            dict_info['display'] = x
        if system_list[i].lower() == '-s':
            dict_info['starting_directory'] = os.path.abspath(system_list[i+1])
        elif system_list[i].lower() == '-i':
            dict_info['iter_mode'] = system_list[i+1].lower() == 'true'
    dict_info['file'] = system_list[1]

    try:
        FILE_FINDER = FIND_FILE(**dict_info)
        if FILE_FINDER is None:
            print("Unable to allocate the starting directory")
            sys.exit(1)
        SEARCH_FILE = FILE_FINDER.search(system_list[2])
        if SEARCH_FILE is None:
            print("Unable to search the file")
            sys.exit(1)
        else:
            print("FILE FOUND AT",SEARCH_FILE)
    except Exception as err:
        print(err)