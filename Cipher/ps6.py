import string


def load_words(file_name):
    '''
    file_name (string): the name of the file containing 
    the list of words to load    
    
    Returns: a list of valid words. Words are strings of lowercase letters.
    
    '''
    print('Loading word list from file...')
    # inFile: file
    in_file = open(file_name, 'r')
    # line: string
    line = in_file.readline()
    # word_list: list of strings
    word_list = line.split()
    print('  ', len(word_list), 'words loaded.')
    in_file.close()
    return word_list

def is_word(word_list, word):
    '''
    Determines if word is a valid word, ignoring
    capitalization and punctuation

    Returns: True if word is in word_list, False otherwise

 
    '''
    word = word.lower()
    word = word.strip(" !@#$%^&*()-_+={}[]|\:;'<>?,./\"")
    return word in word_list


def get_story_string():

    f = open("story.txt", "r")
    story = str(f.read())
    f.close()
    return story

WORDLIST_FILENAME = 'words.txt'

class Message(object):
    
    def __init__(self, text):
        '''
        Initializes a Message object
                
        text (string): the message's text

        '''
        self.message_text = text
        self.valid_words = load_words(WORDLIST_FILENAME)


    def get_message_text(self):
        '''
        Used to safely access self.message_text outside of the class
        
        Returns: self.message_text
        '''
        return self.message_text

    def get_valid_words(self):
        '''
        Used to safely access a copy of self.valid_words outside of the class
        
        Returns: a COPY of self.valid_words
        '''
        return self.valid_words[:]
        
    def build_shift_dict(self, shift):
        '''
        Creates a dictionary that can be used to apply a cipher to a letter.
        The dictionary maps every uppercase and lowercase letter to a
        character shifted down the alphabet by the input shift. 
        
        shift (integer): the amount by which to shift every letter of the 
        alphabet. 0 <= shift < 26

        Returns: a dictionary mapping a letter (string) to 
                 another letter (string). 
        '''
        
        dict1 = {}
        str1 = string.ascii_uppercase
        for s in str1:
            if (ord(s)+shift-65) < 26 :
                dict1[s] = chr(ord(s)+shift)
            elif (ord(s)+shift-65) >= 26 :
                dict1[s] = chr(ord(s)+shift-26)
        
        str1 = string.ascii_lowercase
        for s in str1:
            if (ord(s)+shift-97) < 26 :
                dict1[s] = chr(ord(s)+shift)
            elif (ord(s)+shift-97) >= 26 :
                dict1[s] = chr(ord(s)+shift-26)
        
        return dict1    


    def apply_shift(self, shift):
        '''
        Applies the Caesar Cipher to self.message_text with the input shift.
        Creates a new string that is self.message_text shifted down the
        alphabet by some number of characters determined by the input shift        
        
        shift (integer): the shift with which to encrypt the message.
        0 <= shift < 26

        Returns: the message text (string) in which every character is shifted
             down the alphabet by the input shift
        '''
        msg=self.get_message_text()
        newmsg=""
        dict1=self.build_shift_dict(shift)
        huh=dict1.keys()
        for char in msg:
            if char in huh:
                newmsg+=dict1.get(char)
            else:
                newmsg+=char
        return newmsg
                
            
            
        

class PlaintextMessage(Message):

    def __init__(self, text, shift):

        '''

        Initializes a PlaintextMessage object        
        
        text (string): the message's text

        shift (integer): the shift associated with this message



        A PlaintextMessage object inherits from Message and has five attributes:

            self.message_text (string, determined by input text)

            self.valid_words (list, determined using helper function load_words)

            self.shift (integer, determined by input shift)

            self.encrypting_dict (dictionary, built using shift)

            self.message_text_encrypted (string, created using shift
            '''
      
        self.shift = shift

        self.message_text = text

        self.valid_words = load_words(WORDLIST_FILENAME)

        self.encrypting_dict = super(PlaintextMessage, self).build_shift_dict(shift)

        self.message_text_encrypted = super(PlaintextMessage, self).apply_shift(shift)



    def get_shift(self):

        '''

        Used to safely access self.shift outside of the class

        

        Returns: self.shift

        '''

        return self.shift



    def get_encrypting_dict(self):

        '''

        Used to safely access a copy self.encrypting_dict outside of the class

        

        Returns: a COPY of self.encrypting_dict

        '''

        

        encrypting_dict_copy = self.encrypting_dict.copy()

        return encrypting_dict_copy



    def get_message_text_encrypted(self):

        '''

        Used to safely access self.message_text_encrypted outside of the class

        

        Returns: self.message_text_encrypted

        '''

        

        return self.message_text_encrypted



    def change_shift(self, shift):

        '''

        Changes self.shift of the PlaintextMessage and updates other 

        attributes determined by shift (ie. self.encrypting_dict and 

        message_text_encrypted).

        

        shift (integer): the new shift that should be associated with this message.

        0 <= shift < 26



        Returns: nothing

        '''

       

        self.shift = shift

        self.encrypting_dict = super(PlaintextMessage, self).build_shift_dict(shift)

        self.message_text_encrypted = super(PlaintextMessage, self).apply_shift(shift)

        

# Correct
class CiphertextMessage(Message):
    def __init__(self, text):
        '''
        Initializes a CiphertextMessage object
                
        text (string): the message's text

        a CiphertextMessage object has two attributes:
            self.message_text (string, determined by input text)
            self.valid_words (list, determined using helper function load_words)
        '''
        Message.__init__(self,text)
        
        
        
        

    def decrypt_message(self):
        '''
        Decrypt self.message_text by trying every possible shift value
        and find the "best" one. 

        Returns: a tuple of the best shift value used to decrypt the message
        and the decrypted message text using that shift value
        '''
        bestscore=0
        
        
        for s in range(26):
            best=0
            shifted_sent=self.apply_shift(s)
            words=shifted_sent.split(' ')
            for word in words:
                if is_word(self.valid_words,word):
                    best=best+1
            if best>bestscore:
                bestscore=s
                final=self.apply_shift(s)
        return (bestscore,final)
    
                    
            
            
            
            
            

##Example test case (PlaintextMessage)
#plaintext = PlaintextMessage('hello', 2)
#print('Expected Output: jgnnq')
#print('Actual Output:', plaintext.get_message_text_encrypted())
#    
##Example test case (CiphertextMessage)
#ciphertext = CiphertextMessage('jgnnq')
#print('Expected Output:', (24, 'hello'))
#print('Actual Output:', ciphertext.decrypt_message())
#
#ciphertext = CiphertextMessage('hello')
#print('Test Output:', ciphertext.decrypt_message())
#
def decrypt_story():
    decrypted=CiphertextMessage(get_story_string())
    print (decrypted.decrypt_message())



                              
