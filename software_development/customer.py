import re
from dataclasses import dataclass, field


# dataclass of customer including an alphanumeric id, a name, and a birthday
@dataclass(frozen=False)  # frozen means that the class cannot be modified after creation. This is useful for storing data in databases or other persistent storages (e.g., files).
class Customer:
    cust_id : str = field()   # this defines how to create instances from the class; it's called "field" because we're creating fields within our object/instance 
    firstname : str = ""      # these are default values if no value was provided when instantiating objects using this class  
    lastname : str = ""       # note that there can only ever exist one instance variable per line - you'll get errors otherwise!

    def __post_init__(self):
        """This method runs automatically once upon instantiation"""

        self._validate_cust_id()    # validate input before saving anything into memory 
        self.__set_fullname__()     # set full name based on given inputs

    @property        # getter function used by Python interpreter whenever trying to access property directly instead of through. notation e.g.: myobj.firstname vs just myobj.firstname()
    def fullname(self)->str:  
        return f"{self.lastname}, {self.firstname}"
    
    ## private methods below here 
    
    ### validation functions go here  

    def _validate_cust_id(self):
        
        assert len(self.cust_id)==8, \
            ValueError("Customer ID must have exactly eight characters") 

        try: 
            int(self.cust_id[0]) == True   
        except Exception as err:  
            raise TypeError('First character of CustID should be numeric') from None
        
    #### setter functions go here 

    def __set_fullname__(self):    
        '''sets the customers' full name'''
        names = [x.strip().title() for x in re.split("[\W]+", self.firstname)] + [''] * max((1,-len([y.strip().title() for y in re.split("[\W]+", self.lastname)])) )
        print(names)
        self.firstname=' '.join(filter(None,[n[:3]for n in reversed(names)])+[''])
        self.lastname =''.join([' '*(4-len(l))+' '+ l[-2:]if not l=='I' else '' for l in filter(None,[n[:-2].upper()+','*bool(re.search('[aeiou]',n))+n[-2:].upper() for n in reversed(names)])]).rstrip(',')


if __name__ == "__main__":
    # added manually
    Customer("12345678", "Ben", "Auffarth")
